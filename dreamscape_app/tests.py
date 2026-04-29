import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_registration(api_client):
    response = api_client.post('/register/', {
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'testpass123',
        'password_confirm': 'testpass123'
    })
    assert response.status_code == 201

@pytest.mark.django_db
def test_registration_with_wrong_password(api_client):
    response = api_client.post('/register/', {
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'testpass123',
        'password_confirm': 'wrongpass'
    })
    assert response.status_code == 400

@pytest.mark.django_db
def test_api_token(api_client):
    api_client.post('/register/', {
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'testpass123',
        'password_confirm': 'testpass123'
    })
    response = api_client.post('/api/token/', {
        'username': 'testuser',
        'password': 'testpass123'
    })
    assert response.status_code == 200

@pytest.mark.django_db
def test_wish_get_without_token(api_client):
    response = api_client.get('/wishes/', {
        'title': 'Побывать в Исландии',
        'is_done': True,
        'category_id': 4
    })
    assert response.status_code == 401