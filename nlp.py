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

# API Configuration
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Determine which API to use (prioritize APIs that are working)
USE_DEEPSEEK = DEEPSEEK_API_KEY is not None
USE_OPENAI = OPENAI_API_KEY is not None
USE_GEMINI = GEMINI_API_KEY is not None

# Initialize clients if keys are available
deepseek_client = None
openai_client = None
gemini_client = None

# DeepSeek API setup
if USE_DEEPSEEK:
    try:
        from openai import OpenAI
        deepseek_client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
        print("✅ DeepSeek API configured")
    except ImportError:
        print("⚠️  OpenAI library not installed. DeepSeek will not be available.")
        USE_DEEPSEEK = False
    except Exception as e:
        print(f"⚠️  DeepSeek configuration error: {e}.")
        USE_DEEPSEEK = False

# OpenAI API setup
if USE_OPENAI:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("✅ OpenAI API configured")
    except ImportError:
        print("⚠️  OpenAI library not installed.")
        USE_OPENAI = False
    except Exception as e:
        print(f"⚠️  OpenAI configuration error: {e}.")
        USE_OPENAI = False

# Gemini API setup
if USE_GEMINI:
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_client = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini API configured")
    except ImportError:
        print("⚠️  Google Generative AI library not installed. Run: pip install google-generativeai")
        USE_GEMINI = False
    except Exception as e:
        print(f"⚠️  Gemini configuration error: {e}.")
        USE_GEMINI = False

if not USE_DEEPSEEK and not USE_OPENAI and not USE_GEMINI:
    print("ℹ️  Using built-in responses (no API keys provided or configured)")
