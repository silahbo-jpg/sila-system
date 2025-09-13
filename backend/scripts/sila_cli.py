#!/usr/bin/env python3
"""
SILA System CLI - Main Entry Point

Command-line interface for managing the SILA governance system.
Follows the required structure: python scripts/main.py [command] [options]

Implements all the workflows from the instructions:

1. Municipality management
2. User creation and management  
3. Citizen registration with full address hierarchy
4. Location hierarchy management
5. System initialization

Usage:
    python scripts/main.py [command] [options]

Examples from instructions:
    python scripts/main.py create-municipality --name "Caála" --province "Huambo" --slug caala
    python scripts/main.py create-user --role municipal_manager --municipality caala --email manager.caala@gov.ao
    python scripts/main.py register-citizen --name "Maria João" --bi 003456789LA045 --province Huambo --municipality Caála --commune Cambuengo --neighborhood "Bairro Novo" --street "Rua 12 de Julho" --house 45
"""

import asyncio
import sys
import os
from pathlib import Path
import click
from typing import Optional, List, Dict, Any
from decimal import Decimal

# Add the backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update, delete, func
from sqlalchemy.future import select as async_select

from app.core.config import settings
from app.core.location.services import LocationService
from app.core.identity.services import CitizenService
from app.core.payment.services import PaymentService
from app.core.location.models import CountryCreate, ProvinceCreate, MunicipalityCreate, CommuneCreate
from app.core.identity.models import CitizenCreate, CitizenRegistration
from app.core.security import get_password_hash
from app.db.database import Base, get_db
from app.models.postgres import User, Country, Province, Municipality, Commune, Citizen


def get_async_session() -> AsyncSession:
    """Create and return an async database session."""
    DATABASE_URL = settings.DATABASE_URL or "postgresql+asyncpg://postgres:Truman1*@localhost:5432/sila_dev"
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    return async_session()


@click.group()
def cli():
    """SILA System Command Line Interface"""
    pass


@cli.command("init-system")
@click.option("--with-sample-data", is_flag=True, help="Create sample data for testing")
def init_system(with_sample_data: bool):
    """Initialize the SILA system with basic data"""
    async def _init():
        db = await get_async_session()
        
        try:
            # Initialize Angola location data
            print("🌍 Initializing Angola location data...")
            result = await LocationService.initialize_angola_data(db)
            print(f"✅ {result['message']}")
            
            # Initialize payment providers
            print("💳 Setting up payment providers...")
            result = await PaymentService.initialize_default_providers(db)
            print(f"✅ {result['message']}")
            
            if with_sample_data:
                print("📊 Creating sample data...")
                await _create_sample_data(db)
                print("✅ Sample data created")
                
            print("\n🎉 SILA system initialized successfully!")
            
        finally:
            await db.close()
    
    asyncio.run(_init())


@cli.command("create-municipality")
@click.option("--name", required=True, help="Municipality name")
@click.option("--province", required=True, help="Province name")
@click.option("--slug", help="URL-friendly slug (auto-generated if not provided)")
@click.option("--code", help="Municipality code")
@click.option("--population", type=int, help="Population")
def create_municipality(name: str, province: str, slug: Optional[str], code: Optional[str], population: Optional[int]):
    """Create a new municipality portal"""
    async def _create():
        db = await get_async_session()
        
        try:
            # Find province
            province_obj = await db.execute(async_select(Province).where(Province.name == province))
            province_obj = province_obj.scalars().first()
            if not province_obj:
                click.echo(f"❌ Province '{province}' not found")
                return
            
            # Create municipality
            municipality_data = MunicipalityCreate(
                name=name,
                slug=slug or name.lower().replace(" ", "-"),
                code=code,
                population=population,
                province_id=province_obj.id
            )
            
            municipality = await LocationService.create_municipality(db, municipality_data)
            click.echo(f"✅ Municipality '{name}' created successfully")
            click.echo(f"   Portal URL: sila.gov.ao/{municipality.slug}")
            click.echo(f"   ID: {municipality.id}")
            
        except Exception as e:
            click.echo(f"❌ Error: {str(e)}")
        finally:
            await db.close()
    
    asyncio.run(_create())


