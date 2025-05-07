import os
import logging
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define base model class
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the base model class
db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)

# Configure app
app.secret_key = os.environ.get("SESSION_SECRET", "default-dev-secret-key") 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Define grade options, standings, majors, and companies
GRADES = ["A", "B", "C", "D", "F"]
STANDINGS = ["Perfect", "Fine", "Needs assistance"]
MAJORS = [
    "EM", "MSSEP", "MENG", "IMBU", "MTRA", "FENV"
]
COMPANIES = ["2nd", "4th", "6th"]

@app.route('/')
def index():
    """Render the main page with only authorized companies visible"""
    try:
        # Import here to avoid circular imports
        from models import Cadet
        
        # Determine which companies the user is authorized to view
        auth_2nd = session.get('auth_2nd_company') == True
        auth_4th = session.get('auth_4th_company') == True
        auth_6th = session.get('auth_6th_company') == True
        
        # Get statistics only for authorized companies
        company_stats = {}
        company_stats['2nd'] = Cadet.query.filter_by(company="2nd").count() if auth_2nd else None
        company_stats['4th'] = Cadet.query.filter_by(company="4th").count() if auth_4th else None
        company_stats['6th'] = Cadet.query.filter_by(company="6th").count() if auth_6th else None
        
        # Get overall counts only for companies the user can access
        authorized_companies = []
        if auth_2nd: authorized_companies.append("2nd")
        if auth_4th: authorized_companies.append("4th")
        if auth_6th: authorized_companies.append("6th")
        
        # Count cadets in authorized companies
        if authorized_companies:
            filled_count = Cadet.query.filter(
                Cadet.name.isnot(None),
                Cadet.company.in_(authorized_companies)
            ).count()
            total_count = Cadet.query.filter(
                Cadet.company.in_(authorized_companies)
            ).count()
        else:
            filled_count = 0
            total_count = 0
        
        return render_template('companies.html', 
                          second_company_count=company_stats['2nd'],
                          fourth_company_count=company_stats['4th'],
                          sixth_company_count=company_stats['6th'],
                          auth_2nd=auth_2nd,
                          auth_4th=auth_4th,
                          auth_6th=auth_6th,
                          filled_count=filled_count,
                          total_count=total_count)
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return render_template('companies.html', 
                            second_company_count=0,
                            fourth_company_count=0,
                            sixth_company_count=0,
                            auth_2nd=False,
                            auth_4th=False,
                            auth_6th=False,
                            filled_count=0,
                            total_count=0,
                            error=str(e))
        
# Removed full directory route to restrict access

@app.route('/company/2nd', methods=['GET', 'POST'])
def second_company():
    """Render the 2nd company cadet directory with password protection"""
    # Password for 2nd company
    COMPANY_PASSWORD = "11"
    
    # Check if user is already authenticated for this company
    if session.get('auth_2nd_company') != True:
        if request.method == 'POST':
            password = request.form.get('password', '')
            if password == COMPANY_PASSWORD:
                # Password correct, set session
                session['auth_2nd_company'] = True
                flash('Login successful. Welcome to 2nd Company.', 'success')
            else:
                # Password incorrect
                flash('Incorrect password. Access denied.', 'danger')
                return render_template('login.html', company_name="2nd")
        else:
            # GET request, show login form
            return render_template('login.html', company_name="2nd")
    
    try:
        # Import here to avoid circular imports
        from models import Cadet
        cadets = Cadet.query.filter_by(company="2nd").order_by(Cadet.position).all()
        
        # Get count of filled cadet positions
        filled_count = sum(1 for cadet in cadets if cadet.name)
        
        return render_template('index.html', 
                            cadets=cadets,
                            filled_count=filled_count,
                            total_count=len(cadets),
                            title="2nd Company Directory")
    except Exception as e:
        logger.error(f"Error in 2nd company route: {str(e)}")
        return render_template('index.html', 
                            cadets=[],
                            filled_count=0,
                            total_count=0,
                            error=str(e))

