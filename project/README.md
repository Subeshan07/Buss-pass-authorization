# College Bus Pass Authenticator System

A secure, professional-grade web application for managing digital bus passes in educational institutions. Built with Flask (Python) backend and modern web technologies.

## 🌟 Features

### 👤 Student Features
- **Secure Registration**: Register with unique registration number, name, department, and year
- **Digital Bus Pass**: Automatic QR code generation for each student
- **Personal Dashboard**: View pass status, download QR code, and manage account
- **Mobile Optimized**: Responsive design works perfectly on all devices

### 🔍 Conductor Features
- **QR Code Scanner**: Real-time camera-based scanning using device camera
- **Instant Verification**: Immediate validation against database
- **Status Feedback**: Clear visual indicators for valid, invalid, or blocked passes
- **Offline Capability**: Works even with intermittent connectivity

### 🛡️ Admin Features
- **Student Management**: View all registered students and their status
- **Pass Control**: Activate or revoke student passes instantly
- **Search & Filter**: Find students quickly with advanced search
- **Analytics Dashboard**: Overview of total students, active passes, and system usage

### 🔐 Security Features
- **HTTPS Encryption**: All communications secured with SSL/TLS
- **Separate Authentication**: Distinct login systems for students and admins
- **Password Security**: Bcrypt hashing for all passwords
- **SQL Injection Protection**: Parameterized queries and SQLAlchemy ORM
- **Session Management**: Secure session handling with timeout

## 🛠️ Technology Stack

- **Backend**: Flask (Python 3.7+)
- **Database**: MySQL with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **QR Generation**: Python `qrcode` library
- **QR Scanning**: `html5-qrcode` JavaScript library
- **Security**: Flask-Login, Werkzeug password hashing
- **Styling**: Custom CSS with responsive design

## 📋 Prerequisites

- Python 3.7 or higher
- MySQL Server 5.7 or higher
- OpenSSL (for SSL certificate generation)
- Modern web browser with camera support

## 🚀 Quick Setup

### Option 1: Automated Setup (Recommended)
```bash
# Clone or download the project
cd buspass-authenticator

# Run the complete setup script
python run_setup.py
```

### Option 2: Manual Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Database**
   ```bash
   python create_database.py
   ```

3. **Generate SSL Certificates**
   ```bash
   python setup_ssl.py
   ```

4. **Configure Database** (if needed)
   Edit `config.py` and update MySQL credentials:
   ```python
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/buspass_db'
   ```

5. **Start Application**
   ```bash
   python app.py
   ```

6. **Access Application**
   Open https://localhost:5000 in your browser

## 🔑 Default Credentials

### No Default Credentials
- **Students**: Must register through the registration form
- **Admins**: Must register using the admin registration form with code: `ADMIN2025`

> 🔐 **Security**: No default accounts are created. All users must register first.

## 📱 Usage Guide

### For Students
1. **Registration**: Visit the registration page and fill in your details
2. **Login**: Use your registration number and password to log in
3. **Get Pass**: Your QR code pass is generated automatically
4. **Show Pass**: Display the QR code to conductors for scanning

### For Conductors
1. **Access Scanner**: Go to `/scan` route or use the scanner link
2. **Scan QR Code**: Point camera at student's QR code
3. **View Result**: See instant validation result with student details

### For Administrators
1. **Admin Login**: Use admin credentials to access admin panel
2. **Manage Students**: View, search, and filter all registered students
3. **Control Passes**: Activate or revoke student passes as needed
4. **Monitor System**: View system statistics and usage

## 🗂️ Project Structure

```
buspass-authenticator/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── forms.py              # WTForms for validation
├── create_database.py    # Database setup script
├── setup_ssl.py          # SSL certificate generator
├── run_setup.py          # Complete setup automation
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login_choice.html
│   ├── student_login.html
│   ├── admin_login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── admin_dashboard.html
│   ├── scan.html
│   └── pass_generated.html
├── static/              # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── qrcodes/         # Generated QR codes
├── cert.pem            # SSL certificate
└── key.pem             # SSL private key
```

## 🔧 Configuration

### Database Configuration
Update `config.py` with your MySQL settings:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@host:port/database'
    SECRET_KEY = 'your-secret-key-here'
```

### Environment Variables
You can also use environment variables:

```bash
export DATABASE_URL="mysql+pymysql://user:pass@localhost/buspass_db"
export SECRET_KEY="your-secret-key"
export FLASK_ENV="production"  # or "development"
```

## 🛡️ Security Considerations

### For Development
- Self-signed SSL certificates are used (browser will show warnings)
- Default passwords are set for quick testing
- Debug mode is enabled

### For Production
- Use proper SSL certificates from a trusted CA
- Change all default passwords
- Set strong SECRET_KEY
- Disable debug mode
- Use environment variables for sensitive data
- Implement rate limiting
- Add logging and monitoring

## 🐛 Troubleshooting

### Common Issues

1. **MySQL Connection Error**
   - Check if MySQL server is running
   - Verify credentials in `config.py`
   - Ensure database exists

2. **SSL Certificate Warnings**
   - Normal for self-signed certificates
   - Click "Advanced" → "Proceed to localhost"
   - For production, use proper SSL certificates

3. **Camera Access Denied**
   - Ensure HTTPS is being used
   - Grant camera permissions in browser
   - Check if camera is being used by another application

4. **QR Code Not Generating**
   - Check if `static/qrcodes/` directory exists
   - Verify write permissions
   - Check Python PIL/Pillow installation

### Database Reset
If you need to reset the database:

```bash
# Drop and recreate database
python create_database.py
```

## 📈 Future Enhancements

- [ ] Mobile app for students
- [ ] Bulk student import via CSV
- [ ] Email notifications
- [ ] Pass expiry dates
- [ ] Multiple bus routes
- [ ] Student photo integration
- [ ] Attendance tracking
- [ ] API for third-party integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the configuration guide

---

**Built with ❤️ for educational institutions**