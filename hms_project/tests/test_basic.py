import pytest
from hms_app import create_app, db
from hms_app.models import User, Department

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for testing

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Hospital Management System" in rv.data

def test_register(client):
    rv = client.post('/auth/register', data=dict(
        username='testuser',
        email='test@test.com',
        password='password',
        confirm_password='password',
        contact_info='1234567890'
    ), follow_redirects=True)
    assert rv.status_code == 200
    assert b"Your account has been created" in rv.data

    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.role == 'patient'

def test_admin_login(client):
    # Create admin
    from werkzeug.security import generate_password_hash
    admin = User(username='admin', email='admin@hms.com',
                 password_hash=generate_password_hash('admin123'), role='admin')
    db.session.add(admin)
    db.session.commit()

    rv = client.post('/auth/login', data=dict(
        username='admin',
        password='admin123'
    ), follow_redirects=True)
    assert rv.status_code == 200
    # Redirects to admin dashboard
    assert b"Admin Dashboard" in rv.data

def test_departments_exist(client):
     # Setup DB should have created departments if we ran the script,
     # but in test fixture we start empty.
     # So we can test manual creation.
     dep = Department(name='Test Dep')
     db.session.add(dep)
     db.session.commit()
     assert Department.query.count() == 1