@app.route('/company/4th', methods=['GET', 'POST'])
def fourth_company():
    """Render the 4th company cadet directory with password protection"""
    # Password for 4th company
    COMPANY_PASSWORD = "1111"
    
    # Check if user is already authenticated for this company
    if session.get('auth_4th_company') != True:
        if request.method == 'POST':
            password = request.form.get('password', '')
            if password == COMPANY_PASSWORD:
                # Password correct, set session
                session['auth_4th_company'] = True
                flash('Login successful. Welcome to 4th Company.', 'success')
            else:
                # Password incorrect
                flash('Incorrect password. Access denied.', 'danger')
                return render_template('login.html', company_name="4th")
        else:
            # GET request, show login form
            return render_template('login.html', company_name="4th")
    
    try:
        # Import here to avoid circular imports
        from models import Cadet
        cadets = Cadet.query.filter_by(company="4th").order_by(Cadet.position).all()
        
        # Get count of filled cadet positions
        filled_count = sum(1 for cadet in cadets if cadet.name)
        
        return render_template('index.html', 
                            cadets=cadets,
                            filled_count=filled_count,
                            total_count=len(cadets),
                            title="4th Company Directory")
    except Exception as e:
        logger.error(f"Error in 4th company route: {str(e)}")
        return render_template('index.html', 
                            cadets=[],
                            filled_count=0,
                            total_count=0,
                            error=str(e))

@app.route('/company/6th', methods=['GET', 'POST'])
def sixth_company():
    """Render the 6th company cadet directory with password protection"""
    # Password for 6th company
    COMPANY_PASSWORD = "111111"
    
    # Check if user is already authenticated for this company
    if session.get('auth_6th_company') != True:
        if request.method == 'POST':
            password = request.form.get('password', '')
            if password == COMPANY_PASSWORD:
                # Password correct, set session
                session['auth_6th_company'] = True
                flash('Login successful. Welcome to 6th Company.', 'success')
            else:
                # Password incorrect
                flash('Incorrect password. Access denied.', 'danger')
                return render_template('login.html', company_name="6th")
        else:
            # GET request, show login form
            return render_template('login.html', company_name="6th")
    
    try:
        # Import here to avoid circular imports
        from models import Cadet
        cadets = Cadet.query.filter_by(company="6th").order_by(Cadet.position).all()
        
        # Get count of filled cadet positions
        filled_count = sum(1 for cadet in cadets if cadet.name)
        
        return render_template('index.html', 
                            cadets=cadets,
                            filled_count=filled_count,
                            total_count=len(cadets),
                            title="6th Company Directory")
    except Exception as e:
        logger.error(f"Error in 6th company route: {str(e)}")
        return render_template('index.html', 
                            cadets=[],
                            filled_count=0,
                            total_count=0,
                            error=str(e))

@app.route('/cadet/<int:position>')
def view_cadet(position):
    """View a specific cadet's details with strict company separation"""
    # Import here to avoid circular imports
    from models import Cadet, Class
    
    cadet = Cadet.query.filter_by(position=position).first_or_404()
    
    # Enforce complete company separation
    # Only allow access if the user has been authenticated for this specific company
    if cadet.company:
        company_auth_key = f'auth_{cadet.company.lower()}_company'
        if not session.get(company_auth_key):
            flash(f'Access denied. This cadet belongs to {cadet.company} Company and you do not have permission to view.', 'danger')
            return redirect(url_for('index'))
    
    # Get all classes for dropdown selection
    all_classes = Class.query.order_by(Class.department, Class.name).all()
    
    # Group classes by department for easier selection
    departments = {}
    for cls in all_classes:
        dept = cls.department or "Other"
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(cls)
    
    return render_template('cadet.html',
                        cadet=cadet,
                        departments=departments,
                        grades=GRADES,
                        standings=STANDINGS,
                        majors=MAJORS,
                        companies=COMPANIES)

