from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
from PIL import Image
import os
from werkzeug.utils import secure_filename
import io
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'aditya-ai-secret-key-2024'

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=GEMINI_API_KEY)

# Initialize models
text_model = genai.GenerativeModel('gemini-1.5-flash')
vision_model = genai.GenerativeModel('gemini-1.5-flash')

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Serve the main AI chat interface with fixed galaxy background"""
    return render_template('ai_chat_fixed.html')

@app.route('/galaxy')
def galaxy():
    """Serve the galaxy AI chat interface"""
    return render_template('ai_chat_galaxy.html')

@app.route('/classic')
def classic():
    """Serve the classic AI chat interface"""
    return render_template('ai_chat.html')

@app.route('/video-selector')
def video_selector():
    """Serve the galaxy video selector interface"""
    return render_template('galaxy_video_selector.html')

@app.route('/api/select-galaxy-video', methods=['POST'])
def select_galaxy_video():
    """API endpoint to select galaxy video"""
    try:
        data = request.get_json()
        video_type = data.get('type', 'enhanced')
        
        import shutil
        import os
        
        video_dir = os.path.join(app.static_folder, 'videos')
        
        if video_type == 'simple':
            source = os.path.join(video_dir, 'galaxy_simple.mp4')
        else:  # enhanced
            source = os.path.join(video_dir, 'galaxy_enhanced.mp4') if os.path.exists(os.path.join(video_dir, 'galaxy_enhanced.mp4')) else os.path.join(video_dir, 'galaxy.mp4')
        
        target = os.path.join(video_dir, 'galaxy.mp4')
        
        if os.path.exists(source):
            # Backup current galaxy.mp4 if it's different
            if video_type == 'simple' and os.path.exists(target):
                shutil.copy2(target, os.path.join(video_dir, 'galaxy_enhanced.mp4'))
            
            shutil.copy2(source, target)
            return jsonify({'success': True, 'message': f'{video_type} video selected'})
        else:
            return jsonify({'error': f'{video_type} video not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Handle text-based AI conversations"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get conversation history from session
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        # Generate AI response
        response = text_model.generate_content(user_message)
        ai_response = response.text
        
        # Store in chat history
        session['chat_history'].append({
            'user': user_message,
            'ai': ai_response
        })
        
        # Keep only last 10 conversations to avoid session bloat
        if len(session['chat_history']) > 10:
            session['chat_history'] = session['chat_history'][-10:]
        
        return jsonify({
            'response': ai_response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': f'AI Error: {str(e)}'}), 500

@app.route('/chat_with_image', methods=['POST'])
def chat_with_image():
    """Handle AI conversations with image analysis"""
    try:
        # Get text prompt
        prompt = request.form.get('prompt', 'Analyze this image')
        
        # Check if image was uploaded
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload an image.'}), 400
        
        # Process image with PIL
        try:
            image = Image.open(io.BytesIO(file.read()))
            
            # Generate AI response with image
            response = vision_model.generate_content([prompt, image])
            ai_response = response.text
            
            # Save image for reference
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.seek(0)
            file.save(filepath)
            
            return jsonify({
                'response': ai_response,
                'image_info': {
                    'filename': filename,
                    'size': f"{image.size[0]}x{image.size[1]}",
                    'format': image.format
                },
                'status': 'success'
            })
            
        except Exception as img_error:
            return jsonify({'error': f'Image processing error: {str(img_error)}'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/get_history')
def get_history():
    """Get chat history"""
    history = session.get('chat_history', [])
    return jsonify({'history': history})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear chat history"""
    session['chat_history'] = []
    return jsonify({'status': 'success', 'message': 'Chat history cleared'})

if __name__ == '__main__':
    print("🤖 Aditya AI - Galaxy ChatGPT Interface")
    print("🌐 Open http://localhost:3001")
    print("✨ Features: Chat, Voice Input, Image Analysis, Galaxy Sidebar")
    app.run(debug=True, host='0.0.0.0', port=3001)
