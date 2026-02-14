# MediBot Quick Start Guide 🚀

Get MediBot running in 5 minutes!

## Prerequisites ✅

- Python 3.8 or higher
- pip (Python package manager)
- MongoDB (optional - can work without it)

## Option 1: Fastest Start (Automated) ⚡

### Step 1: Run Setup Script
```bash
cd medibot
python setup.py
```

This will:
- Check Python version
- Create virtual environment
- Install all dependencies
- Download NLP models
- Set up configuration files

### Step 2: Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Step 3: Start the Server

**Using Quick Start Scripts:**

Linux/Mac:
```bash
./start.sh
```

Windows:
```bash
start.bat
```

**Or manually:**
```bash
python backend/fastapi_server.py
```

### Step 4: Open Frontend
Open `frontend/index.html` in your browser and start chatting!

---

## Option 2: Manual Setup 🛠️

### Step 1: Install Dependencies
```bash
cd medibot
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env if needed (optional for basic usage)
```

### Step 3: Run Server
```bash
# FastAPI (Recommended)
python backend/fastapi_server.py

# OR Flask
python backend/flask_server.py
```

### Step 4: Access Application
- **Frontend**: Open `frontend/index.html`
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Option 3: Docker (Production-Ready) 🐳

### Prerequisites
- Docker
- Docker Compose

### Step 1: Build and Run
```bash
cd medibot
docker-compose up -d
```

### Step 2: Access
- **API**: http://localhost:8000
- **MongoDB**: localhost:27017

### Step 3: Stop
```bash
docker-compose down
```

---

## Testing Your Installation ✅

### 1. Test API
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "nlp_model": "loaded"
}
```

### 2. Test Chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a headache", "user_id": "test"}'
```

### 3. Run System Tests
```bash
python test_system.py
```

---

## First Conversation Example 💬

1. Open `frontend/index.html` in browser
2. Type: "I have a fever and cough"
3. Press Send
4. MediBot will:
   - Detect symptoms: fever, cough
   - Match possible conditions
   - Provide preliminary advice
   - Display health disclaimer

---

## Common Issues & Quick Fixes 🔧

### Issue: "Module not found"
**Fix:**
```bash
pip install -r requirements.txt
```

### Issue: "Port already in use"
**Fix:** Change port in `.env`
```bash
FASTAPI_PORT=8001
```

### Issue: "MongoDB connection error"
**Fix:** Either install MongoDB or continue without it
```bash
# The app works without MongoDB with limited features
# Or install MongoDB: https://www.mongodb.com/docs/manual/installation/
```

### Issue: Model download slow
**Fix:** This happens only once. Go get coffee ☕

---

## Next Steps 📚

### 1. Explore API Documentation
Visit: http://localhost:8000/docs

### 2. Customize Medical Knowledge
Edit: `data/medical_knowledge.json`

### 3. Configure Settings
Edit: `.env` file

### 4. Read Full Documentation
See: `README.md` and `API_DOCS.md`

---

## Example API Calls

### Python
```python
import requests

response = requests.post(
    'http://localhost:8000/api/chat',
    json={'message': 'I have symptoms', 'user_id': 'test'}
)
print(response.json())
```

### JavaScript
```javascript
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: 'I have symptoms',
    user_id: 'test'
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I feel sick", "user_id": "test"}'
```

---

## Performance Tips ⚡

### 1. First Run
- First run downloads models (~200MB)
- Takes 2-3 minutes
- Subsequent runs are instant

### 2. With GPU (Optional)
```bash
# Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3. Reduce Memory Usage
Change model in `.env`:
```bash
MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
```

---

## Stopping the Server

### Development Mode
Press `Ctrl+C` in terminal

### Docker Mode
```bash
docker-compose down
```

---

## Getting Help 💡

1. **Check Logs**: Look at server console output
2. **Test Health**: `curl http://localhost:8000/health`
3. **Read Docs**: Check `README.md` for details
4. **Run Tests**: `python test_system.py`

---

## What's Working? ✅

- ✅ Symptom extraction from natural language
- ✅ Semantic condition matching
- ✅ Conversational context (LangChain)
- ✅ Intent detection (Dialogflow optional)
- ✅ RESTful API (FastAPI + Flask)
- ✅ MongoDB integration (optional)
- ✅ Web interface
- ✅ Conversation logging
- ✅ User history tracking

---

## Quick Commands Cheat Sheet

```bash
# Setup
python setup.py

# Activate venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Start server
python backend/fastapi_server.py

# Test
python test_system.py
curl http://localhost:8000/health

# Docker
docker-compose up -d
docker-compose down

# Install deps
pip install -r requirements.txt
```

---

## Minimum System Requirements

- **OS**: Windows, Linux, or macOS
- **Python**: 3.8+
- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 1GB free space
- **Network**: For downloading models (first run only)

---

## Pro Tips 💡

1. **Use FastAPI**: Better performance and auto-docs
2. **Enable MongoDB**: For conversation history
3. **Use virtual environment**: Keeps dependencies isolated
4. **Check `/docs`**: Interactive API documentation
5. **Read disclaimers**: This is NOT medical advice

---

## Success Checklist ✅

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] Server starts without errors
- [ ] Health check returns "healthy"
- [ ] Frontend loads in browser
- [ ] Can send messages and get responses
- [ ] Symptoms detected correctly
- [ ] Conditions matched appropriately

---

## Ready to Go! 🎉

You're all set! Start chatting with MediBot and remember:

**⚠️ IMPORTANT**: MediBot provides preliminary information only. Always consult healthcare professionals for medical advice!

---

**Questions?** Check `README.md` or `API_DOCS.md` for detailed documentation.