@app.route('/cadet/<int:position>/update', methods=['POST'])
def update_cadet(position):
    """Update a cadet's information with company separation"""
    # Import here to avoid circular imports
    from models import Cadet, Class
    
    cadet = Cadet.query.filter_by(position=position).first_or_404()
    
    # Enforce company separation
    if cadet.company:
        company_auth_key = f'auth_{cadet.company.lower()}_company'
        if not session.get(company_auth_key):
            flash(f'Access denied. This cadet belongs to {cadet.company} Company and you do not have permission to modify.', 'danger')
            return redirect(url_for('index'))
    
    # Get basic cadet info
    cadet.name = request.form.get('name', '').strip()
    cadet.standing = request.form.get('standing', '').strip()
    cadet.major = request.form.get('major', '').strip()
    
    # Maintain company separation - a user can only set cadets to their own company
    requested_company = request.form.get('company', '').strip()
    if requested_company:
        company_auth_key = f'auth_{requested_company.lower()}_company'
        if not session.get(company_auth_key):
            flash(f'You cannot assign a cadet to {requested_company} Company without proper authorization.', 'warning')
            # Keep the original company
        else:
            cadet.company = requested_company
    
    # Start with the current classes dictionary
    # Only keep real classes, not placeholders
    new_classes = {k: v for k, v in cadet.classes.items() if not k.startswith("Class Slot")}
    
    # Track classes we've already processed to avoid duplicates
    processed_classes = set(new_classes.keys())
    
    # Keep track of changes for debug messages
    changes = []
    
    # Process each of the form fields
    # No limit on how many classes a cadet can have
    
    # Process class entries dynamically based on form data
    # Extract all class indices from the form
    class_indices = set()
    for key in request.form.keys():
        if key.startswith('class_'):
            try:
                index = int(key.replace('class_', ''))
                class_indices.add(index)
            except ValueError:
                continue
    
    # Process all classes in order
    for i in sorted(class_indices):
        # Get the original class name that was in this slot
        original_class = request.form.get(f'original_class_{i}', '').strip()
        
        # Get the selected class for this slot
        selected_class = request.form.get(f'class_{i}', '').strip()
        
        # Check if custom class was selected
        if selected_class == 'custom':
            # Use the custom class input instead
            custom_class = request.form.get(f'custom_class_{i}', '').strip()
            if custom_class:
                selected_class = custom_class
                
                # Add the custom class to the database if it's new
                if not Class.query.filter_by(name=custom_class).first():
                    department = "Custom"
                    new_class_obj = Class(name=custom_class, department=department)
                    db.session.add(new_class_obj)
                    changes.append(f"Added new class: {custom_class}")
        
        # Skip if we've already processed this class (to prevent duplicates)
        if selected_class and selected_class in processed_classes:
            logger.warning(f"Skipping duplicate class: {selected_class}")
            continue
            
        # Get the grade for this slot
        grade = request.form.get(f'grade_{i}', '').strip()
        
        # Only add real classes (no empty slots)
        if selected_class and not selected_class.startswith("Class Slot"):
            # Add the class with the grade (it's a real class)
            new_classes[selected_class] = grade
            processed_classes.add(selected_class)
            
            if original_class != selected_class:
                changes.append(f"Added new class: {selected_class}")
            elif original_class in new_classes and new_classes[original_class] != grade:
                changes.append(f"Updated grade for {selected_class} to {grade}")
        
        # Handle removal of original class if it was replaced
        elif original_class and original_class in new_classes and original_class != selected_class:
            changes.append(f"Removed class: {original_class}")
            # The class will be excluded from new_classes because selected_class is empty
    
    # Update the cadet's classes
    cadet.classes = new_classes
    
    # Update comments field
    cadet.comments = request.form.get('comments', '').strip()
    
    # Log changes for debugging
    logger.info(f"Classes update for cadet {position}: {len(new_classes)} classes, changes: {changes}")
    logger.info(f"Cadet will have {len(new_classes)} classes after update")
    
    db.session.commit()
    flash(f'Cadet {cadet.name} updated successfully.', 'success')
    return redirect(url_for('view_cadet', position=position))

@app.route('/cadet/<int:position>/remove_class', methods=['POST'])
def remove_class(position):
    """Remove a class from a cadet's record without adding an empty slot"""
    # Import here to avoid circular imports
    from models import Cadet
    
    cadet = Cadet.query.filter_by(position=position).first_or_404()
    
    # Enforce company separation
    if cadet.company:
        company_auth_key = f'auth_{cadet.company.lower()}_company'
        if not session.get(company_auth_key):
            flash(f'Access denied. This cadet belongs to {cadet.company} Company and you do not have permission to modify.', 'danger')
            return redirect(url_for('index'))
            
    class_name = request.form.get('class_name', '').strip()
    
    if class_name in cadet.classes:
        # Remove the class
        classes = cadet.classes.copy()
        del classes[class_name]
        
        # Update the cadet's classes - no need to add an empty slot or enforce total count
        cadet.classes = classes
        db.session.commit()
        logger.info(f"Removed class '{class_name}' from cadet {position}")
        flash(f'Removed {class_name} from {cadet.name}\'s record.', 'success')
    
    return redirect(url_for('view_cadet', position=position))

