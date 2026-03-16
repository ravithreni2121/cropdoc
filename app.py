from flask import Flask, render_template, request, redirect, url_for, session
import os
import cv2
import numpy as np

app = Flask(__name__)
app.secret_key = "ravithreni_reddy_master_2026"

# Configuration
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Translation Database for Farmers
TRANSLATIONS = {
    'en': {
        'title': 'CropDoc AI', 'welcome': 'Welcome, Ravithreni Reddy', 'login_title': 'Farmer Login',
        'user_label': 'Username', 'pass_label': 'Password', 'btn_login': 'Enter Portal',
        'select': 'Select Crop', 'btn_analyze': 'Analyze Leaf', 'severity': 'Disease Severity',
        'treatment': 'Treatment Plan', 'logout': 'Logout', 'error': 'Incorrect Details'
    },
    'te': {
        'title': 'క్రాప్ డాక్ AI', 'welcome': 'స్వాగతం, రవిత్రేణి రెడ్డి', 'login_title': 'రైతు లాగిన్',
        'user_label': 'యూజర్ నేమ్', 'pass_label': 'పాస్ వర్డ్', 'btn_login': 'ప్రవేశించండి',
        'select': 'పంటను ఎంచుకోండి', 'btn_analyze': 'ఆకును విశ్లేషించండి', 'severity': 'వ్యాధి తీవ్రత',
        'treatment': 'చికిత్స ప్రణాళిక', 'logout': 'నిష్క్రమించు', 'error': 'తప్పుడు వివరాలు'
    },
    'hi': {
        'title': 'क्रॉपडॉक AI', 'welcome': 'स्वागत है, रवित्रेणी रेड्डी', 'login_title': 'किसान लॉगिन',
        'user_label': 'उपयोगकर्ता नाम', 'pass_label': 'पासवर्ड', 'btn_login': 'प्रवेश करें',
        'select': 'फसल चुनें', 'btn_analyze': 'विश्लेषण करें', 'severity': 'रोग की गंभीरता',
        'treatment': 'उपचार योजना', 'logout': 'लॉगआउट', 'error': 'गलत विवरण'
    }
}

def analyze_leaf(image_path, crop_type, lang):
    img = cv2.imread(image_path)
    if img is None: return "Error", 0, "..."
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([10, 40, 20]), np.array([30, 255, 200]))
    severity = round((cv2.countNonZero(mask) / (img.shape[0] * img.shape[1])) * 100, 2)
    
    # Simple logic for demonstration
    if severity > 3:
        res = f"{crop_type.capitalize()} - Infected"
        treat = "Apply copper-based fungicides and isolate infected plants."
    else:
        res = f"{crop_type.capitalize()} - Healthy"
        treat = "No treatment needed. Maintain regular watering."
    return res, severity, treat

@app.route('/')
def home():
    if 'lang' not in session: session['lang'] = 'en'
    lang = session.get('lang')
    return render_template('home.html', text=TRANSLATIONS[lang], lang=lang)

@app.route('/set_lang/<lang>')
def set_lang(lang):
    session['lang'] = lang
    return redirect(request.referrer or url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = session.get('lang', 'en')
    text = TRANSLATIONS[lang]
    if request.method == 'POST':
        # VERIFIED: Ravithreni Reddy | 2107
        if request.form.get('username') == "Ravithreni Reddy" and request.form.get('password') == "2107":
            session['user'] = "Ravithreni"
            return redirect(url_for('diagnose'))
        return render_template('login.html', text=text, lang=lang, error=text['error'])
    return render_template('login.html', text=text, lang=lang)

@app.route('/diagnose', methods=['GET', 'POST'])
def diagnose():
    if 'user' not in session: return redirect(url_for('login'))
    lang = session.get('lang', 'en')
    text = TRANSLATIONS[lang]
    if request.method == 'POST':
        file = request.files.get('file')
        crop = request.form.get('crop_type')
        if file:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)
            pred, sev, treat = analyze_leaf(path, crop, lang)
            return render_template('index.html', text=text, lang=lang, prediction=pred, severity=sev, treatment=treat, image_path=path)
    return render_template('index.html', text=text, lang=lang)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
    
