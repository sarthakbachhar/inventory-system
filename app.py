import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, Product
from datetime import datetime
import uuid
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key'

# File Upload Config
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
            
        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template('dashboard.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        try:
            if not all([request.form.get('name'), request.form.get('price'), request.form.get('quantity')]):
                flash('Please fill all required fields', 'error')
                return redirect(url_for('add_product'))

            if 'image' not in request.files:
                flash('No file uploaded', 'error')
                return redirect(request.url)
                
            file = request.files['image']
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)
                
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{uuid.uuid4()}.{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                product = Product(
                    name=request.form['name'],
                    price=float(request.form['price']),
                    quantity=int(request.form['quantity']),
                    description=request.form.get('description', ''),
                    image=filename,
                    created_at=datetime.utcnow()
                )
                db.session.add(product)
                db.session.commit()
                flash('Product added successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Allowed file types are: png, jpg, jpeg, gif', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            
    return render_template('add_product.html')

@app.route('/delete/<int:id>')
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        if product.image:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
            if os.path.exists(filepath):
                os.remove(filepath)
        
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting product: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/initdb')
def initdb():
    with app.app_context():
        db.create_all()
        
        if not User.query.filter_by(username='admin').first():
            hashed = generate_password_hash("admin123", method='sha256')
            admin = User(username='admin', password=hashed, is_admin=True)
            db.session.add(admin)
            db.session.commit()
            
    return "Database initialized with admin user (username: admin, password: admin123)"

if __name__ == "__main__":
    app.run(debug=os.environ.get('FLASK_DEBUG', False))