@cli.command("create-user")
@click.option("--role", required=True, type=click.Choice(["municipal_manager", "provincial_staff", "national_staff", "citizen"]))
@click.option("--municipality", help="Municipality slug (required for municipal_manager)")
@click.option("--email", required=True, help="User email")
@click.option("--name", help="User full name")
@click.option("--password", help="User password (prompted if not provided)")
def create_user(role: str, municipality: Optional[str], email: str, name: Optional[str], password: Optional[str]):
    """Create a new user account"""
    async def _create():
        db = await get_async_session()
        
        try:
            if not password:
                password = click.prompt("Password", hide_input=True)
            
            municipality_id = None
            if municipality:
                municipality_obj = await db.execute(async_select(Municipality).where(Municipality.slug == municipality))
                municipality_obj = municipality_obj.scalars().first()
                if not municipality_obj:
                    click.echo(f"❌ Municipality '{municipality}' not found")
                    return
                municipality_id = municipality_obj.id
            
            # Create user
            user_data = {
                "email": email,
                "name": name or email.split("@")[0],
                "hashed_password": get_password_hash(password),
                "user_type": role,
                "municipality_id": municipality_id,
                "is_active": True
            }
            
            user = await db.execute(async_select(User).where(User.email == email))
            user = user.scalars().first()
            if user:
                click.echo(f"❌ User '{email}' already exists")
                return
            
            user = User(**user_data)
            db.add(user)
            await db.commit()
            click.echo(f"✅ User '{email}' created successfully")
            click.echo(f"   Role: {role}")
            click.echo(f"   ID: {user.id}")
            
        except Exception as e:
            click.echo(f"❌ Error: {str(e)}")
        finally:
            await db.close()
    
    asyncio.run(_create())


@cli.command("register-citizen")
@click.option("--name", required=True, help="Citizen full name")
@click.option("--bi", required=True, help="BI number (13 characters)")
@click.option("--province", required=True, help="Province name")
@click.option("--municipality", required=True, help="Municipality name")
@click.option("--commune", help="Commune name")
@click.option("--neighborhood", help="Neighborhood (Bairro)")
@click.option("--street", help="Street name")
@click.option("--house", help="House number")
@click.option("--phone", help="Phone number")
@click.option("--email", help="Email address")
@click.option("--create-account", is_flag=True, help="Create user account for citizen")
def register_citizen(name: str, bi: str, province: str, municipality: str, commune: Optional[str], 
                    neighborhood: Optional[str], street: Optional[str], house: Optional[str],
                    phone: Optional[str], email: Optional[str], create_account: bool):
    """Register a new citizen with full address hierarchy"""
    async def _register():
        db = await get_async_session()
        
        try:
            # Find location hierarchy
            country = await db.execute(async_select(Country).where(Country.code == "AO"))
            country = country.scalars().first()
            province_obj = await db.execute(async_select(Province).where(Province.name == province))
            province_obj = province_obj.scalars().first()
            municipality_obj = await db.execute(async_select(Municipality).where(Municipality.name == municipality))
            municipality_obj = municipality_obj.scalars().first()
            commune_obj = None
            
            if not all([country, province_obj, municipality_obj]):
                click.echo("❌ Location hierarchy not found. Please check country, province, and municipality.")
                return
            
            if commune:
                commune_obj = await db.execute(async_select(Commune).where(Commune.name == commune, Commune.municipality_id == municipality_obj.id))
                commune_obj = commune_obj.scalars().first()
                if not commune_obj:
                    click.echo(f"❌ Commune '{commune}' not found in municipality '{municipality}'")
                    return
            
            # Create citizen
            citizen_data = CitizenCreate(
                full_name=name,
                bi_number=bi,
                phone=phone,
                email=email,
                country_id=country.id,
                province_id=province_obj.id,
                municipality_id=municipality_obj.id,
                commune_id=commune_obj.id if commune_obj else None,
                neighborhood=neighborhood,
                street=street,
                house_number=house,
            )
            
            registration = CitizenRegistration(
                citizen=citizen_data,
                create_user_account=create_account,
                username=email if create_account and email else None,
                password=click.prompt("Password", hide_input=True) if create_account else None
            )
            
            citizen, user = await CitizenService.register_citizen(db, registration)
            
            click.echo(f"✅ Citizen '{name}' registered successfully")
            click.echo(f"   BI: {bi}")
            click.echo(f"   Location: {municipality}, {province}")
            click.echo(f"   Citizen ID: {citizen.id}")
            
            if user:
                click.echo(f"   User account created: {user.email}")
            
        except Exception as e:
            click.echo(f"❌ Error: {str(e)}")
        finally:
            await db.close()
    
    asyncio.run(_register())