else:
    available_apis = []
    if USE_DEEPSEEK: available_apis.append("DeepSeek")
    if USE_OPENAI: available_apis.append("OpenAI")
    if USE_GEMINI: available_apis.append("Gemini")
    print(f"🤖 Available APIs: {', '.join(available_apis)}")

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
    
    # Enhanced AI and tech questions
    if any(phrase in question_lower for phrase in ['artificial intelligence', 'what is ai', 'what ai', 'ai is']):
        return "🤖 Artificial Intelligence (AI) enables machines to simulate human intelligence through learning, reasoning, and problem-solving. AI includes machine learning, natural language processing, computer vision, and robotics. Modern AI powers virtual assistants, recommendation systems, autonomous vehicles, and medical diagnostics. I'm an example of AI designed to help you manage tasks and answer questions intelligently!"
    
    if any(phrase in question_lower for phrase in ['machine learning', 'what is ml', 'ml is', 'deep learning']):
        return "🧠 Machine Learning is AI that learns patterns from data without explicit programming. It powers Netflix recommendations, fraud detection, image recognition, and language translation. Types include: Supervised (labeled data), Unsupervised (pattern finding), and Reinforcement (trial-and-error). Deep Learning uses neural networks to process complex data like images and speech."
    
    if any(phrase in question_lower for phrase in ['python programming', 'python', 'learn python']):
        return "🐍 Python is a versatile, beginner-friendly programming language known for readable syntax. It's used in web development (Django/Flask), data science (pandas/numpy), AI/ML (TensorFlow/PyTorch), automation, and scientific computing. Start with basics: variables, functions, loops, then explore libraries for your interests!"
    
    if any(phrase in question_lower for phrase in ['javascript', 'js programming', 'web development']):
        return "💻 JavaScript powers interactive websites and web applications. It runs in browsers (frontend) and servers (Node.js backend). Key concepts: variables, functions, DOM manipulation, async/await, and frameworks like React, Vue, Angular. Essential for modern web development!"
    
    if any(phrase in question_lower for phrase in ['blockchain', 'cryptocurrency', 'bitcoin', 'crypto']):
        return "⛓️ Blockchain is a distributed ledger technology using cryptographic hashing to secure transaction records. Each block contains previous block's hash, creating an immutable chain. Applications: cryptocurrencies (Bitcoin, Ethereum), smart contracts, supply chain tracking, and decentralized finance (DeFi)."
    
    # Enhanced productivity and work questions
    if any(phrase in question_lower for phrase in ['productivity', 'time management', 'organize', 'be productive', 'more productive', 'productive tips']):
        return "⏰ Boost productivity with: 1) Time blocking - schedule specific tasks, 2) Pomodoro Technique - 25min focused work + 5min breaks, 3) GTD system - capture, clarify, organize, reflect, engage, 4) Eliminate distractions - phone notifications off, 5) Prioritize with Eisenhower Matrix (urgent/important)."
    
    if any(phrase in question_lower for phrase in ['study tips', 'learning', 'how to learn']):
        return "📚 Effective learning strategies: 1) Active recall - test yourself frequently, 2) Spaced repetition - review at increasing intervals, 3) Feynman Technique - explain concepts simply, 4) Practice retrieval over re-reading, 5) Create connections between new and existing knowledge, 6) Take breaks for memory consolidation."
    
    # Health and wellness
    if any(phrase in question_lower for phrase in ['meditation', 'mindfulness', 'stress relief']):
        return "🧘 Meditation reduces stress, improves focus, and enhances emotional well-being. Start with 5-10 minutes daily: 1) Find quiet space, 2) Focus on breathing, 3) Notice when mind wanders, 4) Gently return attention to breath. Apps like Headspace or Calm can guide beginners. Benefits include lower anxiety, better sleep, and increased concentration."
    
    if any(phrase in question_lower for phrase in ['exercise', 'fitness', 'workout', 'health']):
        return "💪 Regular exercise improves physical and mental health. WHO recommends 150 minutes moderate aerobic activity weekly plus 2 strength training sessions. Benefits: stronger heart, bones, muscles, better mood, cognitive function, sleep quality. Start small - 10-minute walks, bodyweight exercises, then gradually increase intensity."
    
    if any(phrase in question_lower for phrase in ['sleep', 'better sleep', 'insomnia']):
        return "😴 Quality sleep is crucial for health. Tips: 1) Consistent sleep schedule (same bedtime/wake time), 2) Cool, dark room (60-67°F), 3) No screens 1 hour before bed, 4) Limit caffeine after 2 PM, 5) Regular exercise (not before bed), 6) Relaxation techniques, 7) Comfortable mattress/pillows."
    
    # Science questions
    if any(phrase in question_lower for phrase in ['climate change', 'global warming', 'environment']):
        return "🌍 Climate change refers to long-term shifts in global temperatures and weather patterns. Human activities, especially fossil fuel burning, increase greenhouse gases (CO₂, methane). Effects: rising sea levels, extreme weather, ecosystem disruption. Solutions: renewable energy, energy efficiency, sustainable transportation, carbon capture."
    
    if any(phrase in question_lower for phrase in ['space', 'universe', 'astronomy', 'stars']):
        return "🌌 The universe is approximately 13.8 billion years old and contains billions of galaxies, each with billions of stars. Recent discoveries include gravitational waves, exoplanets in habitable zones, and images of black holes. Space exploration continues with Mars rovers, James Webb Space Telescope, and plans for lunar bases."
    
    # Personal development
    if any(phrase in question_lower for phrase in ['career advice', 'job search', 'career']):
        return "🚀 Career development tips: 1) Identify your strengths and interests, 2) Develop both technical and soft skills, 3) Network genuinely - help others first, 4) Seek mentorship and feedback, 5) Embrace continuous learning, 6) Build an online presence (LinkedIn, portfolio), 7) Practice interviewing, 8) Consider side projects to showcase skills."
    
    if any(phrase in question_lower for phrase in ['communication', 'public speaking', 'presentation']):
        return "🗣️ Effective communication skills: 1) Listen actively - understand before seeking to be understood, 2) Be clear and concise, 3) Use storytelling for engagement, 4) Practice empathy, 5) Ask thoughtful questions, 6) For presentations: know your audience, practice extensively, use visuals effectively, manage nerves through preparation."
    
    # Technology trends
    if any(phrase in question_lower for phrase in ['future technology', 'tech trends', 'innovation']):
        return "🚀 Emerging tech trends: 1) AI & Machine Learning automation, 2) Quantum computing breakthroughs, 3) Extended Reality (AR/VR/MR), 4) 5G and edge computing, 5) Internet of Things (IoT) expansion, 6) Sustainable technology solutions, 7) Biotechnology advances, 8) Autonomous systems. These will reshape work, communication, and daily life."
    
    # Creative and hobbies
    if any(phrase in question_lower for phrase in ['creative', 'creativity', 'art', 'drawing']):
        return "🎨 Boost creativity: 1) Set aside dedicated creative time, 2) Try new experiences and perspectives, 3) Practice regularly - skill enables creativity, 4) Embrace failure as learning, 5) Collaborate with others, 6) Study masters in your field, 7) Take breaks for inspiration, 8) Keep a creative journal or sketchbook."
    
    # Time and date questions
    if any(phrase in question_lower for phrase in ['what time', 'time is', 'current time']):
        return f"⏰ Current time: {datetime.now().strftime('%I:%M %p on %A, %B %d, %Y')}"
    
    if any(phrase in question_lower for phrase in ['what date', 'date today', 'today']):
        return f"📅 Today is {datetime.now().strftime('%A, %B %d, %Y')}"
    
    # Basic greetings and conversation
    if any(phrase in question_lower for phrase in ['hello', 'hi there', 'hey there', 'good morning', 'good afternoon']) or question_lower.strip() in ['hi', 'hello', 'hey']:
        return "👋 Hello! I'm Aditya AI, your intelligent assistant. I can help you set reminders, schedule tasks, answer questions on technology, science, health, productivity, and much more. What would you like to know or accomplish today?"
    
    if any(phrase in question_lower for phrase in ['how are you', 'how do you feel', 'what\'s up']):
        return "😊 I'm doing excellent and ready to help! I have extensive built-in knowledge and can assist with tasks, answer questions, and provide detailed explanations on many topics. How can I assist you today?"
    
    if any(phrase in question_lower for phrase in ['thank you', 'thanks', 'appreciate']):
        return "🙏 You're very welcome! I'm here to help whenever you need assistance. Feel free to ask me anything or set up reminders and tasks!"
    
    # Help and capabilities
    if 'help' in question_lower or 'what can you do' in question_lower:
        return "🔧 I can help you with:\n• 📝 Setting reminders ('remind me to call mom tomorrow')\n• 📅 Scheduling tasks ('schedule meeting at 3pm')\n• 🤖 Technology & programming questions\n• 🧪 Science explanations\n• 💪 Health & wellness advice\n• 📚 Learning & productivity tips\n• 🚀 Career guidance\n• 🎨 Creative inspiration\n\nJust ask me anything!"
    
    # Fallback for unmatched questions
    if '?' in question or any(word in question_lower for word in ['what', 'how', 'why', 'when', 'where', 'who']):
        return f"🤔 That's an interesting question about '{question}'. While I have extensive built-in knowledge, I may not have specific information about this topic. I can help with technology, science, health, productivity, learning, and general questions. Could you try rephrasing or ask about a related topic I might know?"
    
    # Default friendly response
    return "💡 I'm here to help! I have knowledge about technology, science, health, productivity, learning, and many other topics. I can also help you set reminders and schedule tasks. What would you like to know or do?"
    
    # More comprehensive fallback
    return "I have built-in knowledge on topics like technology (AI, programming, quantum computing), science (biology, physics, space), health (exercise, meditation), and general knowledge. I can also help you set reminders and schedule tasks. What would you like to know about?"