@app.route('/cadet/new', methods=['GET', 'POST'])
def new_cadet():
    """Create a new cadet with company separation and no class minimum"""
    # Import here to avoid circular imports
    from models import Cadet, Class
    
    if request.method == 'POST':
        # Get the requested company and verify user has access to it
        requested_company = request.form.get('company', '').strip()
        if requested_company:
            company_auth_key = f'auth_{requested_company.lower()}_company'
            if not session.get(company_auth_key):
                flash(f'You cannot create a cadet in {requested_company} Company without proper authorization.', 'danger')
                return redirect(url_for('index'))
        
        # No limit on cadets - find the next available position
        used_positions = [c.position for c in Cadet.query.all()]
        
        # Find the next available position (no maximum position limit)
        position = 1
        while position in used_positions:
            position += 1
        
        # Get basic cadet info
        name = request.form.get('name', '').strip()
        standing = request.form.get('standing', '').strip()
        major = request.form.get('major', '').strip()
        company = requested_company  # Use the validated company
        
        # Process classes - no minimum or maximum requirement
        classes = {}
        
        # Track classes we've already processed to avoid duplicates
        processed_classes = set()
        
        # Process class entries dynamically based on form data
        # Extract all class indices from the form
        class_indices = set()
        for key in request.form.keys():
            if key.startswith('class_'):
                try:
                    index = int(key.replace('class_', ''))
                    class_indices.add(index)
                except ValueError:
                    continue
                    
        # Process all found classes
        for i in sorted(class_indices):
            # Get the class selection
            selected_class = request.form.get(f'class_{i}', '').strip()
            
            # Check if custom class was selected
            if selected_class == 'custom':
                # Use the custom class input instead
                selected_class = request.form.get(f'custom_class_{i}', '').strip()
                
                # Add it to the Class table if it's a new class and not empty
                if selected_class and not Class.query.filter_by(name=selected_class).first():
                    department = "Custom"  # Default department for custom classes
                    new_class_obj = Class(name=selected_class, department=department)
                    db.session.add(new_class_obj)
            
            # Skip if we've already processed this class (to prevent duplicates)
            if selected_class and selected_class in processed_classes:
                logger.warning(f"Skipping duplicate class: {selected_class}")
                continue
            
            # Get the grade for this class 
            grade = request.form.get(f'grade_{i}', '').strip()
            
            # Only add real classes (not empty slots)
            if selected_class and not selected_class.startswith('Class Slot'):
                # Add the selected class
                classes[selected_class] = grade
                processed_classes.add(selected_class)
            
            # Don't add empty slots - we allow cadets to have any number of classes including 0
        
        # Get comments
        comments = request.form.get('comments', '').strip()
        
        # Create the cadet with the processed classes and comments
        cadet = Cadet(
            position=position,
            name=name,
            standing=standing,
            major=major,
            company=company,
            classes=classes,
            comments=comments
        )
        
        db.session.add(cadet)
        db.session.commit()
        
        flash(f'Cadet {cadet.name} created successfully.', 'success')
        return redirect(url_for('view_cadet', position=cadet.position))
    
    # GET request - display form
    # Get all classes for dropdown selection
    classes = Class.query.order_by(Class.department, Class.name).all()
    
    # Group classes by department for easier selection
    departments = {}
    for cls in classes:
        dept = cls.department or "Other"
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(cls)
    
    return render_template('new_cadet.html',
                        standings=STANDINGS,
                        grades=GRADES,
                        majors=MAJORS,
                        companies=COMPANIES,
                        departments=departments)

