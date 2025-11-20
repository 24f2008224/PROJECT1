import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from hms_app import create_app, db
from hms_app.models import User, Department, Doctor, Patient, Appointment, Treatment

app = create_app()

def setup_db():
    with app.app_context():
        db.create_all()
        print("Database tables created.")

        # Create default admin if not exists
        if not User.query.filter_by(username='admin').first():
            from werkzeug.security import generate_password_hash
            admin = User(username='admin', email='admin@hms.com',
                         password_hash=generate_password_hash('admin123'), role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Default admin created.")

        # Create some departments
        if not Department.query.first():
            deps = ['Cardiology', 'Neurology', 'Orthopedics', 'General']
            for d in deps:
                db.session.add(Department(name=d))
            db.session.commit()
            print("Default departments created.")

if __name__ == '__main__':
    setup_db()
