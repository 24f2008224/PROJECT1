import os
import pytest
from student_app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_handle_request_success(client):
    """Test the API endpoint with a valid request."""
    response = client.post('/api-endpoint', json={
        'secret': 'your_secret_here',
        'brief': 'Create a simple webpage.',
        'task': 'test-repo',
        'evaluation_url': 'https://httpbin.org/post'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Request received successfully'
    assert os.path.exists('student_app/generated_app/index.html')

def test_handle_request_unauthorized(client):
    """Test the API endpoint with an invalid secret."""
    response = client.post('/api-endpoint', json={'secret': 'wrong_secret'})
    assert response.status_code == 401
    assert response.json['error'] == 'Unauthorized'