@app.route('/analytics')
def analytics():
    """Show academic analytics with charts and graphs for all authorized companies"""
    # Import here to avoid circular imports
    from models import Cadet, Class
    import json
    
    # Determine which companies the user is authorized to view
    auth_2nd = session.get('auth_2nd_company') == True
    auth_4th = session.get('auth_4th_company') == True
    auth_6th = session.get('auth_6th_company') == True
    
    # Get authorized companies
    authorized_companies = []
    if auth_2nd: authorized_companies.append("2nd")
    if auth_4th: authorized_companies.append("4th")
    if auth_6th: authorized_companies.append("6th")
    
    if not authorized_companies:
        flash('You need to be logged into at least one company to view analytics.', 'danger')
        return redirect(url_for('index'))
    
    # Get cadets from authorized companies
    cadets = Cadet.query.filter(Cadet.company.in_(authorized_companies)).all()
    
    # Convert cadet data to JSON-safe format
    cadets_list = []
    for cadet in cadets:
        if cadet.name:  # Only include cadets with names
            cadet_dict = {
                'id': cadet.id,
                'position': cadet.position,
                'name': cadet.name,
                'standing': cadet.standing,
                'major': cadet.major,
                'company': cadet.company,
                'classes': cadet.classes
            }
            cadets_list.append(cadet_dict)
    
    # Calculate initial stats
    total_cadets = len(cadets_list)
    
    # Calculate GPA
    total_points = 0
    total_grades = 0
    
    for cadet in cadets_list:
        for grade in cadet['classes'].values():
            if grade:
                points = 0
                if grade == 'A': points = 4
                elif grade == 'B': points = 3
                elif grade == 'C': points = 2
                elif grade == 'D': points = 1
                
                total_points += points
                total_grades += 1
    
    avg_gpa = round(total_points / total_grades, 2) if total_grades > 0 else 'N/A'
    
    # Calculate total classes
    total_classes = 0
    for cadet in cadets_list:
        total_classes += len(cadet['classes'])
    
    return render_template('analytics.html',
                       cadets_json=json.dumps(cadets_list),
                       total_cadets=total_cadets,
                       avg_gpa=avg_gpa,
                       total_classes=total_classes,
                       auth_2nd=auth_2nd,
                       auth_4th=auth_4th,
                       auth_6th=auth_6th,
                       page_title="Combined Analytics",
                       company_view="all")

def get_company_analytics_data(company):
    """Helper function to get analytics data for a specific company"""
    from models import Cadet
    import json
    
    # Get cadets from specified company
    cadets = Cadet.query.filter_by(company=company).all()
    
    # Convert cadet data to JSON-safe format
    cadets_list = []
    for cadet in cadets:
        if cadet.name:  # Only include cadets with names
            cadet_dict = {
                'id': cadet.id,
                'position': cadet.position,
                'name': cadet.name,
                'standing': cadet.standing,
                'major': cadet.major,
                'company': cadet.company,
                'classes': cadet.classes
            }
            cadets_list.append(cadet_dict)
    
    # Calculate stats
    total_cadets = len(cadets_list)
    
    # Calculate GPA
    total_points = 0
    total_grades = 0
    
    for cadet in cadets_list:
        for grade in cadet['classes'].values():
            if grade:
                points = 0
                if grade == 'A': points = 4
                elif grade == 'B': points = 3
                elif grade == 'C': points = 2
                elif grade == 'D': points = 1
                
                total_points += points
                total_grades += 1
    
    avg_gpa = round(total_points / total_grades, 2) if total_grades > 0 else 'N/A'
    
    # Calculate total classes
    total_classes = 0
    for cadet in cadets_list:
        total_classes += len(cadet['classes'])
        
    return {
        'cadets_json': json.dumps(cadets_list),
        'total_cadets': total_cadets,
        'avg_gpa': avg_gpa,
        'total_classes': total_classes
    }
    
@app.route('/analytics/2nd')
def analytics_2nd_company():
    """Show academic analytics for 2nd company only"""
    # Check if user is authorized
    if not session.get('auth_2nd_company'):
        flash('You need to be logged into 2nd company to view these analytics.', 'danger')
        return redirect(url_for('index'))
    
    # Get analytics data
    data = get_company_analytics_data("2nd")
    
    return render_template('analytics.html',
                       cadets_json=data['cadets_json'],
                       total_cadets=data['total_cadets'],
                       avg_gpa=data['avg_gpa'],
                       total_classes=data['total_classes'],
                       auth_2nd=True,
                       auth_4th=False,
                       auth_6th=False,
                       page_title="2nd Company Analytics",
                       company_view="2nd")