def query_deepseek(question):
    """Query DeepSeek API for smart answers"""
    if not USE_DEEPSEEK or not deepseek_client:
        return None
    
    try:
        # Create the prompt for DeepSeek
        messages = [
            {"role": "system", "content": "You are Aditya AI, a helpful personal assistant. Provide concise, helpful answers. Keep responses under 100 words unless the user specifically asks for detailed information."},
            {"role": "user", "content": question}
        ]
        
        response = deepseek_client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            return None
    
    except Exception as e:
        error_str = str(e)
        if "402" in error_str or "Insufficient Balance" in error_str or "billing" in error_str.lower():
            print(f"❌ DeepSeek API billing error: {e}")
            return "billing_error"  # Special indicator for billing issues
        elif "quota" in error_str.lower() or "limit" in error_str.lower():
            print(f"❌ DeepSeek API quota/limit error: {e}")
            return "quota_exceeded"  # Special indicator for quota issues
        elif "401" in error_str or "api key" in error_str.lower() or "unauthorized" in error_str.lower():
            print(f"❌ DeepSeek API authentication error: {e}")
            return "auth_error"
        else:
            print(f"❌ DeepSeek API error: {e}")
            return None

def query_openai(question):
    """Query OpenAI API for smart answers"""
    if not USE_OPENAI or not openai_client:
        return None
    
    try:
        # Create the prompt for OpenAI
        messages = [
            {"role": "system", "content": "You are Aditya AI, a helpful personal assistant. Provide concise, helpful answers. Keep responses under 100 words unless the user specifically asks for detailed information."},
            {"role": "user", "content": question}
        ]
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            return None
    
    except Exception as e:
        error_str = str(e)
        if "quota" in error_str.lower() or "limit" in error_str.lower() or "billing" in error_str.lower():
            print(f"❌ OpenAI API quota/billing error: {e}")
            return "quota_exceeded"  # Special indicator for quota issues
        elif "401" in error_str or "api key" in error_str.lower() or "unauthorized" in error_str.lower():
            print(f"❌ OpenAI API authentication error: {e}")
            return "auth_error"
        else:
            print(f"❌ OpenAI API error: {e}")
            return None

