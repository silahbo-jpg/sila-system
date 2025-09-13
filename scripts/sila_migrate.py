#!/usr/bin/env python3
# 📌 sila_dev_migrate.py - Ferramenta de migração para sila_dev 2.0

import psycopg2
import logging
from datetime import datetime
import hashlib
import bcrypt
import sys
import os
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional, List
import json

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('migration.log')
    ]
)
logger = logging.getLogger('sila_dev_migrate')

class Config:
    """Configurações da migração"""
    # Configurações do PostgreSQL
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'sila_db')
    DB_USER = os.getenv('DB_USER', 'sila_user')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'sila_password')
    
    # Segurança
    DEFAULT_PASSWORD = 'Truman1_Marcelo1_1985'  # Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1* temporária
    
    # Configurações de Email (Atualize com suas credenciais)
    SMTP_SERVER = "smtp.seudominio.com"
    SMTP_PORT = 587
    SMTP_USER = "seu_email@exemplo.com"
    SMTP_PASSWORD = "sua_Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*"
    NOTIFICATION_FROM = "no-reply@sila_dev-system.com"
    NOTIFICATION_SUBJECT = "Atualização da sua conta sila_dev"
    NOTIFICATION_TEMPLATE = """
    Olá {name},
    
    Sua conta foi migrada para a nova versão do sila_dev.
    
    Por questões de segurança, solicitamos que você redefina sua Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1* acessando:
    {reset_link}
    
    Este link expira em 24 horas.
    
    Atenciosamente,
    Equipe sila_dev
    """

class Security:
    """Utilitários de segurança"""
    @staticmethod
    def create_password_hash(password: str) -> str:
        """Gera hash de Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1* com bcrypt ou fallback para SHA-256"""
        try:
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        except Exception as e:
            logger.warning(f"Falha no bcrypt, usando hashlib: {str(e)}")
            return hashlib.sha256(password.encode('utf-8') + b'sila_dev_salt').hexdigest()
    
    @staticmethod
    def generate_reset_token() -> str:
        """Gera um token seguro para redefinição de Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*Truman1*Marcelo1*"""
        return hashlib.sha256(os.urandom(60)).hexdigest()

