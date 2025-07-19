#!/usr/bin/env python3
"""
Database Creation Script for College Bus Pass Authenticator System
This script creates the MySQL database and tables required for the application.
"""

import mysql.connector
from mysql.connector import Error
import sys
import os
from werkzeug.security import generate_password_hash

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change this to your MySQL username
    'password': 'Sube@2005',  # Your MySQL password
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

DATABASE_NAME = 'buspass_db'

def create_database():
    """Create the main database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Database '{DATABASE_NAME}' created successfully!")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables():
    """Create all required tables"""
    try:
        # Connect to the specific database
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Create students table
        students_table = """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            reg_no VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            department VARCHAR(50) NOT NULL,
            year VARCHAR(10) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            qr_code_path VARCHAR(200),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_reg_no (reg_no),
            INDEX idx_is_active (is_active)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        # Create admins table
        admins_table = """
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_username (username)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        # Create pass_scans table for tracking scans
        pass_scans_table = """
        CREATE TABLE IF NOT EXISTS pass_scans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            scanner_info VARCHAR(200),
            status ENUM('valid', 'invalid', 'blocked') NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
            INDEX idx_student_id (student_id),
            INDEX idx_scanned_at (scanned_at)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        # Execute table creation
        cursor.execute(students_table)
        print("✅ Students table created successfully!")
        
        cursor.execute(admins_table)
        print("✅ Admins table created successfully!")
        
        cursor.execute(pass_scans_table)
        print("✅ Pass scans table created successfully!")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error creating tables: {e}")
        return False

def create_admin_registration_route():
    """Create admin registration capability"""
    try:
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("✅ Admin table ready for registration!")
        print("   No default admin created - register through the application")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error setting up admin table: {e}")
        return False


def test_connection():
    """Test database connection"""
    try:
        config = DB_CONFIG.copy()
        config['database'] = DATABASE_NAME
        
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Test queries
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM admins")
        admin_count = cursor.fetchone()[0]
        
        print(f"✅ Database connection successful!")
        print(f"   Students: {student_count}")
        print(f"   Admins: {admin_count}")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up College Bus Pass Authenticator Database...")
    print("=" * 60)
    
    # Check MySQL connection
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        connection.close()
        print("✅ MySQL connection successful!")
    except Error as e:
        print(f"❌ MySQL connection failed: {e}")
        print("Please check your MySQL server and credentials in DB_CONFIG")
        sys.exit(1)
    
    # Create database
    if not create_database():
        sys.exit(1)
    
    # Create tables
    if not create_tables():
        sys.exit(1)
    
    # Setup admin registration capability
    if not create_admin_registration_route():
        sys.exit(1)
    
    # Test connection
    if not test_connection():
        sys.exit(1)
    
    print("=" * 60)
    print("🎉 Database setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update config.py with your MySQL credentials")
    print("2. Install SSL certificates (cert.pem, key.pem)")
    print("3. Run: python app.py")

if __name__ == "__main__":
    main()