@cli.command("list-municipalities")
@click.option("--province", help="Filter by province name")
def list_municipalities(province: Optional[str]):
    """List all municipalities"""
    async def _list():
        db = await get_async_session()
        
        try:
            where_clause = {}
            if province:
                province_obj = await db.execute(async_select(Province).where(Province.name == province))
                province_obj = province_obj.scalars().first()
                if province_obj:
                    where_clause["province_id"] = province_obj.id
            
            municipalities = await db.execute(async_select(Municipality).where(where_clause).order_by(Municipality.name.asc()))
            municipalities = municipalities.scalars().all()
            
            click.echo(f"📋 Found {len(municipalities)} municipalities:")
            for mun in municipalities:
                click.echo(f"   • {mun.name} ({mun.slug}) - {mun.province.name}, {mun.province.country.name}")
                click.echo(f"     Portal: sila.gov.ao/{mun.slug}")
            
        except Exception as e:
            click.echo(f"❌ Error: {str(e)}")
        finally:
            await db.close()
    
    asyncio.run(_list())


@cli.command("citizen-stats")
@click.option("--municipality", help="Municipality slug")
def citizen_stats(municipality: Optional[str]):
    """Show citizen statistics"""
    async def _stats():
        db = await get_async_session()
        
        try:
            if municipality:
                municipality_obj = await db.execute(async_select(Municipality).where(Municipality.slug == municipality))
                municipality_obj = municipality_obj.scalars().first()
                if not municipality_obj:
                    click.echo(f"❌ Municipality '{municipality}' not found")
                    return
                
                citizens = await CitizenService.get_citizens_by_municipality(db, municipality_obj.id)
                click.echo(f"📊 Citizens in {municipality_obj.name}: {len(citizens)}")
            else:
                stats = await CitizenService.get_citizen_statistics(db)
                click.echo("📊 SILA System Citizen Statistics:")
                click.echo(f"   Total Citizens: {stats.total_citizens}")
                click.echo(f"   Verified Citizens: {stats.verified_citizens}")
                click.echo(f"   Active Citizens: {stats.active_citizens}")
                click.echo(f"   Recent Registrations (30 days): {stats.recent_registrations}")
            
        except Exception as e:
            click.echo(f"❌ Error: {str(e)}")
        finally:
            await db.close()
    
    asyncio.run(_stats())


async def _create_sample_data(db: AsyncSession):
    """Create sample data for testing"""
    from uuid import uuid4
    
    # Create a test country
    country = Country(
        id=str(uuid4()),
        name="Test Country",
        code="TC",
        is_active=True
    )
    db.add(country)
    
    # Create a test province
    province = Province(
        id=str(uuid4()),
        name="Test Province",
        code="TP",
        country_id=country.id,
        is_active=True
    )
    db.add(province)
    
    # Create a test municipality
    municipality = Municipality(
        id=str(uuid4()),
        name="Test Municipality",
        slug="test-municipality",
        province_id=province.id,
        is_active=True
    )
    db.add(municipality)
    
    await db.commit()


if __name__ == "__main__":
    cli()