class DatabaseManager:
    """Gerencia conexões com o banco de dados"""
    def __init__(self, db_config: Dict[str, str]):
        self.db_config = db_config
        self.source_conn = None
        self.target_conn = None
    
    def __enter__(self):
        try:
            # Conexão com o banco de dados PostgreSQL
            self.source_conn = psycopg2.connect(
                host=self.db_config['DB_HOST'],
                port=self.db_config['DB_PORT'],
                database=self.db_config['DB_NAME'],
                user=self.db_config['DB_USER'],
                password=self.db_config['DB_PASSWORD']
            )
            self.target_conn = psycopg2.connect(
                host=self.db_config['DB_HOST'],
                port=self.db_config['DB_PORT'],
                database=self.db_config['DB_NAME'],
                user=self.db_config['DB_USER'],
                password=self.db_config['DB_PASSWORD']
            )
            return self
        except psycopg2.Error as e:
            logger.error(f"Erro ao conectar ao banco de dados: {str(e)}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.source_conn:
            self.source_conn.close()
        if self.target_conn:
            if exc_type is None:
                self.target_conn.commit()
            else:
                self.target_conn.rollback()
            self.target_conn.close()

class MigrationManager:
    """Gerencia o processo de migração"""
    def __init__(self, db: DatabaseManager, dry_run: bool = False):
        self.db = db
        self.dry_run = dry_run
        self.results = {
            'total': 0,
            'success': 0,
            'skipped': 0,
            'errors': 0
        }
        self.notifications = []
    
    def migrate_citizens(self) -> bool:
        """Migra a tabela de cidadãos"""
        logger.info("🔄 Migrando cidadãos...")
        
        try:
            source_cur = self.db.source_conn.cursor()
            target_cur = self.db.target_conn.cursor()
            
            # Obter dados dos cidadãos
            source_cur.execute("SELECT * FROM citizens")
            citizens = source_cur.fetchall()
            
            if not source_cur.description:
                logger.warning("Tabela 'citizens' não encontrada ou vazia")
                return True
                
            source_cols = [col[0] for col in source_cur.description]
            
            for citizen in citizens:
                self.results['total'] += 1
                citizen_data = dict(zip(source_cols, citizen))
                
                # Mapear campos para o novo esquema
                migration_data = {
                    'id': citizen_data.get('id'),
                    'name': citizen_data.get('name', ''),
                    'cpf': citizen_data.get('cpf', ''),
                    'birth_date': citizen_data.get('birth_date'),
                    'address': citizen_data.get('address', ''),
                    'phone': citizen_data.get('phone', ''),
                    'email': citizen_data.get('email', ''),
                    'created_at': citizen_data.get('created_at', datetime.now().isoformat()),
                    'updated_at': citizen_data.get('updated_at', datetime.now().isoformat())
                }
                
                # Se for dry run, apenas loga
                if self.dry_run:
                    logger.info(f"[DRY RUN] Migraria cidadão: {migration_data['name']} (CPF: {migration_data['cpf']})")
                    self.results['success'] += 1
                    continue
                
                # Tenta inserir o cidadão
                try:
                    columns = ', '.join([f'"{k}"' for k in migration_data.keys()])
                    placeholders = ', '.join(['%s'] * len(migration_data))
                    query = f'INSERT INTO citizens ({columns}) VALUES ({placeholders}) ON CONFLICT (id) DO NOTHING'
                    
                    target_cur.execute(query, list(migration_data.values()))
                    if target_cur.rowcount > 0:
                        self.results['success'] += 1
                    else:
                        logger.warning(f"Cidadão já existe: {migration_data.get('cpf')}")
                        self.results['skipped'] += 1
                    
                except psycopg2.IntegrityError as e:
                    if "duplicate key value violates unique constraint" in str(e):
                        logger.warning(f"Cidadão já existe: {migration_data.get('cpf')}")
                        self.results['skipped'] += 1
                    else:
                        logger.error(f"Erro ao migrar cidadão {migration_data.get('cpf')}: {str(e)}")
                        self.results['errors'] += 1
                except Exception as e:
                    logger.error(f"Erro ao migrar cidadão {migration_data.get('cpf')}: {str(e)}")
                    self.results['errors'] += 1
            
            return True
            
        except Exception as e:
            logger.error(f"Falha na migração de cidadãos: {str(e)}", exc_info=True)
            return False
    
    def migrate_users(self) -> bool:
        """Migra a tabela de usuários"""
        logger.info("🔄 Migrando usuários...")
        
        try:
            source_cur = self.db.source_conn.cursor()
            target_cur = self.db.target_conn.cursor()
            
            # Obter dados dos usuários
            source_cur.execute("SELECT * FROM users")
            users = source_cur.fetchall()
            source_cols = [col[0] for col in source_cur.description]
            
            for user in users:
                self.results['total'] += 1
                user_data = dict(zip(source_cols, user))
                
                # Preparar dados para migração
                migration_data = {
                    'id': user_data.get('id'),
                    'email': user_data.get('email'),
                    'name': user_data.get('name', 'Usuário sem nome'),
                    'is_active': user_data.get('is_active', True),
                    'created_at': user_data.get('created_at', datetime.now().isoformat()),
                    'updated_at': user_data.get('updated_at', datetime.now().isoformat()),
                    'password_hash': Security.create_password_hash(Config.DEFAULT_PASSWORD)
                }
                
                # Se for dry run, apenas loga
                if self.dry_run:
                    logger.info(f"[DRY RUN] Migraria usuário: {migration_data['email']}")
                    self.results['success'] += 1
                    continue
                
                # Tenta inserir o usuário
                try:
                    columns = ', '.join([f'"{k}"' for k in migration_data.keys()])
                    placeholders = ', '.join(['%s'] * len(migration_data))
                    query = f'INSERT INTO users ({columns}) VALUES ({placeholders}) ON CONFLICT (id) DO NOTHING'
                    
                    target_cur.execute(query, list(migration_data.values()))
                    if target_cur.rowcount > 0:
                        self.results['success'] += 1
                        # Preparar notificação
                        self.notifications.append({
                            'email': migration_data['email'],
                            'name': migration_data['name'],
                            'token': Security.generate_reset_token()
                        })
                    else:
                        logger.warning(f"Usuário já existe: {migration_data.get('email')}")
                        self.results['skipped'] += 1
                        
                except psycopg2.IntegrityError as e:
                    if "duplicate key value violates unique constraint" in str(e):
                        logger.warning(f"Usuário já existe: {migration_data.get('email')}")
                        self.results['skipped'] += 1
                    else:
                        logger.error(f"Erro ao migrar usuário {migration_data.get('email')}: {str(e)}")
                        self.results['errors'] += 1
                except Exception as e:
                    logger.error(f"Erro ao migrar usuário {migration_data.get('email')}: {str(e)}")
                    self.results['errors'] += 1
            
            return True
            
        except Exception as e:
            logger.error(f"Falha na migração de usuários: {str(e)}", exc_info=True)
            return False
    
    def migrate_complaints(self) -> bool:
        """Migra a tabela de reclamações"""
        logger.info("🔄 Migrando reclamações...")
        
        try:
            source_cur = self.db.source_conn.cursor()
            target_cur = self.db.target_conn.cursor()
            
            # Obter dados das reclamações
            source_cur.execute("SELECT * FROM complaints")
            complaints = source_cur.fetchall()
            source_cols = [col[0] for col in source_cur.description]
            
            for complaint in complaints:
                self.results['total'] += 1
                complaint_data = dict(zip(source_cols, complaint))
                
                # Preparar dados para migração
                migration_data = {
                    'id': complaint_data.get('id'),
                    'title': complaint_data.get('title', 'Reclamação sem título'),
                    'description': complaint_data.get('description', ''),
                    'status': complaint_data.get('status', 'pendente'),
                    'priority': complaint_data.get('priority', 'media'),
                    'category': complaint_data.get('category', 'geral'),
                    'citizen_id': complaint_data.get('citizen_id'),
                    'assigned_to': complaint_data.get('assigned_to'),
                    'created_at': complaint_data.get('created_at', datetime.now().isoformat()),
                    'updated_at': complaint_data.get('updated_at', datetime.now().isoformat()),
                    'resolved_at': complaint_data.get('resolved_at')
                }
                
                # Se for dry run, apenas loga
                if self.dry_run:
                    logger.info(f"[DRY RUN] Migraria reclamação: {migration_data['title']}")
                    self.results['success'] += 1
                    continue
                
                # Tenta inserir a reclamação
                try:
                    columns = ', '.join([f'"{k}"' for k in migration_data.keys()])
                    placeholders = ', '.join(['%s'] * len(migration_data))
                    query = f'INSERT INTO complaints ({columns}) VALUES ({placeholders}) ON CONFLICT (id) DO NOTHING'
                    
                    target_cur.execute(query, list(migration_data.values()))
                    if target_cur.rowcount > 0:
                        self.results['success'] += 1
                    else:
                        logger.warning(f"Reclamação já existe: {migration_data.get('id')}")
                        self.results['skipped'] += 1
                        
                except psycopg2.IntegrityError as e:
                    if "duplicate key value violates unique constraint" in str(e):
                        logger.warning(f"Reclamação já existe: {migration_data.get('id')}")
                        self.results['skipped'] += 1
                    else:
                        logger.error(f"Erro ao migrar reclamação {migration_data.get('id')}: {str(e)}")
                        self.results['errors'] += 1
                except Exception as e:
                    logger.error(f"Erro ao migrar reclamação {migration_data.get('id')}: {str(e)}")
                    self.results['errors'] += 1
            
            return True
            
        except Exception as e:
            logger.error(f"Falha na migração de reclamações: {str(e)}", exc_info=True)
            return False
    
    def send_notifications(self):
        """Envia notificações para usuários migrados"""
        if self.dry_run:
            logger.info(f"[DRY RUN] Enviaria {len(self.notifications)} notificações")
            return
        
        logger.info(f"📧 Enviando {len(self.notifications)} notificações...")
        
        try:
            for notification in self.notifications:
                # Aqui você pode implementar o envio real de emails
                logger.info(f"📧 Notificação preparada para {notification['email']} (token: {notification['token'][:10]}...)")
                
                # Exemplo de envio de email (descomente e configure para uso real)
                # self._send_email_notification(notification)
                
        except Exception as e:
            logger.error(f"Erro ao enviar notificações: {str(e)}")
    
    def _send_email_notification(self, notification: Dict[str, str]):
        """Envia notificação por email (implementação de exemplo)"""
        try:
            msg = MIMEMultipart()
            msg['From'] = Config.NOTIFICATION_FROM
            msg['To'] = notification['email']
            msg['Subject'] = Config.NOTIFICATION_SUBJECT
            
            # Criar link de redefinição (ajuste conforme sua implementação)
            reset_link = f"https://seusistema.com/reset-password?token={notification['token']}"
            
            body = Config.NOTIFICATION_TEMPLATE.format(
                name=notification['name'],
                reset_link=reset_link
            )
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Conectar ao servidor SMTP e enviar
            # server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            # server.starttls()
            # server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            # server.send_message(msg)
            # server.quit()
            
            logger.info(f"📧 Email enviado para {notification['email']}")
            
        except Exception as e:
            logger.error(f"Erro ao enviar email para {notification['email']}: {str(e)}")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Migração de dados do sila_dev para PostgreSQL')
    parser.add_argument('--dry-run', action='store_true', help='Executa a migração em modo de teste')
    parser.add_argument('--only-users', action='store_true', help='Migra apenas usuários')
    parser.add_argument('--only-citizens', action='store_true', help='Migra apenas cidadãos')
    parser.add_argument('--only-complaints', action='store_true', help='Migra apenas reclamações')
    
    args = parser.parse_args()
    
    logger.info("🚀 Iniciando migração do sila_dev para PostgreSQL")
    if args.dry_run:
        logger.info("🔍 Modo DRY RUN - nenhuma alteração será feita")
    
    try:
        # Configurações do banco de dados
        db_config = {
            'DB_HOST': Config.DB_HOST,
            'DB_PORT': Config.DB_PORT,
            'DB_NAME': Config.DB_NAME,
            'DB_USER': Config.DB_USER,
            'DB_PASSWORD': Config.DB_PASSWORD
        }
        
        with DatabaseManager(db_config) as db:
            migration = MigrationManager(db, args.dry_run)
            
            # Determinar quais tabelas migrar
            migrate_users = not args.only_citizens and not args.only_complaints
            migrate_citizens = not args.only_users and not args.only_complaints
            migrate_complaints = not args.only_users and not args.only_citizens
            
            # Executar migrações
            success = True
            
            if migrate_citizens:
                success &= migration.migrate_citizens()
            
            if migrate_users:
                success &= migration.migrate_users()
            
            if migrate_complaints:
                success &= migration.migrate_complaints()
            
            # Enviar notificações
            if migrate_users and success:
                migration.send_notifications()
            
            # Relatório final
            logger.info("📊 Relatório de migração:")
            logger.info(f"   Total: {migration.results['total']}")
            logger.info(f"   Sucesso: {migration.results['success']}")
            logger.info(f"   Pulados: {migration.results['skipped']}")
            logger.info(f"   Erros: {migration.results['errors']}")
            
            if success:
                logger.info("✅ Migração concluída com sucesso!")
                return 0
            else:
                logger.error("❌ Migração concluída com erros!")
                return 1
                
    except Exception as e:
        logger.error(f"Erro fatal durante a migração: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())