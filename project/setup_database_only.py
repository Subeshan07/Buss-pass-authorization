#!/usr/bin/env python3
"""
Quick Database Setup Script for College Bus Pass Authenticator System
Run this first to create the database before starting the application.
"""

import mysql.connector
from mysql.connector import Error
import sys

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Sube@2005',  # Your MySQL password
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

DATABASE_NAME = 'buspass_db'

def test_mysql_connection():
    """Test basic MySQL connection"""
    try:
        print("🔍 Testing MySQL connection...")
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        if connection.is_connected():
            print("✅ MySQL connection successful!")
            connection.close()
            return True
    except Error as e:
        print(f"❌ MySQL connection failed: {e}")
        print("\n📋 Troubleshooting steps:")
        print("1. Make sure MySQL server is running")
        print("2. Check if username 'root' is correct")
        print("3. Verify password 'Sube@2005' is correct")
        print("4. Ensure MySQL is installed and accessible")
        return False

def create_database():
    """Create the database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Database '{DATABASE_NAME}' created successfully!")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Setting up MySQL Database for Bus Pass System...")
    print("=" * 50)
    
    # Test MySQL connection
    if not test_mysql_connection():
        sys.exit(1)
    
    # Create database
    if not create_database():
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 Database setup completed!")
    print("\n📋 Next steps:")
    print("1. Run: python app.py")
    print("2. The app will create tables automatically")
    print("3. Access: https://localhost:5000")

if __name__ == "__main__":
    main()