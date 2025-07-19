from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import qrcode
import json
import os
from datetime import datetime
import ssl

from config import config
from models import db, Student, Admin
from forms import StudentRegistrationForm, StudentLoginForm, AdminLoginForm, AdminRegistrationForm

app = Flask(__name__)

# Load configuration based on environment
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_choice'

@login_manager.user_loader
def load_user(user_id):
    if user_id.startswith('admin_'):
        admin_id = int(user_id.split('_')[1])
        return Admin.query.get(admin_id)
    else:
        return Student.query.get(int(user_id))

def generate_qr_code(student_data):
    """Generate QR code for student pass"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr_data = {
        'reg_no': student_data['reg_no'],
        'name': student_data['name'],
        'department': student_data['department'],
        'year': student_data['year'],
        'timestamp': datetime.now().isoformat()
    }
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save QR code
    qr_filename = f"{student_data['reg_no']}_pass.png"
    qr_path = os.path.join(app.config['UPLOAD_FOLDER'], qr_filename)
    img.save(qr_path)
    
    return qr_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_choice')
def login_choice():
    return render_template('login_choice.html')

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    form = StudentLoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(reg_no=form.reg_no.data).first()
        if student and student.check_password(form.password.data):
            login_user(student)
            return redirect(url_for('student_dashboard'))
        flash('Invalid registration number or password', 'error')
    return render_template('student_login.html', form=form)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('admin_login.html', form=form)

@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        admin = Admin(username=form.username.data)
        admin.set_password(form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash('Admin registration successful! You can now login.', 'success')
        return redirect(url_for('admin_login'))
    return render_template('admin_register.html', form=form)
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        # Check if registration number already exists
        existing_student = Student.query.filter_by(reg_no=form.reg_no.data).first()
        if existing_student:
            flash('Registration number already exists!', 'error')
            return render_template('register.html', form=form)
        
        student = Student(
            reg_no=form.reg_no.data,
            name=form.name.data,
            department=form.department.data,
            year=form.year.data
        )
        student.set_password(form.password.data)
        
        # Generate QR code
        qr_filename = generate_qr_code({
            'reg_no': student.reg_no,
            'name': student.name,
            'department': student.department,
            'year': student.year
        })
        student.qr_code_path = qr_filename
        
        db.session.add(student)
        db.session.commit()
        
        flash('Registration successful! Your bus pass has been generated.', 'success')
        return render_template('pass_generated.html', student=student)
    
    return render_template('register.html', form=form)

@app.route('/student_dashboard')
@login_required
def student_dashboard():
    if isinstance(current_user, Admin):
        return redirect(url_for('admin_dashboard'))
    return render_template('student_dashboard.html', student=current_user)

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not isinstance(current_user, Admin):
        flash('Access denied! Admin access only.', 'error')
        return redirect(url_for('student_dashboard'))
    
    students = Student.query.all()
    return render_template('admin_dashboard.html', students=students)

@app.route('/scan')
def scan():
    return render_template('scan.html')

@app.route('/verify', methods=['POST'])
def verify():
    try:
        qr_data = request.json.get('qr_data')
        if not qr_data:
            return jsonify({'status': 'error', 'message': 'No QR data provided'})
        
        # Parse QR code data
        student_data = json.loads(qr_data)
        reg_no = student_data.get('reg_no')
        
        # Verify student in database
        student = Student.query.filter_by(reg_no=reg_no).first()
        
        if student and student.is_active:
            return jsonify({
                'status': 'valid',
                'student': {
                    'reg_no': student.reg_no,
                    'name': student.name,
                    'department': student.department,
                    'year': student.year
                }
            })
        elif student and not student.is_active:
            return jsonify({
                'status': 'blocked',
                'message': 'This pass has been revoked or blocked'
            })
        else:
            return jsonify({
                'status': 'invalid',
                'message': 'Invalid or fake pass detected'
            })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Invalid QR code format'})

@app.route('/revoke_pass/<int:student_id>')
@login_required
def revoke_pass(student_id):
    if not isinstance(current_user, Admin):
        flash('Access denied! Admin access only.', 'error')
        return redirect(url_for('student_dashboard'))
    
    student = Student.query.get_or_404(student_id)
    student.is_active = False
    db.session.commit()
    flash(f'Pass revoked for {student.name}', 'warning')
    return redirect(url_for('admin_dashboard'))

@app.route('/activate_pass/<int:student_id>')
@login_required
def activate_pass(student_id):
    if not isinstance(current_user, Admin):
        flash('Access denied! Admin access only.', 'error')
        return redirect(url_for('student_dashboard'))
    
    student = Student.query.get_or_404(student_id)
    student.is_active = True
    db.session.commit()
    flash(f'Pass activated for {student.name}', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("Please ensure:")
            print("1. MySQL server is running")
            print("2. Database 'buspass_db' exists")
            print("3. MySQL credentials are correct")
            print("4. Run 'python create_database.py' first")
            exit(1)
        
        # Create QR codes directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # For development with HTTPS
    # In production, use proper SSL certificates
    #context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    #context.load_cert_chain('cert.pem', 'key.pem')
    
    try:
        # Try to run with HTTPS (comment out for basic development)
        # app.run(debug=True, host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
        
        # For development without SSL (comment out the above line and uncomment this)
        app.run(debug=True, host='0.0.0.0', port=5000)
    except FileNotFoundError:
        print("SSL certificates not found. Running without HTTPS for development.")
        print("For production, generate SSL certificates using:")
        print("openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365")
        app.run(debug=True, host='0.0.0.0', port=5000)