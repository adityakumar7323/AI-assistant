from flask import Flask, render_template, request, jsonify
from PIL import Image
import os
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with image upload interface"""
    return render_template('upload_index.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    """Handle image upload and processing"""
    try:
        # Check if file was uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        # Check if a file was actually selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, BMP, or WEBP files only.'}), 400
        
        # Try to open and verify the image using PIL
        try:
            # Use file.stream to read the image without saving it first
            image = Image.open(io.BytesIO(file.read()))
            
            # Get image information
            width, height = image.size
            format_type = image.format
            mode = image.mode
            
            # Optionally save the file (for demonstration)
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Reset file pointer and save
            file.seek(0)
            file.save(filepath)
            
            return jsonify({
                'message': 'Image processed successfully!',
                'details': {
                    'filename': filename,
                    'width': width,
                    'height': height,
                    'format': format_type,
                    'mode': mode,
                    'size': f"{width}x{height}"
                }
            }), 200
            
        except Exception as img_error:
            return jsonify({'error': f'Invalid image file: {str(img_error)}'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

if __name__ == '__main__':
    print("🖼️  Aditya AI Image Upload Server starting...")
    print("📱 Open http://localhost:5001 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5001)