def query_gemini(question):
    """Query Gemini API for smart answers"""
    if not USE_GEMINI or not gemini_client:
        return None
    
    try:
        # Create the prompt for Gemini
        prompt = f"""You are Aditya AI, a helpful personal assistant. Provide concise, helpful answers. Keep responses under 100 words unless the user specifically asks for detailed information.

User question: {question}"""
        
        response = gemini_client.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            return None
    
    except Exception as e:
        error_str = str(e)
        if "quota" in error_str.lower() or "limit" in error_str.lower() or "billing" in error_str.lower():
            print(f"❌ Gemini API quota/billing error: {e}")
            return "quota_exceeded"  # Special indicator for quota issues
        elif "401" in error_str or "api key" in error_str.lower() or "unauthorized" in error_str.lower():
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
            # Try DeepSeek first, then OpenAI, then Gemini, then use built-in knowledge
            answer = query_deepseek(cleaned_input) if USE_DEEPSEEK else None
            
            # Fallback to OpenAI if DeepSeek fails or has issues
            if not answer or answer in ["quota_exceeded", "auth_error", "billing_error"]:
                if USE_OPENAI:
                    answer = query_openai(cleaned_input)
            
            # Fallback to Gemini if both DeepSeek and OpenAI fail or have issues
            if not answer or answer in ["quota_exceeded", "auth_error", "billing_error"]:
                if USE_GEMINI:
                    answer = query_gemini(cleaned_input)
            
            # Use enhanced built-in knowledge if all APIs fail
            if answer and answer not in ["quota_exceeded", "auth_error", "billing_error"]:
                return f"🤖 {answer}"
            else:
                return get_predefined_answer(cleaned_input)
        
        else:
            return "I'm not sure how to help with that. Try asking me to set a reminder, schedule a task, or ask a question!"
    
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        return "Sorry, I encountered an error processing your request. Please try again."

