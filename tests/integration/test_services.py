"""
Integration tests for service management endpoints.

This module contains tests for service-related operations such as
creating, retrieving, updating, and managing services.
"""
import pytest
from fastapi import status
from typing import Dict, List, Any

class TestServices:
    """Test cases for service management endpoints."""
    
    def test_create_service(self, client, auth_headers, service_factory):
        ""Test creating a new service with valid data."""
        # Arrange
        service_data = service_factory.build_dict()
        
        # Act
        response = client.post(
            "/api/v1/services/",
            headers=auth_headers,
            json=service_data
        )
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["code"] == service_data["code"]
        assert data["name"] == service_data["name"]
        assert data["status"] == "draft"  # Default status
        assert "id" in data
        assert "created_at" in data
    
    def test_create_service_duplicate_code(self, client, auth_headers, service_factory):
        ""Test creating a service with a duplicate code fails."""
        # Arrange - create first service
        service1 = service_factory.build()
        client.post("/api/v1/services/", headers=auth_headers, json=service1.dict())
        
        # Create second service with same code
        service2 = service_factory.build(code=service1.code)
        
        # Act
        response = client.post(
            "/api/v1/services/",
            headers=auth_headers,
            json=service2.dict()
        )
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "code" in response.text.lower()
        assert "already exists" in response.text.lower()
    
    def test_get_service(self, client, auth_headers, service_factory):
        ""Test retrieving a service by ID."""
        # Arrange - create a service
        service_data = service_factory.build_dict()
        create_response = client.post(
            "/api/v1/services/",
            headers=auth_headers,
            json=service_data
        )
        service_id = create_response.json()["id"]
        
        # Act
        response = client.get(
            f"/api/v1/services/{service_id}",
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == service_id
        assert data["code"] == service_data["code"]
        assert data["name"] == service_data["name"]
    
    def test_list_services(self, client, auth_headers, service_factory):
        ""Test listing services with pagination and filtering."""
        # Arrange - create test services
        services = []
        for status in ["draft", "active", "inactive"]:
            service = service_factory.build(status=status)
            response = client.post(
                "/api/v1/services/",
                headers=auth_headers,
                json=service.dict()
            )
            services.append(response.json())
        
        # Act - get active services
        response = client.get(
            "/api/v1/services/",
            headers=auth_headers,
            params={"status": "active"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert all(s["status"] == "active" for s in data["items"])
    
    def test_update_service(self, client, auth_headers, service_factory):
        ""Test updating a service."""
        # Arrange - create a service
        service = service_factory.build()
        create_response = client.post(
            "/api/v1/services/",
            headers=auth_headers,
            json=service.dict()
        )
        service_id = create_response.json()["id"]
        
        # Update data
        update_data = {
            "name": "Updated Service Name",
            "description": "Updated description",
            "status": "under_review",
            "metadata": {"key": "value"}
        }
        
        # Act
        response = client.patch(
            f"/api/v1/services/{service_id}",
            headers=auth_headers,
            json=update_data
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
        assert data["status"] == update_data["status"]
        assert data["metadata"] == update_data["metadata"]
    
    def test_delete_service(self, client, auth_headers, service_factory):
        ""Test deleting a service."""
        # Arrange - create a service
        service = service_factory.build()
        create_response = client.post(
            "/api/v1/services/",
            headers=auth_headers,
            json=service.dict()
        )
        service_id = create_response.json()["id"]
        
        # Act - delete the service
        response = client.delete(
            f"/api/v1/services/{service_id}",
            headers=auth_headers
        )
        
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify service no longer exists
        get_response = client.get(
            f"/api/v1/services/{service_id}",
            headers=auth_headers
        )
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_service_workflow(self, client, auth_headers, service_factory):
        ""Test service status workflow transitions."""
        # Create service in draft status
        service = service_factory.build(status="draft")
        create_response = client.post(
            "/api/v1/services/",
            headers=auth_headers,
            json=service.dict()
        )
        service_id = create_response.json()["id"]
        
        # Test transition to under_review
        response = client.patch(
            f"/api/v1/services/{service_id}",
            headers=auth_headers,
            json={"status": "under_review"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "under_review"
        
        # Test transition to active (requires admin)
        admin_headers = client.post("/api/v1/auth/login", data={
            "username": "admin@example.com",
            "password": "adminpassword"
        }).json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_headers}"}
        
        response = client.patch(
            f"/api/v1/services/{service_id}",
            headers=admin_headers,
            json={"status": "active"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "active"
        
        # Test invalid transition (active -> draft)
        response = client.patch(
            f"/api/v1/services/{service_id}",
            headers=auth_headers,
            json={"status": "draft"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "invalid status transition" in response.text.lower()
    
    def test_service_categories(self, client, auth_headers, service_factory):
        ""Test managing service categories."""
        # Create services in different categories
        categories = ["construction", "environment", "business"]
        for category in categories:
            service = service_factory.build(category=category)
            client.post(
                "/api/v1/services/",
                headers=auth_headers,
                json=service.dict()
            )
        
        # Get services by category
        response = client.get(
            "/api/v1/services/",
            headers=auth_headers,
            params={"category": "environment"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(s["category"] == "environment" for s in data["items"])
    
    def test_service_search(self, client, auth_headers, service_factory):
        ""Test searching services by name or code."""
        # Create test services
        services = [
            {"name": "Building Permit", "code": "BP-001"},
            {"name": "Environmental License", "code": "EL-001"},
            {"name": "Business Registration", "code": "BR-001"}
        ]
        
        for service in services:
            service_factory.create(**service)
        
        # Test search by name
        response = client.get(
            "/api/v1/services/search",
            headers=auth_headers,
            params={"query": "Building"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) >= 1
        assert "Building" in data["items"][0]["name"]
        
        # Test search by code
        response = client.get(
            "/api/v1/services/search",
            headers=auth_headers,
            params={"query": "EL-001"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["items"]) >= 1
        assert data["items"][0]["code"] == "EL-001"
