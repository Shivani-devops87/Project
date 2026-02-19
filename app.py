from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Vegetable classes for the classification model
VEGETABLE_CLASSES = [
    'Bean', 'Bitter_Gourd', 'Bottle_Gourd', 'Brinjal', 'Broccoli',
    'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Cucumber',
    'Papaya', 'Potato', 'Pumpkin', 'Radish', 'Tomato'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Save the uploaded file
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # For now, return a demo prediction
        # TODO: Load and use the actual trained model
        import random
        predicted_class = random.choice(VEGETABLE_CLASSES)
        confidence = round(random.uniform(0.75, 0.99), 2)
        
        return render_template('prediction.html', 
                             prediction=predicted_class,
                             confidence=confidence,
                             image_path=f'uploads/{filename}')
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    print("=" * 60)
    print("🌱 GreenClassify Deep Learning - Vegetable Classifier")
    print("=" * 60)
    print("📍 Server starting at: http://127.0.0.1:5000")
    print("📂 Upload folder:", UPLOAD_FOLDER)
    print("🎯 Supported vegetables:", len(VEGETABLE_CLASSES))
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
