from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from datetime import datetime
import json
import os
from werkzeug.utils import secure_filename
from nlp import process_query, ask_ai_question, detect_intent, analyze_image
from models import init_db, add_task, get_tasks, delete_task, update_task

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Configure upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize database on startup
init_db()

@app.route('/')
def index():
    """Main page showing the assistant interface and current tasks/reminders"""
    try:
        tasks = get_tasks()
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        print(f"❌ Error loading index page: {e}")
        return render_template('index.html', tasks=[])

@app.route('/process', methods=['POST'])
def process():
    """Process user query and return appropriate response"""
    try:
        user_input = request.json.get('query', '').strip()
        
        if not user_input:
            return jsonify({'error': 'No query provided'}), 400
        
        # Process the query using NLP
        response = process_query(user_input)
        
        # Refresh tasks list for the frontend
        tasks = get_tasks()
        
        return jsonify({
            'response': response,
            'tasks': tasks
        })
    
    except Exception as e:
        print(f"❌ Error in process route: {e}")
        return jsonify({'error': 'Sorry, I encountered an error processing your request. Please try again.'}), 500

@app.route('/ask', methods=['POST'])
def ask():
    """Handle AI questions and task/reminder requests"""
    try:
        user_input = request.json.get('query', '').strip()
        
        if not user_input:
            return jsonify({'error': 'No query provided'}), 400
        
        # Check if it's a task/reminder request
        intent = detect_intent(user_input)
        
        if intent in ['reminder', 'schedule']:
            # Handle as task/reminder using existing logic
            response = process_query(user_input)
            tasks = get_tasks()
            return jsonify({
                'reply': response,
                'tasks': tasks,
                'type': 'task_action'
            })
        else:
            # Handle as AI question
            ai_response = ask_ai_question(user_input)
            return jsonify({
                'reply': ai_response,
                'type': 'ai_response'
            })
    
    except Exception as e:
        print(f"❌ Error in ask route: {e}")
        return jsonify({'error': 'Sorry, I encountered an error processing your request. Please try again.'}), 500

@app.route('/analyze_image', methods=['POST'])
def analyze_image_route():
    """Handle image upload and analysis"""
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP, WEBP'}), 400
        
        # Get optional text prompt
        prompt = request.form.get('prompt', 'Describe this image in detail.')
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze the image
        analysis_result = analyze_image(filepath, prompt)
        
        # Clean up the uploaded file after analysis
        try:
            os.remove(filepath)
        except:
            pass  # Don't fail if cleanup fails
        
        return jsonify({
            'reply': analysis_result,
            'type': 'image_analysis'
        })
    
    except Exception as e:
        print(f"❌ Error in analyze_image route: {e}")
        return jsonify({'error': 'Sorry, I encountered an error analyzing the image. Please try again.'}), 500

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    """Delete a specific task/reminder"""
    try:
        success = delete_task(task_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        print(f"❌ Error deleting task: {e}")
        return jsonify({'error': 'Failed to delete task'}), 500

@app.route('/update_task/<int:task_id>', methods=['PUT'])
def update_task_route(task_id):
    """Update a specific task/reminder"""
    try:
        data = request.json
        new_content = data.get('content')
        new_datetime = data.get('datetime')
        
        if not new_content and not new_datetime:
            return jsonify({'error': 'No content or datetime provided'}), 400
        
        success = update_task(task_id, new_content, new_datetime)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Task not found'}), 404
    except Exception as e:
        print(f"❌ Error updating task: {e}")
        return jsonify({'error': 'Failed to update task'}), 500

@app.route('/test')
def test():
    """Test route to check if templates are working"""
    return "<h1>Flask is working!</h1><p>Template directory exists and Flask is serving content.</p>"

@app.route('/testtemplate')
def test_template():
    """Test route with minimal template"""
    tasks = get_tasks()
    return render_template('test.html', tasks=tasks)

if __name__ == '__main__':
    print("🤖 Aditya AI starting...")
    print("📱 Open http://localhost:8000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=8000)
