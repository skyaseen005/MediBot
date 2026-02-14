# MediBot - Complete Project Information

## Project Overview

MediBot is a fully functional AI-driven medical chatbot that provides preliminary health advice by recognizing symptoms and mapping them to relevant medical information. The system uses advanced NLP techniques and machine learning to understand user queries and provide contextually appropriate responses.

## Key Features Implemented

### 1. **Symptom Recognition & Extraction**
- Context-aware NLP pipeline using Sentence Transformers
- Keyword-based symptom detection with negation handling
- Supports variations in symptom descriptions
- Extracts multiple symptoms from single query

### 2. **Semantic Condition Matching**
- Uses sentence embeddings for semantic similarity
- Cosine similarity-based matching
- Returns top-k most relevant conditions
- Confidence scoring for each match

### 3. **Conversational AI**
- LangChain integration for conversation memory
- Context-aware multi-turn conversations
- Follow-up question handling
- Session management

### 4. **Intent Detection**
- Dialogflow integration (optional)
- Fallback rule-based classification
- Multiple intent types: greeting, help, symptom_query, emergency
- Entity extraction for duration, severity, location

### 5. **Dual API Implementation**
- **FastAPI**: Modern, high-performance API with automatic documentation
- **Flask**: Traditional, lightweight alternative
- Both implementations share the same core logic
- RESTful design with proper error handling

### 6. **Database Integration**
- MongoDB for persistent storage
- Conversation logging for analytics
- User history tracking
- Medical knowledge base management
- Works with or without database (graceful degradation)

### 7. **Web Interface**
- Clean, modern UI with gradient design
- Real-time chat interface
- Typing indicators
- Responsive layout
- Displays detected symptoms and conditions
- Health disclaimers

## Tech Stack Details

### Backend
- **FastAPI 0.104.1**: Modern, fast web framework
- **Flask 3.0.0**: Traditional, lightweight framework
- **Uvicorn**: ASGI server for FastAPI
- **Pydantic**: Data validation and settings

### Database
- **PyMongo 4.6.0**: MongoDB driver
- **Motor 3.3.2**: Async MongoDB driver

### NLP & ML
- **Transformers 4.36.0**: Hugging Face transformers library
- **Sentence-Transformers 2.2.2**: Semantic text embeddings
- **PyTorch 2.1.0**: Deep learning framework
- **LangChain 0.1.0**: LLM application framework
- **scikit-learn**: Additional ML utilities

### Optional Integrations
- **Google Cloud Dialogflow**: Intent detection
- **Hugging Face Hub**: Model downloads

## Project Structure Explained

```
medibot/
├── backend/                          # All backend code
│   ├── fastapi_server.py            # FastAPI implementation
│   ├── flask_server.py              # Flask implementation
│   ├── database.py                  # MongoDB handler
│   ├── nlp_pipeline.py              # Core NLP processing
│   ├── langchain_integration.py     # LangChain integration
│   └── dialogflow_integration.py    # Dialogflow integration
│
├── frontend/                         # Web interface
│   └── index.html                   # Single-page application
│
├── data/                            # Data files
│   └── medical_knowledge.json       # Medical conditions database
│
├── config/                          # Configuration files
├── models/                          # Model cache directory
│
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
│
├── setup.py                         # Automated setup script
├── start.sh                         # Linux/Mac start script
├── start.bat                        # Windows start script
├── test_system.py                   # System tests
│
├── Dockerfile                       # Docker container config
├── docker-compose.yml               # Docker Compose config
│
├── README.md                        # Main documentation
├── API_DOCS.md                      # API documentation
└── PROJECT_INFO.md                  # This file
```

## How It Works

### 1. User Input Processing
```
User Input → Intent Detection → Symptom Extraction → Semantic Matching → Response Generation
```

### 2. NLP Pipeline Flow
1. **Input**: User message (e.g., "I have a headache and fever")
2. **Symptom Extraction**: Detects ["headache", "fever"]
3. **Negation Handling**: Removes negated symptoms
4. **Semantic Encoding**: Converts input to embeddings
5. **Similarity Matching**: Compares with condition embeddings
6. **Ranking**: Returns top matches with confidence scores

### 3. Conversation Flow
```
User Message
    ↓
[Dialogflow] Optional Intent Detection
    ↓
[NLP Pipeline] Symptom Analysis
    ↓
[LangChain] Context Enhancement
    ↓
[Response Generator] Natural Language Response
    ↓
[Database] Log Conversation
    ↓
Return to User
```

## API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/api/chat` | POST | Main chat interface |
| `/api/symptoms` | POST | Search by symptoms |
| `/api/conditions` | GET | Get all conditions |
| `/api/history/{user_id}` | GET | User history |
| `/api/clear-session` | POST | Clear session |

## Configuration Options

### Environment Variables

```bash
# Database
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB_NAME=medibot

# Optional: Hugging Face
HUGGINGFACE_API_TOKEN=your_token

# Optional: Dialogflow
DIALOGFLOW_PROJECT_ID=your_project_id
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json

# Server Config
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
FLASK_PORT=5000

# Model Config
MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
```

### Model Options