@app.route('/analytics/4th')
def analytics_4th_company():
    """Show academic analytics for 4th company only"""
    # Check if user is authorized
    if not session.get('auth_4th_company'):
        flash('You need to be logged into 4th company to view these analytics.', 'danger')
        return redirect(url_for('index'))
    
    # Get analytics data
    data = get_company_analytics_data("4th")
    
    return render_template('analytics.html',
                       cadets_json=data['cadets_json'],
                       total_cadets=data['total_cadets'],
                       avg_gpa=data['avg_gpa'],
                       total_classes=data['total_classes'],
                       auth_2nd=False,
                       auth_4th=True,
                       auth_6th=False,
                       page_title="4th Company Analytics",
                       company_view="4th")

@app.route('/analytics/6th')
def analytics_6th_company():
    """Show academic analytics for 6th company only"""
    # Check if user is authorized
    if not session.get('auth_6th_company'):
        flash('You need to be logged into 6th company to view these analytics.', 'danger')
        return redirect(url_for('index'))
    
    # Get analytics data
    data = get_company_analytics_data("6th")
    
    return render_template('analytics.html',
                       cadets_json=data['cadets_json'],
                       total_cadets=data['total_cadets'],
                       avg_gpa=data['avg_gpa'],
                       total_classes=data['total_classes'],
                       auth_2nd=False,
                       auth_4th=False,
                       auth_6th=True,
                       page_title="6th Company Analytics",
                       company_view="6th")

@app.route('/classes')
def list_classes():
    """List all classes in the system"""
    # Import here to avoid circular imports
    from models import Class
    
    classes = Class.query.order_by(Class.department, Class.name).all()
    
    # Group by department
    departments = {}
    for cls in classes:
        dept = cls.department or "Other"
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(cls)
    
    return render_template('classes.html', departments=departments)

@app.route('/class/new', methods=['POST'])
def new_class():
    """Add a new class to the system"""
    # Import here to avoid circular imports
    from models import Class
    
    name = request.form.get('name', '').strip()
    department = request.form.get('department', '').strip()
    
    if not name:
        flash('Class name is required.', 'danger')
        return redirect(url_for('list_classes'))
    
    # Check if class already exists
    if Class.query.filter_by(name=name).first():
        flash(f'Class "{name}" already exists.', 'warning')
        return redirect(url_for('list_classes'))
    
    # Add new class
    new_class = Class(name=name, department=department)
    db.session.add(new_class)
    db.session.commit()
    
    flash(f'Class "{name}" added successfully.', 'success')
    return redirect(url_for('list_classes'))

@app.route('/class/delete', methods=['POST'])
def delete_class():
    """Delete a class from the system"""
    # Import here to avoid circular imports
    from models import Class
    
    class_id = request.form.get('class_id')
    
    if not class_id:
        flash('Class ID is required.', 'danger')
        return redirect(url_for('list_classes'))
    
    # Find the class
    class_to_delete = Class.query.get(class_id)
    
    if not class_to_delete:
        flash('Class not found.', 'danger')
        return redirect(url_for('list_classes'))
    
    class_name = class_to_delete.name
    
    # Delete the class
    db.session.delete(class_to_delete)
    db.session.commit()
    
    flash(f'Class "{class_name}" deleted successfully.', 'success')
    return redirect(url_for('list_classes'))

@app.route('/clear/<int:position>', methods=['POST'])
def clear_cadet(position):
    """Clear a cadet's information (reset to empty) with company separation"""
    # Import here to avoid circular imports
    from models import Cadet
    
    cadet = Cadet.query.filter_by(position=position).first()
    
    if not cadet:
        flash(f'Cadet position {position} not found.', 'danger')
        return redirect(url_for('index'))
    
    # Enforce company separation
    if cadet.company:
        company_auth_key = f'auth_{cadet.company.lower()}_company'
        if not session.get(company_auth_key):
            flash(f'Access denied. This cadet belongs to {cadet.company} Company and you do not have permission to modify.', 'danger')
            return redirect(url_for('index'))
    
    # Reset cadet information with no classes and no comments
    cadet.name = None
    cadet.standing = None
    cadet.major = None
    cadet.company = None
    cadet.classes = {}
    cadet.comments = None
    
    db.session.commit()
    flash(f'Cadet position {position} cleared.', 'success')
    return redirect(url_for('index'))

