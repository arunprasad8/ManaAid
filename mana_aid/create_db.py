#!/usr/bin/env python3
"""
Standalone script to create the database and verify schema
"""
import os
import sys
from sqlalchemy import create_engine, inspect, text

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.surplus_post import SurplusPost
from app.models.food_request import FoodRequest
from app.models.volunteer_task import VolunteerTask
from app.models.sponsor_order import SponsorOrder

def main():
    print("Creating Flask app...")
    app = create_app()
    
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        
        print("Creating all tables...")
        db.create_all()
        
        print("Verifying User table schema...")
        inspector = inspect(db.engine)
        user_columns = inspector.get_columns('user')
        
        print("User table columns:")
        for column in user_columns:
            print(f"  - {column['name']}: {column['type']}")
        
        # Check if phone column exists
        phone_exists = any(col['name'] == 'phone' for col in user_columns)
        print(f"\nPhone column exists: {phone_exists}")
        
        if not phone_exists:
            print("ERROR: Phone column is missing!")
            return False
        
        print("\nDatabase created successfully!")
        return True

if __name__ == "__main__":
    main() 