You can change the NLP model in `.env`:
- `all-MiniLM-L6-v2`: Fast, lightweight (default)
- `all-mpnet-base-v2`: Better accuracy, slower
- `multi-qa-mpnet-base-dot-v1`: Optimized for Q&A

## Installation Methods

### Method 1: Automated Setup
```bash
python setup.py
```

### Method 2: Manual Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run server
python backend/fastapi_server.py
```

### Method 3: Docker
```bash
docker-compose up
```

## Running the Application

### FastAPI (Recommended)
```bash
python backend/fastapi_server.py
# Access: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Flask
```bash
python backend/flask_server.py
# Access: http://localhost:5000
```

### Frontend
```bash
# Open directly
open frontend/index.html

# Or serve with Python
cd frontend
python -m http.server 3000
# Access: http://localhost:3000
```

## Testing

### Run All Tests
```bash
python test_system.py
```

### Test Individual Components
```python
# Test NLP Pipeline
from backend.nlp_pipeline import MedicalNLPPipeline
nlp = MedicalNLPPipeline()
analysis = nlp.analyze_query("I have a fever")

# Test Database
from backend.database import MediBotDB
db = MediBotDB()
conditions = db.get_all_conditions()
```

### Test API with cURL
```bash
# Health check
curl http://localhost:8000/health

# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have symptoms", "user_id": "test"}'
```

## Medical Knowledge Base

Currently includes 12 conditions:
1. Common Cold
2. Flu (Influenza)
3. Migraine
4. Allergies
5. Gastroenteritis
6. Anxiety
7. Hypertension
8. Asthma
9. Diabetes (Type 2)
10. Depression
11. Urinary Tract Infection
12. COVID-19

### Adding New Conditions
Edit `data/medical_knowledge.json`:
```json
{
  "condition": "New Condition",
  "symptoms": ["symptom1", "symptom2", "symptom3"],
  "advice": "Medical advice and recommendations",
  "severity": "mild|moderate|serious"
}
```

## Performance Considerations

### Speed Optimizations
- Model embeddings cached after first load
- MongoDB connection pooling
- Async operations where possible
- Lightweight model by default

### Resource Usage
- RAM: ~1-2 GB (with model loaded)
- Disk: ~500 MB (including models)
- CPU: Low during inference
- GPU: Optional, can improve performance

## Security Best Practices

### Implemented
✓ Input sanitization
✓ Error handling
✓ CORS configuration
✓ Health disclaimers

### Recommended for Production
- [ ] Rate limiting
- [ ] Authentication/Authorization
- [ ] HTTPS/TLS
- [ ] API key management
- [ ] Request logging
- [ ] Input validation middleware
- [ ] Session management
- [ ] Data encryption

## Deployment Options

### 1. Local Server
- Use for development
- Easy debugging
- No deployment costs

### 2. Docker
- Consistent environment
- Easy scaling
- Portable

### 3. Cloud Platforms

#### Heroku
```bash
# Create Procfile
web: python backend/fastapi_server.py
```

#### AWS EC2
- Use provided Dockerfile
- Set up security groups
- Configure reverse proxy (nginx)

#### Google Cloud Run
- Containerize application
- Deploy with Cloud Build
- Auto-scaling enabled

#### Azure App Service
- Use Docker container
- Configure app settings
- Enable CI/CD

## Monitoring & Logging

### Built-in Logging
- Conversation logging to MongoDB
- Server startup logs
- Error tracking

### Production Monitoring
- Add APM (Application Performance Monitoring)
- Set up log aggregation (ELK stack)
- Configure alerts
- Track API metrics

## Common Issues & Solutions

### Issue: Model Download Fails
**Solution**: Set cache directory
```bash
export TRANSFORMERS_CACHE=/path/to/cache
```

### Issue: MongoDB Connection Error
**Solution**: Check MongoDB status
```bash
sudo systemctl status mongod
```

### Issue: Port Already in Use
**Solution**: Change port in `.env`
```bash
FASTAPI_PORT=8001
```

### Issue: Import Errors
**Solution**: Ensure virtual environment activated
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Future Enhancements Roadmap

### Phase 1 (Immediate)
- [ ] Enhanced medical knowledge base
- [ ] Multi-language support
- [ ] Better error messages

### Phase 2 (Short-term)
- [ ] Voice input/output
- [ ] Image-based symptom detection
- [ ] Advanced analytics dashboard

### Phase 3 (Long-term)
- [ ] Mobile applications
- [ ] Integration with EHR systems
- [ ] Telemedicine platform integration
- [ ] AI-powered diagnosis improvement

## Contributing Guidelines

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## License

MIT License - Free to use and modify

## Support & Resources

- **Documentation**: README.md, API_DOCS.md
- **API Docs**: http://localhost:8000/docs
- **GitHub Issues**: For bug reports
- **Community**: Share improvements

## Credits & Acknowledgments

Built using:
- Hugging Face Transformers
- Sentence Transformers (UKPLab)
- FastAPI (Sebastián Ramírez)
- LangChain (Harrison Chase)
- MongoDB

## Disclaimer

**CRITICAL**: This is a preliminary health information tool only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical concerns. In emergencies, call local emergency services immediately.

---

**Project Status**: ✅ Complete and Fully Functional
**Last Updated**: February 2024
**Version**: 1.0.0
