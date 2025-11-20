from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from hms_app import db
from hms_app.doctor import doctor_bp
from hms_app.models import Appointment, Treatment
from hms_app.decorators import doctor_required

@doctor_bp.route('/dashboard')
@login_required
@doctor_required
def dashboard():
    doctor = current_user.doctor
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    return render_template('doctor/dashboard.html', appointments=appointments, doctor=doctor)

@doctor_bp.route('/update_availability', methods=['POST'])
@login_required
@doctor_required
def update_availability():
    availability = request.form.get('availability')
    current_user.doctor.availability = availability
    db.session.commit()
    flash('Availability updated successfully', 'success')
    return redirect(url_for('doctor.dashboard'))

@doctor_bp.route('/appointment/<int:appt_id>', methods=['GET', 'POST'])
@login_required
@doctor_required
def manage_appointment(appt_id):
    appointment = Appointment.query.get_or_404(appt_id)
    if appointment.doctor_id != current_user.doctor.id:
        flash('You cannot manage this appointment', 'danger')
        return redirect(url_for('doctor.dashboard'))

    if request.method == 'POST':
        status = request.form.get('status')
        diagnosis = request.form.get('diagnosis')
        prescription = request.form.get('prescription')
        description = request.form.get('description')

        appointment.status = status

        treatment = Treatment.query.filter_by(appointment_id=appointment.id).first()
        if not treatment:
            treatment = Treatment(appointment_id=appointment.id, diagnosis=diagnosis,
                                  prescription=prescription, description=description)
            db.session.add(treatment)
        else:
            treatment.diagnosis = diagnosis
            treatment.prescription = prescription
            treatment.description = description

        db.session.commit()
        flash('Appointment updated', 'success')
        return redirect(url_for('doctor.dashboard'))

    return render_template('doctor/manage_appointment.html', appointment=appointment)