@app.route('/delete/<int:position>', methods=['POST'])
def delete_cadet(position):
    """Delete a cadet completely from the database with company separation"""
    # Import here to avoid circular imports
    from models import Cadet
    
    cadet = Cadet.query.filter_by(position=position).first()
    
    if not cadet:
        flash(f'Cadet position {position} not found.', 'danger')
        return redirect(url_for('index'))
    
    # Enforce company separation
    if cadet.company:
        company_auth_key = f'auth_{cadet.company.lower()}_company'
        if not session.get(company_auth_key):
            flash(f'Access denied. This cadet belongs to {cadet.company} Company and you do not have permission to delete.', 'danger')
            return redirect(url_for('index'))
    
    # Store the name for the flash message
    cadet_name = cadet.name or f"Position {position}"
    
    # Delete the cadet
    db.session.delete(cadet)
    db.session.commit()
    
    flash(f'Cadet {cadet_name} has been deleted.', 'success')
    return redirect(url_for('index'))

@app.route('/delete-all-cadets', methods=['POST'])
def delete_all_cadets():
    """Delete all cadets from a specific company that the user has access to"""
    # Import here to avoid circular imports
    from models import Cadet
    
    # Determine which companies the user has access to
    authorized_companies = []
    for company in COMPANIES:
        company_auth_key = f'auth_{company.lower()}_company'
        if session.get(company_auth_key):
            authorized_companies.append(company)
    
    if not authorized_companies:
        flash('You need to be logged into at least one company to delete cadets.', 'danger')
        return redirect(url_for('index'))
    
    # Get only cadets from the companies the user has access to
    cadets_to_delete = Cadet.query.filter(Cadet.company.in_(authorized_companies)).all()
    count = len(cadets_to_delete)
    
    if count == 0:
        flash('No cadets found to delete in your authorized companies.', 'info')
        return redirect(url_for('index'))
    
    # Delete all cadets from the authorized companies
    for cadet in cadets_to_delete:
        db.session.delete(cadet)
    
    db.session.commit()
    
    # Prepare a message that includes which companies were affected
    companies_text = ", ".join(authorized_companies)
    flash(f'All {count} cadets from {companies_text} Company have been deleted.', 'success')
    return redirect(url_for('index'))

@app.route('/remove-empty-slots')
def reset_class_slots():
    """Clean cadets' class lists to remove empty slots and keep only real classes"""
    # Import here to avoid circular imports
    from models import Cadet
    
    # Determine which companies the user has access to
    authorized_companies = []
    for company in COMPANIES:
        company_auth_key = f'auth_{company.lower()}_company'
        if session.get(company_auth_key):
            authorized_companies.append(company)
    
    if not authorized_companies:
        flash('You need to be logged into at least one company to manage cadets.', 'danger')
        return redirect(url_for('index'))
    
    # Get only cadets from the companies the user has access to
    cadets = Cadet.query.filter(Cadet.company.in_(authorized_companies)).all()
    
    if not cadets:
        flash('No cadets found in your authorized companies.', 'info')
        return redirect(url_for('index'))
        
    counter = 0
    
    for cadet in cadets:
        # Get current classes
        current_classes = cadet.classes
        
        # Create a new classes dict with only real classes
        new_classes = {}
        
        # Keep only real classes (not "Class Slot X" placeholders)
        for class_name, grade in current_classes.items():
            if "Class Slot" not in class_name:
                # Only keep real classes
                new_classes[class_name] = grade
        
        # Log the changes
        if len(current_classes) != len(new_classes):
            logger.info(f"Cleaning cadet {cadet.position}: {len(current_classes)} classes → {len(new_classes)} classes")
            
        # Only update if needed
        if set(current_classes.keys()) != set(new_classes.keys()):
            # Set the cadet's classes to our new cleaned dictionary
            cadet.classes = new_classes
            counter += 1
    
    # Commit changes if any were made
    if counter > 0:
        db.session.commit()
        flash(f'Cleaned class lists for {counter} cadets, removing empty slots.', 'success')
    else:
        flash('No empty slots found to clean.', 'info')
    
    return redirect(url_for('index'))