def ask_ai_question(user_input):
    """Handle questions that should be sent to AI APIs (DeepSeek or OpenAI)"""
    try:
        # Clean input
        cleaned_input = clean_user_input(user_input)
        if not cleaned_input:
            return "Please provide a valid question."
        
        # Try DeepSeek first if available
        if USE_DEEPSEEK and deepseek_client:
            ai_response = query_deepseek(cleaned_input)
            if ai_response and ai_response not in ["quota_exceeded", "auth_error", "billing_error"]:
                return ai_response
            elif ai_response == "billing_error":
                print("⚠️ DeepSeek has insufficient balance, switching to built-in knowledge")
            elif ai_response == "quota_exceeded":
                print("⚠️ DeepSeek API quota exceeded, switching to built-in knowledge")
            elif ai_response == "auth_error":
                print("⚠️ DeepSeek API authentication issue, switching to built-in knowledge")
        
        # Try OpenAI if DeepSeek fails or isn't available
        if USE_OPENAI and openai_client:
            ai_response = query_openai(cleaned_input)
            if ai_response and ai_response not in ["quota_exceeded", "auth_error"]:
                return ai_response
            elif ai_response == "quota_exceeded":
                print("⚠️ OpenAI API quota exceeded, trying Gemini...")
            elif ai_response == "auth_error":
                print("⚠️ OpenAI API authentication issue, trying Gemini...")
        
        # Try Gemini if both DeepSeek and OpenAI fail or aren't available
        if USE_GEMINI and gemini_client:
            ai_response = query_gemini(cleaned_input)
            if ai_response and ai_response not in ["quota_exceeded", "auth_error"]:
                return ai_response
            elif ai_response == "quota_exceeded":
                print("⚠️ Gemini API quota exceeded, using built-in knowledge")
            elif ai_response == "auth_error":
                print("⚠️ Gemini API authentication issue, using built-in knowledge")
        
        # Use enhanced built-in knowledge - no error messages shown to user
        predefined_answer = get_predefined_answer(cleaned_input)
        return predefined_answer
    
    except Exception as e:
        print(f"❌ Error in ask_ai_question: {e}")
        # Even on exception, provide helpful built-in response
        return get_predefined_answer(user_input)

def analyze_image(image_path, prompt="Describe this image in detail."):
    """Analyze an image using DeepSeek or OpenAI Vision APIs"""
    try:
        # Import PIL for image handling
        try:
            from PIL import Image
        except ImportError:
            return "⚠️ Image processing requires Pillow library. Please install it with: pip install Pillow"
        
        # Try DeepSeek first if available (DeepSeek doesn't have vision yet, so we'll use OpenAI for images)
        # Try OpenAI for image analysis since DeepSeek doesn't support vision yet
        if USE_OPENAI and openai_client:
            try:
                import base64
                import io
                
                # Load and prepare the image
                image = Image.open(image_path)
                
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Convert image to base64
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                # Create the prompt for OpenAI Vision
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"""You are Aditya AI, an AI assistant analyzing an image. {prompt}

Please provide a helpful and detailed response that includes:
1. What you see in the image
2. Any text or important details
3. Context or insights about the image
4. Any questions the user might have about what's shown

Be conversational and helpful in your response."""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_base64}"
                                }
                            }
                        ]
                    }
                ]
                
                response = openai_client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=messages,
                    max_tokens=300
                )
                
                if response.choices and response.choices[0].message.content:
                    return f"🖼️ **Image Analysis**: {response.choices[0].message.content.strip()}"
                    
            except Exception as openai_error:
                print(f"❌ OpenAI vision error: {openai_error}")
        
        # If DeepSeek is available but no OpenAI for vision, provide text-based analysis
        if USE_DEEPSEEK and deepseek_client and not (USE_OPENAI and openai_client):
            return f"🖼️ **Image Analysis**: I can see you've uploaded an image, but DeepSeek doesn't currently support image analysis. I can help you with text-based questions about the image if you describe what you see!"
        
        # If neither API is available
        return "⚠️ Image analysis requires either OpenAI API for vision support. Using text description: I can see you've uploaded an image, but I need API access to analyze it. Please ensure your API keys are configured."
    
    except Exception as e:
        error_str = str(e)
        if "quota" in error_str.lower() or "limit" in error_str.lower():
            print(f"❌ API quota exceeded for image analysis: {e}")
            return "⚠️ API quota exceeded for image analysis. Please try again later or check your API usage."
        elif "403" in error_str or "401" in error_str or "api key" in error_str.lower():
            print(f"❌ API authentication error for image analysis: {e}")
            return "⚠️ API authentication issue. Please check your API key configuration."
        else:
            print(f"❌ Image analysis error: {e}")
            return "⚠️ Sorry, I encountered an error analyzing the image. Please try again."
