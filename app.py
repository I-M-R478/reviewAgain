import os
from flask import Flask, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import PyPDF2
import sqlite3
from datetime import datetime



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class StudentCopy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    extracted_text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"StudentCopy {self.file_name}"
    
with app.app_context():
    db.create_all()    

@app.route('/')
def home():
    files = StudentCopy.query.order_by(StudentCopy.upload_date.desc()).all()
    return render_template('index.html', files=files)

@app.route('/uploads', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file here", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    

    file_name = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(file_path)


    
    extracted_text = extract_text(file_path)
    student_copy = StudentCopy(file_name=file_name, extracted_text=extracted_text)
    db.session.add(student_copy)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/view/<int:file_id>')
def view_file(file_id):
    student_copy = StudentCopy.query.get_or_404(file_id)
    return render_template('review.html', file=student_copy)


def extract_text(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text    
    except Exception as e:
        return f"error pdf reading: {e}"
    

if __name__ == '__main__':
    app.run(debug=True)