# MediBot - AI Medical Chatbot 🏥

An AI-driven medical chatbot capable of offering preliminary health advice by recognizing symptoms and mapping them to relevant medical information. Built with Python, FastAPI/Flask, MongoDB, Hugging Face, and LangChain.

## Features ✨

- **Symptom Recognition**: Context-aware NLP pipelines to detect and extract symptoms from user queries
- **Condition Mapping**: Semantic similarity matching to identify potential medical conditions
- **Conversational AI**: LangChain-powered conversational memory for context-aware responses
- **Intent Detection**: Dialogflow integration (optional) for enhanced intent classification
- **RESTful API**: Both FastAPI and Flask implementations
- **Database Storage**: MongoDB for conversation logging and medical knowledge base
- **Web Interface**: Clean, responsive HTML/CSS/JS frontend

## Tech Stack 🛠️

- **Backend**: FastAPI, Flask
- **Database**: MongoDB
- **NLP/ML**: Hugging Face Transformers, Sentence Transformers, LangChain
- **Intent Detection**: Dialogflow (optional)
- **Frontend**: HTML, CSS, JavaScript

## Project Structure 📁

```
medibot/
├── backend/
│   ├── fastapi_server.py      # FastAPI server implementation
│   ├── flask_server.py         # Flask server implementation
│   ├── database.py             # MongoDB handler
│   ├── nlp_pipeline.py         # NLP processing and symptom extraction
│   ├── langchain_integration.py # LangChain conversational chain
│   └── dialogflow_integration.py # Dialogflow intent detection
├── frontend/
│   └── index.html              # Web interface
├── data/
│   └── medical_knowledge.json  # Medical knowledge base
├── config/
├── models/
├── requirements.txt            # Python dependencies
└── .env.example               # Environment variables template
```

## Installation & Setup 🚀

### Prerequisites

- Python 3.8 or higher
- MongoDB (local or cloud instance)
- Optional: Google Cloud account for Dialogflow

### Step 1: Clone and Install Dependencies

```bash
# Navigate to project directory
cd medibot

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configurations
# Minimum required:
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=medibot
```

### Step 3: Set Up MongoDB

**Option A: Local MongoDB**
```bash
# Install MongoDB Community Edition
# https://www.mongodb.com/docs/manual/installation/

# Start MongoDB service
sudo systemctl start mongod  # Linux
brew services start mongodb-community  # macOS
```

**Option B: MongoDB Atlas (Free Cloud)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a cluster
4. Get connection string and update `MONGODB_URI` in `.env`

### Step 4: Get Hugging Face Token (Optional, for advanced models)

```bash
# Get free token from https://huggingface.co/settings/tokens
# Add to .env:
HUGGINGFACE_API_TOKEN=your_token_here
```

### Step 5: Set Up Dialogflow (Optional)

1. Go to https://dialogflow.cloud.google.com/
2. Create a new agent
3. Download service account JSON
4. Update `.env`:
```
DIALOGFLOW_PROJECT_ID=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

## Running the Application 🏃

### Option 1: FastAPI Server (Recommended)

```bash
cd backend
python fastapi_server.py
```

Server will run at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Option 2: Flask Server

```bash
cd backend
python flask_server.py
```

Server will run at: `http://localhost:5000`

### Frontend

Open `frontend/index.html` in your browser, or serve it:

```bash
cd frontend
python -m http.server 3000
```

Then visit: `http://localhost:3000`

## API Endpoints 📡

### Health Check
```bash
GET /health
```

### Chat (Main Endpoint)
```bash
POST /api/chat
Content-Type: application/json

{
    "message": "I have a headache and fever",
    "user_id": "user123"
}
```

### Search Symptoms
```bash
POST /api/symptoms
Content-Type: application/json

{
    "symptoms": ["fever", "cough", "fatigue"]
}
```

### Get All Conditions
```bash
GET /api/conditions
```

### Get User History
```bash
GET /api/history/{user_id}?limit=10
```

### Clear Session
```bash
POST /api/clear-session
```

## Usage Examples 💬

### Example 1: Basic Symptom Query
```
User: "I have a headache and nausea"
Bot: Detects symptoms → Matches to Migraine → Provides advice
```

