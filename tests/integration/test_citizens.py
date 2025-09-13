"""
Integration tests for citizen management endpoints.

This module contains tests for citizen-related operations such as
creating, retrieving, updating, and deleting citizen records.
"""
import pytest
from fastapi import status
from typing import Dict, Any

class TestCitizens:
    """Test cases for citizen management endpoints."""
    
    def test_create_citizen(self, client, auth_headers, citizen_factory):
        ""Test creating a new citizen record."""
        # Arrange
        citizen_data = citizen_factory.build_dict()
        
        # Act
        response = client.post(
            "/api/v1/citizens/",
            headers=auth_headers,
            json=citizen_data
        )
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["cpf"] == citizen_data["cpf"]
        assert data["full_name"] == citizen_data["full_name"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_duplicate_cpf(self, client, auth_headers, citizen_factory):
        ""Test creating a citizen with a duplicate CPF fails."""
        # Arrange - create first citizen
        citizen1 = citizen_factory.build()
        client.post("/api/v1/citizens/", headers=auth_headers, json=citizen1.dict())
        
        # Create second citizen with same CPF
        citizen2 = citizen_factory.build(cpf=citizen1.cpf)
        
        # Act
        response = client.post(
            "/api/v1/citizens/",
            headers=auth_headers,
            json=citizen2.dict()
        )
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "cpf" in response.text.lower()
        assert "already exists" in response.text.lower()
    
    def test_get_citizen(self, client, auth_headers, citizen_factory):
        ""Test retrieving a citizen by ID."""
        # Arrange - create a citizen
        citizen_data = citizen_factory.build_dict()
        create_response = client.post(
            "/api/v1/citizens/",
            headers=auth_headers,
            json=citizen_data
        )
        citizen_id = create_response.json()["id"]
        
        # Act
        response = client.get(
            f"/api/v1/citizens/{citizen_id}",
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == citizen_id
        assert data["cpf"] == citizen_data["cpf"]
    
    def test_list_citizens(self, client, auth_headers, citizen_factory):
        ""Test listing citizens with pagination and filtering."""
        # Arrange - create test citizens
        citizens = []
        for _ in range(5):
            citizen = citizen_factory.build()
            response = client.post(
                "/api/v1/citizens/",
                headers=auth_headers,
                json=citizen.dict()
            )
            citizens.append(response.json())
        
        # Act - get first page
        response = client.get(
            "/api/v1/citizens/",
            headers=auth_headers,
            params={"skip": 0, "limit": 2}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert len(data["items"]) == 2
        assert data["total"] >= 5
    
    def test_update_citizen(self, client, auth_headers, citizen_factory):
        ""Test updating a citizen record."""
        # Arrange - create a citizen
        citizen = citizen_factory.build()
        create_response = client.post(
            "/api/v1/citizens/",
            headers=auth_headers,
            json=citizen.dict()
        )
        citizen_id = create_response.json()["id"]
        
        # Update data
        update_data = {
            "full_name": "Updated Name",
            "phone_number": "+5511999999999",
            "address_street": "New Street Name",
            "address_number": "123"
        }
        
        # Act
        response = client.patch(
            f"/api/v1/citizens/{citizen_id}",
            headers=auth_headers,
            json=update_data
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
        assert data["phone_number"] == update_data["phone_number"]
        assert data["address_street"] == update_data["address_street"]
        assert data["address_number"] == update_data["address_number"]
    
    def test_delete_citizen(self, client, auth_headers, citizen_factory):
        ""Test deleting a citizen record."""
        # Arrange - create a citizen
        citizen = citizen_factory.build()
        create_response = client.post(
            "/api/v1/citizens/",
            headers=auth_headers,
            json=citizen.dict()
        )
        citizen_id = create_response.json()["id"]
        
        # Act - delete the citizen
        response = client.delete(
            f"/api/v1/citizens/{citizen_id}",
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify citizen no longer exists
        get_response = client.get(
            f"/api/v1/citizens/{citizen_id}",
            headers=auth_headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_search_citizens(self, client, auth_headers, citizen_factory):
        ""Test searching citizens by name or CPF."""
        # Arrange - create test citizens
        citizen1 = citizen_factory.build(full_name="João da Silva", cpf="12345678901")
        citizen2 = citizen_factory.build(full_name="Maria Oliveira", cpf="10987654321")
        
        client.post("/api/v1/citizens/", headers=auth_headers, json=citizen1.dict())
        client.post("/api/v1/citizens/", headers=auth_headers, json=citizen2.dict())
        
        # Test search by name
        response = client.get(
            "/api/v1/citizens/search",
            headers=auth_headers,
            params={"query": "João"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) >= 1
        assert any(c["full_name"] == "João da Silva" for c in data["items"])
        
        # Test search by CPF
        response = client.get(
            "/api/v1/citizens/search",
            headers=auth_headers,
            params={"query": "10987654321"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) >= 1
        assert any(c["cpf"] == "10987654321" for c in data["items"])
    
    def test_export_citizens(self, client, auth_headers, citizen_factory):
        ""Test exporting citizens to CSV."""
        # Arrange - create test citizens
        for _ in range(3):
            citizen = citizen_factory.build()
            client.post("/api/v1/citizens/", headers=auth_headers, json=citizen.dict())
        
        # Act
        response = client.get(
            "/api/v1/citizens/export",
            headers=auth_headers,
            params={"format": "csv"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        content_disposition = response.headers["content-disposition"]
        assert "citizens_export" in content_disposition
        assert ".csv" in content_disposition
        
        # Check CSV content
        csv_content = response.text
        lines = csv_content.strip().split("\n")
        assert len(lines) >= 4  # header + 3 citizens + possible others
