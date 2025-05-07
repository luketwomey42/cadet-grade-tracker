import os
import logging
import json
from app import app, db
from sqlalchemy import inspect, text

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Import models
from models import Cadet, Class

def migrate_database():
    """Handle database migrations manually"""
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Check if tables exist
        if 'cadets' not in inspector.get_table_names():
            # Create all tables if they don't exist
            db.create_all()
            logger.info("Created all database tables")
        else:
            # Tables exist, check for missing columns and add them
            columns = [col['name'] for col in inspector.get_columns('cadets')]
            
            with db.engine.connect() as conn:
                if 'major' not in columns:
                    logger.info("Adding 'major' column to cadets table")
                    conn.execute(text("ALTER TABLE cadets ADD COLUMN major VARCHAR(100)"))
                    conn.commit()
                
                if 'classes' not in columns:
                    logger.info("Adding 'classes' column to cadets table")
                    conn.execute(text("ALTER TABLE cadets ADD COLUMN classes TEXT DEFAULT '{}'"))
                    conn.commit()
                
                # Add company column if it doesn't exist
                if 'company' not in columns:
                    logger.info("Adding 'company' column to cadets table")
                    conn.execute(text("ALTER TABLE cadets ADD COLUMN company VARCHAR(20)"))
                    conn.commit()
                
                # Add comments column if it doesn't exist
                if 'comments' not in columns:
                    logger.info("Adding 'comments' column to cadets table")
                    conn.execute(text("ALTER TABLE cadets ADD COLUMN comments TEXT"))
                    conn.commit()
                
                # If using grades before, migrate to classes
                if 'grades' in columns and 'classes' in columns:
                    logger.info("Migrating from 'grades' to 'classes'")
                    # Get all cadets
                    result = conn.execute(text("SELECT id, grades FROM cadets WHERE grades IS NOT NULL AND grades != '{}'"))
                    for row in result:
                        try:
                            # Convert grades to classes format
                            grades = json.loads(row[1])
                            # Update the classes column
                            conn.execute(
                                text("UPDATE cadets SET classes = :classes WHERE id = :id"),
                                {"classes": json.dumps(grades), "id": row[0]}
                            )
                        except Exception as e:
                            logger.error(f"Error migrating grades for cadet {row[0]}: {str(e)}")
                    conn.commit()
            
            # Check if classes table exists
            if 'classes' not in inspector.get_table_names():
                # Create classes table
                db.create_all(tables=[Class.__table__])
                logger.info("Created classes table")
        
        # Initialize 70 empty cadet positions if they don't exist
        # Each with 5 empty class slots
        logger.info("Checking cadet positions...")
        # Get all existing positions
        existing_positions = [c.position for c in Cadet.query.all()]
        
        # Find missing positions in the range 1-70
        missing_positions = [i for i in range(1, 71) if i not in existing_positions]
        
        if missing_positions:
            logger.info(f"Found {len(missing_positions)} missing cadet positions: {missing_positions}")
            for position in missing_positions:
                # Initialize with 5 empty class slots
                empty_classes = {
                    "Class Slot 1": "",
                    "Class Slot 2": "",
                    "Class Slot 3": "",
                    "Class Slot 4": "",
                    "Class Slot 5": ""
                }
                # Check again if position exists (to be extra safe)
                if not Cadet.query.filter_by(position=position).first():
                    new_cadet = Cadet(position=position, classes=empty_classes)
                    db.session.add(new_cadet)
                    logger.info(f"Adding cadet at position {position}")
            
            db.session.commit()
            logger.info(f"Initialized {len(missing_positions)} cadet positions with 5 empty class slots each")
        
        # Add default classes if none exist
        if Class.query.count() == 0:
            default_classes = [
                ("Calculus I", "Mathematics"),
                ("Physics 101", "Physics"),
                ("Computer Science Fundamentals", "Computer Science"),
                ("Military History", "History"),
                ("Strategic Leadership", "Military Strategy"),
                ("Physical Training", "Athletics")
            ]
            
            for name, department in default_classes:
                db.session.add(Class(name=name, department=department))
            
            db.session.commit()
            logger.info("Added default classes")

# Run migrations and create tables
with app.app_context():
    migrate_database()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)