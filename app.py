import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from config import config_by_name
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config_by_name[os.environ.get('FLASK_ENV', 'dev')])

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ==================== MODELS ====================

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scripts = db.relationship('Script', backref='author', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

class Script(db.Model):
    __tablename__ = 'scripts'
    id = db.Column(db.Integer, primary_key=True)
    signal = db.Column(db.String(255), nullable=False)
    response = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Script {self.signal}>'

# ==================== DEFAULT SCRIPTS ====================

DEFAULT_SCRIPTS = {
    "How did you do that?": "Hey! Yeah, that's something a lot of people get stuck on. What specifically have you tried so far?",
    "Where can I learn more?": "I can definitely give you the breakdown. Just so I make sure I'm giving you the right info, what's your main goal with this?",
    "I've been struggling with this too": "I hear you—it's a frustrating spot to be in. How long has this been a challenge for you?",
    "Send me the link": "I'll drop that for you now! Are you planning to use it for your business or something else?",
    "🔥 Fire / This is exactly what I needed": "Appreciate that! Are you currently trying to improve this area?"
}

# ==================== ROUTES ====================

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == os.environ.get('PASSWORD'):
            session['logged_in'] = True
            return redirect(url_for('scriptor'))
        else:
            return render_template('login.html', error='Invalid password')
    
    return render_template('login.html')

@app.route('/scriptor')
def scriptor():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    scripts = DEFAULT_SCRIPTS
    return render_template('index.html', scripts=scripts)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/scripts', methods=['GET'])
def get_scripts():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({'scripts': DEFAULT_SCRIPTS})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('FLASK_ENV') == 'dev'
    app.run(host='0.0.0.0', port=port, debug=debug)