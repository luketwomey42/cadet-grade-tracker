from app import db
import json

class Cadet(db.Model):
    """Cadet model for storing cadet information"""
    __tablename__ = 'cadets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    standing = db.Column(db.String(50), nullable=True)
    major = db.Column(db.String(100), nullable=True)
    company = db.Column(db.String(20), nullable=True)  # Added company field (2nd, 4th, 6th)
    # Store classes and grades as JSON string
    _classes = db.Column('classes', db.Text, default='{}')
    position = db.Column(db.Integer, nullable=False, unique=True)
    comments = db.Column(db.Text, nullable=True)  # Added comments field for cadet notes
    
    def __init__(self, position, name=None, standing=None, major=None, company=None, classes=None, comments=None):
        self.position = position
        self.name = name
        self.standing = standing
        self.major = major
        self.company = company
        self.classes = classes or {}
        self.comments = comments
    
    @property
    def classes(self):
        if not self._classes:
            return {}
        return json.loads(self._classes)
    
    @classes.setter
    def classes(self, value):
        self._classes = json.dumps(value)
        
class Class(db.Model):
    """Class model for tracking all possible classes across majors"""
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    department = db.Column(db.String(100), nullable=True)
    
    def __init__(self, name, department=None):
        self.name = name
        self.department = department