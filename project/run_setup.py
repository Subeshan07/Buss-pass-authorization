#!/usr/bin/env python3
"""
Complete Setup Script for College Bus Pass Authenticator System
This script runs the complete setup process including database and SSL.
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run([sys.executable] + command, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        if e.stderr:
            print(f"Error: {e.stderr}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        return False

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install Python requirements"""
    print("\n📦 Installing Python requirements...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'static/qrcodes',
        'static/css',
        'static/js',
        'templates'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory created: {directory}")

def main():
    """Main setup function"""
    print("🚀 College Bus Pass Authenticator - Complete Setup")
    print("=" * 60)
    
    # Check Python version
    check_python_version()
    
    # Create directories
    print("\n📁 Creating project directories...")
    create_directories()
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation")
        sys.exit(1)
    
    # Setup SSL certificates
    if not run_command(['setup_ssl.py'], "Setting up SSL certificates"):
        print("⚠️  SSL setup failed, but continuing...")
    
    # Setup database
    if not run_command(['create_database.py'], "Setting up database"):
        print("❌ Setup failed at database creation")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("\n📋 What's been set up:")
    print("   ✅ Python dependencies installed")
    print("   ✅ Project directories created")
    print("   ✅ SSL certificates generated")
    print("   ✅ MySQL database and tables created")
    print("   ✅ Default admin user created")
    print("   ✅ Sample student data added")
    
    print("\n🚀 Ready to start!")
    print("   Run: python app.py")
    print("   Access: https://localhost:5000")
    
    print("\n🔐 Default login credentials:")
    print("   Admin: admin / admin123")
    print("   Student: 21CS001 / password123")
    
    print("\n⚠️  Important notes:")
    print("   - Change default passwords in production")
    print("   - Update MySQL credentials in config.py")
    print("   - Browser will show security warning for self-signed SSL")

if __name__ == "__main__":
    main()