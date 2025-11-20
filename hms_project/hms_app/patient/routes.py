from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from hms_app import db
from hms_app.patient import patient_bp
from hms_app.models import Appointment, Doctor
from hms_app.decorators import patient_required
from datetime import datetime

@patient_bp.route('/dashboard')
@login_required
@patient_required
def dashboard():
    patient = current_user.patient
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    return render_template('patient/dashboard.html', appointments=appointments)

@patient_bp.route('/book_appointment', methods=['GET', 'POST'])
@login_required
@patient_required
def book_appointment():
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        date_time_str = request.form.get('date_time')
        symptoms = request.form.get('symptoms')

        try:
            date_time = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid date format', 'danger')
            return redirect(url_for('patient.book_appointment'))

        appt = Appointment(doctor_id=doctor_id, patient_id=current_user.patient.id,
                           date_time=date_time, symptoms=symptoms)
        db.session.add(appt)
        db.session.commit()

        flash('Appointment booked successfully', 'success')
        return redirect(url_for('patient.dashboard'))

    doctors = Doctor.query.all()
    return render_template('patient/book_appointment.html', doctors=doctors)
