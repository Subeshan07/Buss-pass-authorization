from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError
from models import Student

class StudentRegistrationForm(FlaskForm):
    reg_no = StringField('Registration Number', validators=[
        DataRequired(),
        Length(min=5, max=20),
        Regexp('^[A-Za-z0-9]+$', message="Registration number must contain only letters and numbers")
    ])
    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    department = SelectField('Department', choices=[
        ('CSE', 'Computer Science Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('IT', 'Information Technology'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    year = SelectField('Year', choices=[
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year')
    ], validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, max=20)
    ])
    submit = SubmitField('Register & Generate Pass')
    
    def validate_reg_no(self, reg_no):
        student = Student.query.filter_by(reg_no=reg_no.data).first()
        if student:
            raise ValidationError('Registration number already exists. Please choose a different one.')

class StudentLoginForm(FlaskForm):
    reg_no = StringField('Registration Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AdminRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=80),
        Regexp('^[A-Za-z0-9_]+$', message="Username must contain only letters, numbers, and underscores")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=20)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired()
    ])
    admin_code = StringField('Admin Registration Code', validators=[
        DataRequired(),
        Length(min=6, max=20)
    ])
    submit = SubmitField('Register as Admin')
    
    def validate_username(self, username):
        from models import Admin
        admin = Admin.query.filter_by(username=username.data).first()
        if admin:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError('Passwords do not match.')
    
    def validate_admin_code(self, admin_code):
        # Secret admin registration code - change this in production
        if admin_code.data != 'ADMIN2025':
            raise ValidationError('Invalid admin registration code.')
class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')