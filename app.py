"""
Recipe Sharing Platform - Flask Web Application
Student Name: [Your Name Here]
Class: [Your Class Name and Number]
Project: Flask Web Application - Recipe Sharing Platform
Date: October 2025

This is a recipe sharing web application that allows users to register, login,
create recipes, view recipes from other users, and manage their own recipe collection.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import os

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)


# Database Models
class User(db.Model):
    """User model for authentication and user management"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with recipes (one-to-many)
    recipes = db.relationship('Recipe', backref='author', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the user's password"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Recipe(db.Model):
    """Recipe model for storing recipe information"""
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer)  # in minutes
    cook_time = db.Column(db.Integer)  # in minutes
    servings = db.Column(db.Integer)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key relationship to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Recipe {self.title}>'


# Login required decorator
def login_required(f):
    """Decorator to require login for certain routes"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# Routes
@app.route('/')
def index():
    """Home page showing recent recipes"""
    recent_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(6).all()
    return render_template('index.html', recipes=recent_recipes)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page with form handling"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html')

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page with form handling"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Log out the current user"""
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/recipes')
def recipes():
    """Display all recipes with filtering options"""
    category = request.args.get('category')

    if category:
        recipes_list = Recipe.query.filter_by(category=category).order_by(Recipe.created_at.desc()).all()
    else:
        recipes_list = Recipe.query.order_by(Recipe.created_at.desc()).all()

    return render_template('recipes.html', recipes=recipes_list, current_category=category)


@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Display detailed view of a single recipe"""
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)


@app.route('/add-recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    """Add a new recipe - requires login"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        prep_time = request.form.get('prep_time')
        cook_time = request.form.get('cook_time')
        servings = request.form.get('servings')
        category = request.form.get('category')

        # Validation
        if not title or not description or not ingredients or not instructions:
            flash('Please fill in all required fields.', 'danger')
            return render_template('add_recipe.html')

        # Create new recipe
        new_recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            prep_time=int(prep_time) if prep_time else None,
            cook_time=int(cook_time) if cook_time else None,
            servings=int(servings) if servings else None,
            category=category,
            user_id=session['user_id']
        )

        db.session.add(new_recipe)
        db.session.commit()

        flash('Recipe added successfully!', 'success')
        return redirect(url_for('recipe_detail', recipe_id=new_recipe.id))

    return render_template('add_recipe.html')


@app.route('/profile')
@login_required
def profile():
    """User profile page showing their recipes"""
    user = User.query.get(session['user_id'])
    user_recipes = Recipe.query.filter_by(user_id=session['user_id']).order_by(Recipe.created_at.desc()).all()
    return render_template('profile.html', user=user, recipes=user_recipes)


@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    """Edit an existing recipe - only by the author"""
    recipe = Recipe.query.get_or_404(recipe_id)

    # Check if current user is the author
    if recipe.user_id != session['user_id']:
        flash('You can only edit your own recipes.', 'danger')
        return redirect(url_for('recipe_detail', recipe_id=recipe_id))

    if request.method == 'POST':
        recipe.title = request.form.get('title')
        recipe.description = request.form.get('description')
        recipe.ingredients = request.form.get('ingredients')
        recipe.instructions = request.form.get('instructions')
        recipe.prep_time = int(request.form.get('prep_time')) if request.form.get('prep_time') else None
        recipe.cook_time = int(request.form.get('cook_time')) if request.form.get('cook_time') else None
        recipe.servings = int(request.form.get('servings')) if request.form.get('servings') else None
        recipe.category = request.form.get('category')

        db.session.commit()
        flash('Recipe updated successfully!', 'success')
        return redirect(url_for('recipe_detail', recipe_id=recipe_id))

    return render_template('edit_recipe.html', recipe=recipe)


@app.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    """Delete a recipe - only by the author"""
    recipe = Recipe.query.get_or_404(recipe_id)

    # Check if current user is the author
    if recipe.user_id != session['user_id']:
        flash('You can only delete your own recipes.', 'danger')
        return redirect(url_for('recipe_detail', recipe_id=recipe_id))

    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted successfully.', 'info')
    return redirect(url_for('profile'))


# Database initialization
def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")


# Main execution
if __name__ == '__main__':
    # Create database tables if they don't exist
    if not os.path.exists('instance/recipes.db'):
        with app.app_context():
            db.create_all()
            print("Database created successfully!")

    # Run the application
    app.run(debug=True)