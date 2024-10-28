import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from db_def import db, User, Event
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PERMANENT'] = False
app.config['SECRET_KEY'] = 'W2668'

# Initialize the database with the app
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = generate_password_hash('admin123')

@app.context_processor
def inject_username():
    return dict(username=session.get('username'))

# Home route
@app.route('/')
def home():
    username = session.get('username')
    return render_template('home.html', username=username)

# Events page route
@app.route('/events', methods=['GET', 'POST'])
def events():
    search_query = request.args.get('search', '')
    if search_query:
        # Filter events based on the search query
        events_data = Event.query.filter(Event.title.ilike(f'%{search_query}%')).all()
    else:
        events_data = Event.query.all()

    return render_template('events_page.html', events=events_data, search_query=search_query)


# About page route
@app.route('/about')
def about():
    return render_template('about_page.html')

# Admin Dashboard route
@app.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))
    events = Event.query.all()
    return render_template('admin_dashboard.html', events=events)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Modify the add_event route
@app.route('/admin/add_event', methods=['POST'])
def add_event():
    if not session.get('is_admin'):
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))

    title = request.form.get('title')
    date = request.form.get('date')
    location = request.form.get('location')
    description = request.form.get('description')
    
    # Handle image file upload
    image_file = request.files.get('image')
    image_path = None
    if image_file:
        filename = secure_filename(image_file.filename)
        image_path = f"uploads/{filename}"  # Only save the relative path
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(full_path)

    new_event = Event(title=title, date=date, location=location, description=description, image=image_path)
    db.session.add(new_event)
    db.session.commit()

    flash("Event added successfully!", "success")
    return redirect(url_for('admin_dashboard'))

# Delete Event route
@app.route('/admin/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    if not session.get('is_admin'):
        flash("Unauthorized access!", "error")
        return redirect(url_for('login'))
    
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        flash("Event deleted successfully!", "success")
    else:
        flash("Event not found.", "error")
    
    return redirect(url_for('admin_dashboard'))

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username already exists
        if User.query.filter_by(username=username).first():
            flash("Username already exists. Please choose another.", "error")
            return redirect(url_for('signup'))

        # Create a new user with hashed password
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('login.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check for admin credentials
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD, password):
            session['is_admin'] = True
            session['username'] = username
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_dashboard'))

        # Check for regular user credentials
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = False  # Regular user
            flash("Login successful!", "success")
            return redirect(url_for('home'))

        flash("Invalid username or password.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('home'))

@app.route('/contact')
def contact():
    return render_template('contact_page.html')

if __name__ == "__main__":
    app.run(debug=True)
