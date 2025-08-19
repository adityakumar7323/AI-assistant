# 🤖 AI-Powered Personal Assistant

A minimal, lightweight AI-powered personal assistant built with Python Flask. This assistant can set reminders, schedule tasks, and answer basic questions through a clean web interface.

## ✨ Features

- **Natural Language Processing**: Understands reminders, scheduling requests, and questions
- **Task Management**: Add, view, and delete reminders and scheduled tasks  
- **Smart Responses**: Basic question answering with optional OpenAI integration
- **Clean UI**: Modern, responsive web interface
- **Lightweight**: Minimal dependencies, uses SQLite database
- **Easy Setup**: Single command to get started

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd ai-personal-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

### 4. Open Your Browser
Navigate to `http://localhost:5000`

## 💬 Usage Examples

The assistant understands natural language. Try these commands:

### Reminders
- "remind me to call mom tomorrow"
- "remind me to buy groceries"
- "don't forget to take medicine at 8pm"

### Scheduling
- "schedule meeting at 3pm"
- "plan dinner with friends tomorrow"
- "add task: finish project report"

### Questions
- "what time is it?"
- "what's today's date?"
- "how are you?"
- "help"

## 🔧 Configuration

### OpenAI Integration (Optional)
To enable smarter responses with OpenAI:

1. Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
2. Set environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
3. Install OpenAI package:
   ```bash
   pip install openai==0.28.1
   ```

### Advanced NLP (Optional)
For more sophisticated natural language processing:

```bash
pip install nltk spacy
```

## 📁 Project Structure

```
ai-personal-assistant/
├── app.py              # Main Flask application
├── models.py           # Database functions (SQLite)
├── nlp.py             # NLP processing and intent detection
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── templates/
│   └── index.html     # Web interface
└── assistant.db       # SQLite database (created automatically)
```

## 🛠 Technical Details

- **Backend**: Python Flask
- **Database**: SQLite (file-based, no setup required)
- **Frontend**: HTML/CSS/JavaScript (no frameworks)
- **NLP**: Keyword-based intent detection with regex patterns
- **API**: Optional OpenAI integration for smart responses

## 🔄 API Endpoints

- `GET /` - Main interface
- `POST /process` - Process user queries
- `DELETE /delete_task/<id>` - Delete a task
- `PUT /update_task/<id>` - Update a task

## 🎯 Intent Detection

The assistant recognizes three types of intents:

1. **Reminders**: Keywords like "remind", "remember", "don't forget"
2. **Scheduling**: Keywords like "schedule", "plan", "appointment", "meeting"  
3. **Questions**: Keywords like "what", "how", "when", or ending with "?"

## 📅 Time Parsing

Supports natural language time expressions:
- "tomorrow" → Next day at 9 AM
- "today" → Today at 6 PM  
- "next week" → Same day next week at 9 AM
- "at 3pm" → Today at 3 PM
- "at 15:30" → Today at 15:30

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🆘 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**Database permissions:**
```bash
# Ensure write permissions
chmod 755 .
```

**Missing dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 🔮 Future Enhancements

- [ ] Email notifications for reminders
- [ ] Calendar integration
- [ ] Voice input/output
- [ ] Multi-user support
- [ ] Mobile app
- [ ] Advanced NLP with spaCy/NLTK
- [ ] Task categories and priorities
- [ ] Recurring reminders

---

**Made with ❤️ and Python** 

Ready to upload to GitHub! 🚀
# Personal-AI