### Example 2: Follow-up Questions
```
User: "I also have sensitivity to light"
Bot: Uses conversation context → Updates analysis → Provides additional guidance
```

### Example 3: Emergency Detection
```
User: "Severe chest pain and difficulty breathing"
Bot: Detects severity → Recommends immediate medical attention
```

## Testing the API 🧪

### Using cURL

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have fever and cough", "user_id": "test_user"}'
```

### Using Python

```python
import requests

response = requests.post(
    'http://localhost:8000/api/chat',
    json={
        'message': 'I have a sore throat and runny nose',
        'user_id': 'test_user'
    }
)
print(response.json())
```

## Key Features Explained 🔍

### 1. Symptom Extraction
- Uses keyword matching with context awareness
- Handles negations ("I don't have fever")
- Extracts symptom variations

### 2. Semantic Matching
- Uses Sentence Transformers for embeddings
- Calculates cosine similarity between user input and conditions
- Returns top-k most similar conditions

### 3. Conversational Memory
- LangChain ConversationBufferMemory
- Maintains context across conversation
- Handles follow-up questions

### 4. Intent Classification
- Dialogflow integration (optional)
- Fallback rule-based classification
- Handles greetings, help, emergencies

### 5. Response Generation
- Context-aware responses
- Includes disclaimers
- Provides actionable advice

## Medical Knowledge Base 📚

The system includes conditions for:
- Common Cold
- Flu (Influenza)
- Migraine
- Allergies
- Gastroenteritis
- Anxiety
- Hypertension
- Asthma
- Diabetes (Type 2)
- Depression
- UTI
- COVID-19

You can extend the knowledge base by editing `data/medical_knowledge.json`

## Customization 🎨

### Adding New Conditions

Edit `data/medical_knowledge.json`:
```json
{
    "condition": "New Condition",
    "symptoms": ["symptom1", "symptom2"],
    "advice": "Medical advice here",
    "severity": "mild|moderate|serious"
}
```

### Adjusting NLP Model

Change in `.env`:
```
MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
```

Options:
- `all-MiniLM-L6-v2` (fast, lightweight)
- `all-mpnet-base-v2` (better accuracy)
- `multi-qa-mpnet-base-dot-v1` (optimized for Q&A)

## Troubleshooting 🔧

### MongoDB Connection Error
```
Solution: Check if MongoDB is running
sudo systemctl status mongod
```

### Model Download Issues
```
Solution: Set Hugging Face cache directory
export TRANSFORMERS_CACHE=/path/to/cache
```

### Port Already in Use
```
Solution: Change port in .env
FASTAPI_PORT=8001
```

## Performance Optimization ⚡

1. **Use GPU**: Install `torch` with CUDA support
2. **Cache Embeddings**: Embeddings are cached after first load
3. **Reduce Model Size**: Use smaller transformer models
4. **Enable Connection Pooling**: MongoDB connection pooling enabled by default

## Security Considerations 🔒

- **Disclaimer**: Always include medical disclaimers
- **Data Privacy**: User conversations are logged - ensure GDPR compliance
- **Input Validation**: Sanitize user inputs
- **Rate Limiting**: Implement rate limiting for production
- **Authentication**: Add user authentication for production

## Deployment 🚀

### Docker (Recommended)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "backend/fastapi_server.py"]
```

### Cloud Platforms

- **Heroku**: Use Procfile
- **AWS**: EC2 or Elastic Beanstalk
- **Google Cloud**: Cloud Run
- **Azure**: App Service

## Future Enhancements 🚀

- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Image-based symptom detection
- [ ] Integration with telemedicine platforms
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced analytics dashboard
- [ ] Patient history tracking
- [ ] Appointment scheduling

## Disclaimer ⚠️

**IMPORTANT**: This chatbot provides preliminary information only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions regarding a medical condition. In case of emergency, call your local emergency services immediately.

## License 📄

MIT License - Feel free to use and modify for your projects!

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## Support 💬

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review API docs at `/docs` endpoint

## Credits 👏

Built with:
- FastAPI / Flask
- Hugging Face Transformers
- LangChain
- MongoDB
- Sentence Transformers

---

**Made with ❤️ for better healthcare accessibility**
