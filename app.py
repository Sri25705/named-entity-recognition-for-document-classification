from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os
import spacy
from utils.model_training import train_model
from utils.emailservice import send_email
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from datetime import timedelta
from PyPDF2 import PdfReader
from docx import Document

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for session management
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=30)

db.init_app(app)

# Initialize SpaCy NER model
nlp = spacy.load("en_core_web_sm")

# Set upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid login credentials', 'danger')
    return render_template('login.html')

# Route for the register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error registering user: {e}")
            flash('Error during registration.', 'danger')
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')


# Route for the dashboard page
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

# Route for uploading documents
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected.', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected.', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                # Process document and extract entities
                entities = process_document(file_path)
                if not entities:
                    flash('No entities found in the document.', 'info')
                return render_template('highlight.html', text=entities)
            except Exception as e:
                print(f"Error processing document: {e}")
                flash('Error processing document.', 'danger')
        else:
            flash('Invalid file type.', 'danger')
    return render_template('upload.html')

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to process documents
def process_document(filepath):
    try:
        # Extract text based on file type
        if filepath.endswith('.pdf'):
            reader = PdfReader(filepath)
            text = "".join(page.extract_text() for page in reader.pages if page.extract_text())
        elif filepath.endswith('.docx'):
            doc = Document(filepath)
            text = "\n".join(para.text for para in doc.paragraphs if para.text.strip())
        else:
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()

        if not text.strip():
            return ["No text found in the document."]

        # Perform NER using spaCy
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents if ent.text.strip()]
        return entities if entities else ["No entities found."]
    except Exception as e:
        print(f"Error extracting text or performing NER: {e}")
        return ["Error processing the document."]

# Main function to run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="127.0.0.1", port=5000)
