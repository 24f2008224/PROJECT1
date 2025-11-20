from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from hms_app import db
from hms_app.admin import admin_bp
from hms_app.models import User, Doctor, Patient, Appointment, Department
from hms_app.decorators import admin_required
from werkzeug.security import generate_password_hash

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    doctor_count = Doctor.query.count()
    patient_count = Patient.query.count()
    appointment_count = Appointment.query.count()
    departments = Department.query.all()
    doctors = Doctor.query.all()
    patients = Patient.query.all()
    appointments = Appointment.query.all()

    return render_template('admin/dashboard.html',
                           doctor_count=doctor_count,
                           patient_count=patient_count,
                           appointment_count=appointment_count,
                           departments=departments,
                           doctors=doctors,
                           patients=patients,
                           appointments=appointments)

@admin_bp.route('/search', methods=['POST'])
@login_required
@admin_required
def search():
    doctor_query = request.form.get('doctor_query')
    patient_query = request.form.get('patient_query')

    doctors = Doctor.query.all()
    if doctor_query:
        doctors = Doctor.query.join(User).filter(User.username.contains(doctor_query) | Doctor.specialization.contains(doctor_query)).all()

    patients = Patient.query.all() # We need to pass patients to template now to search/list them
    # But previously dashboard didn't list patients. Let's fetch them.
    if patient_query:
        patients = Patient.query.join(User).filter(User.username.contains(patient_query) | Patient.contact_info.contains(patient_query)).all()
    elif not patient_query and not doctor_query:
        # If just loading dashboard normally we might not want all patients if huge, but for now ok.
        pass

    doctor_count = Doctor.query.count()
    patient_count = Patient.query.count()
    appointment_count = Appointment.query.count()
    departments = Department.query.all()
    appointments = Appointment.query.all()

    return render_template('admin/dashboard.html',
                           doctor_count=doctor_count,
                           patient_count=patient_count,
                           appointment_count=appointment_count,
                           departments=departments,
                           doctors=doctors,
                           patients=patients,
                           appointments=appointments)

@admin_bp.route('/add_doctor', methods=['POST'])
@login_required
@admin_required
def add_doctor():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    department_id = request.form.get('department_id')
    specialization = request.form.get('specialization')

    if User.query.filter_by(username=username).first():
        flash('Username already exists', 'danger')
        return redirect(url_for('admin.dashboard'))

    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password_hash=hashed_password, role='doctor')
    db.session.add(user)
    db.session.commit()

    doctor = Doctor(user_id=user.id, department_id=department_id, specialization=specialization)
    db.session.add(doctor)
    db.session.commit()

    flash('Doctor added successfully', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/update_doctor/<int:doctor_id>', methods=['POST'])
@login_required
@admin_required
def update_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    specialization = request.form.get('specialization')
    # Only updating specialization for simplicity, can add more fields
    doctor.specialization = specialization
    db.session.commit()
    flash('Doctor updated successfully', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot delete admin', 'danger')
        return redirect(url_for('admin.dashboard'))

    # Cascading delete should be handled by DB or manually if no cascade set
    # Here manual cleanup for safety
    if user.role == 'doctor':
        doctor = Doctor.query.filter_by(user_id=user.id).first()
        if doctor:
            # Appointments? For now let's say we keep them or delete them
            # Ideally we should soft delete or blacklist.
            # Requirement says "Blacklist/remove".
            db.session.delete(doctor)
    elif user.role == 'patient':
        patient = Patient.query.filter_by(user_id=user.id).first()
        if patient:
            db.session.delete(patient)

    db.session.delete(user)
    db.session.commit()
    flash('User removed successfully', 'success')
    return redirect(url_for('admin.dashboard'))
