#!/usr/bin/env python3
"""
SSL Certificate Setup Script for College Bus Pass Authenticator System
This script generates self-signed SSL certificates for HTTPS development.
"""

import os
import subprocess
import sys
from datetime import datetime, timedelta

def check_openssl():
    """Check if OpenSSL is available"""
    try:
        result = subprocess.run(['openssl', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ OpenSSL found: {result.stdout.strip()}")
            return True
        else:
            print("❌ OpenSSL not found")
            return False
    except FileNotFoundError:
        print("❌ OpenSSL not found in PATH")
        return False

def generate_ssl_certificates():
    """Generate self-signed SSL certificates"""
    try:
        print("🔐 Generating SSL certificates...")
        
        # Generate private key
        key_cmd = [
            'openssl', 'genrsa',
            '-out', 'key.pem',
            '2048'
        ]
        
        result = subprocess.run(key_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error generating private key: {result.stderr}")
            return False
        
        print("✅ Private key generated (key.pem)")
        
        # Generate certificate
        cert_cmd = [
            'openssl', 'req',
            '-new', '-x509',
            '-key', 'key.pem',
            '-out', 'cert.pem',
            '-days', '365',
            '-subj', '/C=IN/ST=State/L=City/O=College/OU=IT/CN=localhost'
        ]
        
        result = subprocess.run(cert_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Error generating certificate: {result.stderr}")
            return False
        
        print("✅ Certificate generated (cert.pem)")
        
        # Set appropriate permissions
        os.chmod('key.pem', 0o600)
        os.chmod('cert.pem', 0o644)
        
        print("✅ SSL certificates generated successfully!")
        print("   - cert.pem (Certificate)")
        print("   - key.pem (Private Key)")
        print("\n⚠️  These are self-signed certificates for development only!")
        print("   Your browser will show a security warning - this is normal.")
        print("   Click 'Advanced' and 'Proceed to localhost' to continue.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating SSL certificates: {e}")
        return False

def create_ssl_config():
    """Create SSL configuration file"""
    ssl_config = """# SSL Configuration for Development
# 
# This file contains SSL configuration for the Flask application.
# For production, use proper SSL certificates from a trusted CA.

[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no

[req_distinguished_name]
C = IN
ST = State
L = City
O = College
OU = IT Department
CN = localhost

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = 127.0.0.1
IP.1 = 127.0.0.1
IP.2 = ::1
"""
    
    try:
        with open('ssl.conf', 'w') as f:
            f.write(ssl_config)
        print("✅ SSL configuration file created (ssl.conf)")
        return True
    except Exception as e:
        print(f"❌ Error creating SSL config: {e}")
        return False

def main():
    """Main SSL setup function"""
    print("🔐 Setting up SSL Certificates for HTTPS...")
    print("=" * 50)
    
    # Check if certificates already exist
    if os.path.exists('cert.pem') and os.path.exists('key.pem'):
        print("ℹ️  SSL certificates already exist!")
        response = input("Do you want to regenerate them? (y/N): ").lower()
        if response != 'y':
            print("✅ Using existing SSL certificates")
            return
    
    # Check OpenSSL availability
    if not check_openssl():
        print("\n📋 To install OpenSSL:")
        print("   Windows: Download from https://slproweb.com/products/Win32OpenSSL.html")
        print("   macOS: brew install openssl")
        print("   Ubuntu/Debian: sudo apt-get install openssl")
        print("   CentOS/RHEL: sudo yum install openssl")
        sys.exit(1)
    
    # Create SSL config
    create_ssl_config()
    
    # Generate certificates
    if generate_ssl_certificates():
        print("\n🎉 SSL setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run the database setup: python create_database.py")
        print("2. Start the application: python app.py")
        print("3. Access via: https://localhost:5000")
        print("\n⚠️  Browser Security Warning:")
        print("   Your browser will show 'Your connection is not private'")
        print("   This is normal for self-signed certificates.")
        print("   Click 'Advanced' → 'Proceed to localhost (unsafe)' to continue.")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()