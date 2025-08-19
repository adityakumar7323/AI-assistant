import re
from datetime import datetime, timedelta
import os
from models import add_task

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, that's okay
    pass

# Google Gemini API setup
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
USE_GEMINI = GEMINI_API_KEY is not None

if USE_GEMINI:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Google Gemini API configured")
    except ImportError:
        print("⚠️  Google Generative AI library not installed. Using fallback responses.")
        USE_GEMINI = False
    except Exception as e:
        print(f"⚠️  Gemini configuration error: {e}. Using fallback responses.")
        USE_GEMINI = False
else:
    print("ℹ️  Using built-in responses (no Gemini API key provided)")
    model = None

def clean_user_input(text):
    """Clean and normalize user input"""
    if not text:
        return ""
    
    # Strip quotes and extra whitespace
    text = text.strip().strip('"\'')
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def extract_datetime_from_text(text):
    """Extract datetime information from natural language text"""
    text_lower = text.lower()
    now = datetime.now()
    
    # Tomorrow
    if 'tomorrow' in text_lower:
        return (now + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
    
    # Today
    if 'today' in text_lower:
        return now.replace(hour=18, minute=0, second=0, microsecond=0)
    
    # Next week
    if 'next week' in text_lower:
        return (now + timedelta(days=7)).replace(hour=9, minute=0, second=0, microsecond=0)
    
    # Time patterns (e.g., "at 3pm", "at 15:30")
    time_patterns = [
        r'at (\d{1,2}):(\d{2})',  # at 15:30
        r'at (\d{1,2})pm',        # at 3pm
        r'at (\d{1,2})am',        # at 9am
        r'(\d{1,2}):(\d{2})',     # 15:30
    ]
    
    for pattern in time_patterns:
        match = re.search(pattern, text_lower)
        if match:
            if 'pm' in pattern:
                hour = int(match.group(1))
                if hour != 12:
                    hour += 12
                return now.replace(hour=hour, minute=0, second=0, microsecond=0)
            elif 'am' in pattern:
                hour = int(match.group(1))
                if hour == 12:
                    hour = 0
                return now.replace(hour=hour, minute=0, second=0, microsecond=0)
            else:
                hour = int(match.group(1))
                minute = int(match.group(2)) if len(match.groups()) > 1 else 0
                return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    return None

def detect_intent(text):
    """Detect user intent from natural language text"""
    text_lower = text.lower()
    
    # Reminder keywords
    reminder_keywords = ['remind', 'reminder', 'remember', 'don\'t forget']
    if any(keyword in text_lower for keyword in reminder_keywords):
        return 'reminder'
    
    # Schedule/task keywords
    schedule_keywords = ['schedule', 'plan', 'appointment', 'meeting', 'task', 'todo']
    if any(keyword in text_lower for keyword in schedule_keywords):
        return 'schedule'
    
    # Question keywords
    question_keywords = ['what', 'how', 'when', 'where', 'why', 'who', 'which', '?']
    if any(keyword in text_lower for keyword in question_keywords):
        return 'question'
    
    # Default to question if unsure
    return 'question'

def extract_task_content(text, intent):
    """Extract the actual task content from the user input"""
    text_lower = text.lower()
    
    if intent == 'reminder':
        # Remove reminder keywords
        patterns = [
            r'remind me to ',
            r'remind me ',
            r'reminder to ',
            r'remember to ',
            r'don\'t forget to ',
        ]
        
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    elif intent == 'schedule':
        # Remove schedule keywords
        patterns = [
            r'schedule ',
            r'plan ',
            r'add task ',
            r'create task ',
        ]
        
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    return text.strip()

def get_predefined_answer(question):
    """Provide comprehensive predefined answers for common questions"""
    question_lower = question.lower()
    
    # AI and tech questions (detailed answers)
    if any(phrase in question_lower for phrase in ['artificial intelligence', 'what is ai', 'what ai']):
        return "Artificial Intelligence (AI) is technology that enables machines to simulate human intelligence processes like learning, reasoning, and problem-solving. AI includes machine learning, natural language processing, computer vision, and robotics. I'm an example of AI designed to help you manage tasks and answer questions!"
    
    if any(phrase in question_lower for phrase in ['machine learning', 'what is ml', 'ml is']):
        return "Machine Learning is a subset of AI where computers learn patterns from data without being explicitly programmed. It powers recommendations on Netflix, fraud detection in banking, image recognition in photos, and much more. Types include supervised learning (with labeled data), unsupervised learning (finding patterns), and reinforcement learning (learning through trial and error)."
    
    if any(phrase in question_lower for phrase in ['quantum computing', 'quantum computer']):
        return "Quantum computing uses quantum mechanical phenomena like superposition and entanglement to process information. Unlike classical bits (0 or 1), quantum bits (qubits) can exist in multiple states simultaneously, potentially solving certain problems exponentially faster than classical computers. Applications include cryptography, drug discovery, and optimization problems."
    
    if any(phrase in question_lower for phrase in ['python', 'programming python']):
        return "Python is a versatile, high-level programming language known for its readable syntax and extensive libraries. It's widely used in web development (Django, Flask), data science (pandas, numpy), AI/ML (TensorFlow, PyTorch), automation, and scientific computing. Python's philosophy emphasizes code readability and simplicity."
    
    if any(phrase in question_lower for phrase in ['javascript', 'js programming']):
        return "JavaScript is a dynamic programming language primarily used for web development. It runs in browsers to create interactive websites and also on servers (Node.js). Key features include event-driven programming, asynchronous operations with promises/async-await, and a vast ecosystem of frameworks like React, Vue, and Angular."
    
    if any(phrase in question_lower for phrase in ['blockchain', 'cryptocurrency', 'bitcoin']):
        return "Blockchain is a distributed ledger technology that maintains a continuously growing list of records (blocks) linked using cryptography. Each block contains a hash of the previous block, timestamp, and transaction data. It's the technology behind cryptocurrencies like Bitcoin and has applications in supply chain, voting systems, and smart contracts."
    
    # Science questions
    if any(phrase in question_lower for phrase in ['photosynthesis', 'how plants']):
        return "Photosynthesis is the process by which plants convert sunlight, carbon dioxide, and water into glucose and oxygen. It occurs in chloroplasts using chlorophyll. The equation is: 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂. This process is crucial for life on Earth as it produces oxygen and forms the base of food chains."
    
    if any(phrase in question_lower for phrase in ['dna', 'genetic', 'genes']):
        return "DNA (Deoxyribonucleic Acid) is the molecule that carries genetic instructions for all living organisms. It has a double helix structure made of nucleotides (A, T, G, C). Genes are specific DNA sequences that code for proteins. DNA replication, transcription to RNA, and translation to proteins form the central dogma of molecular biology."
    
    if any(phrase in question_lower for phrase in ['black hole', 'space', 'universe']):
        return "Black holes are regions of spacetime where gravity is so strong that nothing, not even light, can escape. They form when massive stars collapse. The event horizon is the 'point of no return.' Recent discoveries include gravitational waves from black hole mergers and the first image of a black hole's event horizon by the Event Horizon Telescope."
    
    # Health and wellness
    if any(phrase in question_lower for phrase in ['meditation', 'mindfulness']):
        return "Meditation is a practice that trains attention and awareness to achieve mental clarity and emotional stability. Benefits include reduced stress, improved focus, lower blood pressure, and enhanced emotional regulation. Common types include mindfulness meditation, focused breathing, body scans, and loving-kindness meditation. Even 10 minutes daily can provide benefits."
    
    if any(phrase in question_lower for phrase in ['exercise', 'fitness', 'workout']):
        return "Regular exercise provides numerous benefits: improved cardiovascular health, stronger muscles and bones, better mental health, enhanced cognitive function, and increased longevity. The WHO recommends at least 150 minutes of moderate aerobic activity weekly, plus muscle-strengthening activities twice a week."
    
    # Time and date questions
    if any(phrase in question_lower for phrase in ['what time', 'time is']):
        return f"The current time is {datetime.now().strftime('%H:%M on %B %d, %Y')}"
    
    if any(phrase in question_lower for phrase in ['what date', 'date today']):
        return f"Today is {datetime.now().strftime('%B %d, %Y')}"
    
    # Basic greetings and conversation
    if any(phrase in question_lower for phrase in ['hello', 'hi there', 'hey there']) or question_lower.strip() in ['hi', 'hello', 'hey']:
        return "Hello! I'm Aditya AI, your AI assistant. I can help you set reminders, schedule tasks, and answer questions on topics like technology, science, health, and more."
    
    if any(phrase in question_lower for phrase in ['how are you', 'how do you feel']):
        return "I'm doing great! Ready to help you with your tasks and questions. I have built-in knowledge on many topics and can provide detailed explanations."
    
    # Help and other questions
    if 'help' in question_lower:
        return "I can help you with:\n• Setting reminders (e.g., 'remind me to call mom tomorrow')\n• Scheduling tasks (e.g., 'schedule meeting at 3pm')\n• Answering questions about technology, science, health\n• Explaining concepts like AI, quantum computing, programming\n• Managing your tasks and reminders"
    
    if 'weather' in question_lower:
        return "I don't have access to real-time weather data, but you can check your local weather app or websites like weather.com or weather.gov for current conditions and forecasts."
    
    # More comprehensive fallback
    return "I have built-in knowledge on topics like technology (AI, programming, quantum computing), science (biology, physics, space), health (exercise, meditation), and general knowledge. I can also help you set reminders and schedule tasks. What would you like to know about?"

def query_gemini(question):
    """Query Google Gemini API for smart answers"""
    if not USE_GEMINI or not model:
        return None
    
    try:
        # Create the prompt for Gemini
        prompt = f"You are Aditya AI, a helpful personal assistant. Provide concise, helpful answers. Keep responses under 100 words unless the user specifically asks for detailed information.\n\nUser question: {question}"
        
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            return None
    
    except Exception as e:
        error_str = str(e)
        if "quota" in error_str.lower() or "limit" in error_str.lower():
            print(f"❌ Gemini API quota exceeded: {e}")
            return "quota_exceeded"  # Special indicator for quota issues
        elif "403" in error_str or "api key" in error_str.lower():
            print(f"❌ Gemini API authentication error: {e}")
            return "auth_error"
        else:
            print(f"❌ Gemini API error: {e}")
            return None

def process_query(user_input):
    """Main function to process user queries and return appropriate responses"""
    try:
        # Clean and validate input
        cleaned_input = clean_user_input(user_input)
        if not cleaned_input:
            return "Please provide a valid message."
        
        # Detect intent
        intent = detect_intent(cleaned_input)
        
        if intent in ['reminder', 'schedule']:
            # Extract task content
            content = extract_task_content(cleaned_input, intent)
            
            if not content:
                return "I couldn't understand what you want me to remind you about. Could you be more specific?"
            
            # Extract datetime if available
            task_datetime = extract_datetime_from_text(cleaned_input)
            datetime_str = task_datetime.isoformat() if task_datetime else None
            
            # Add to database
            task_id = add_task(content, intent, datetime_str)
            
            if task_id is None:
                return "Sorry, I couldn't save your task right now. Please try again."
            
            # Create response
            if task_datetime:
                formatted_time = task_datetime.strftime('%B %d, %Y at %H:%M')
                return f"✅ {intent.capitalize()} set: '{content}' for {formatted_time}"
            else:
                return f"✅ {intent.capitalize()} added: '{content}'"
        
        elif intent == 'question':
            # Try Gemini first, then fallback to predefined answers
            answer = query_gemini(cleaned_input) if USE_GEMINI else None
            
            if answer:
                return f"🤖 {answer}"
            else:
                return f"💡 {get_predefined_answer(cleaned_input)}"
        
        else:
            return "I'm not sure how to help with that. Try asking me to set a reminder, schedule a task, or ask a question!"
    
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        return "Sorry, I encountered an error processing your request. Please try again."

def ask_ai_question(user_input):
    """Handle questions that should be sent to Gemini API"""
    try:
        # Clean input
        cleaned_input = clean_user_input(user_input)
        if not cleaned_input:
            return "Please provide a valid question."
        
        # Try Gemini first
        if USE_GEMINI and model:
            ai_response = query_gemini(cleaned_input)
            if ai_response == "quota_exceeded":
                return "⚠️ Gemini API quota exceeded. Using built-in knowledge: " + get_predefined_answer(cleaned_input)
            elif ai_response == "auth_error":
                return "⚠️ Gemini API authentication issue. Using built-in knowledge: " + get_predefined_answer(cleaned_input)
            elif ai_response:
                return ai_response
        
        # Fallback to predefined answers
        predefined_answer = get_predefined_answer(cleaned_input)
        if "I have built-in knowledge" not in predefined_answer:
            return predefined_answer
        
        # Final fallback with helpful message
        return f"💡 Using built-in knowledge: {predefined_answer}"
    
    except Exception as e:
        print(f"❌ Error in ask_ai_question: {e}")
        return "Sorry, I'm having trouble answering that right now."

def analyze_image(image_path, prompt="Describe this image in detail."):
    """Analyze an image using Google Gemini Vision"""
    try:
        if not USE_GEMINI or not model:
            return "⚠️ Image analysis requires Gemini API. Using text description: I can see you've uploaded an image, but I need Gemini API access to analyze it. Please ensure your API key is configured."
        
        # Import PIL for image handling
        try:
            from PIL import Image
        except ImportError:
            return "⚠️ Image processing requires Pillow library. Please install it with: pip install Pillow"
        
        # Load and prepare the image
        try:
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Create a comprehensive prompt for image analysis
            full_prompt = f"""You are Aditya AI, an AI assistant analyzing an image. {prompt}

Please provide a helpful and detailed response that includes:
1. What you see in the image
2. Any text or important details
3. Context or insights about the image
4. Any questions the user might have about what's shown

Be conversational and helpful in your response."""

            # Use Gemini vision model to analyze the image
            response = model.generate_content([full_prompt, image])
            
            if response.text:
                return f"🖼️ **Image Analysis**: {response.text.strip()}"
            else:
                return "⚠️ I couldn't analyze this image. Please try uploading a different image or check if it's a valid image format."
                
        except Exception as img_error:
            print(f"❌ Image processing error: {img_error}")
            return f"⚠️ Error processing the image: {str(img_error)}. Please try a different image format or size."
    
    except Exception as e:
        error_str = str(e)
        if "quota" in error_str.lower() or "limit" in error_str.lower():
            print(f"❌ Gemini API quota exceeded for image analysis: {e}")
            return "⚠️ Gemini API quota exceeded for image analysis. Please try again later or check your API usage."
        elif "403" in error_str or "api key" in error_str.lower():
            print(f"❌ Gemini API authentication error for image analysis: {e}")
            return "⚠️ Gemini API authentication issue. Please check your API key configuration."
        else:
            print(f"❌ Gemini image analysis error: {e}")
            return "⚠️ Sorry, I encountered an error analyzing the image. Please try again."
