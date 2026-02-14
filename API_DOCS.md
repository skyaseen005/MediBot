# MediBot API Documentation

## Base URL
- FastAPI: `http://localhost:8000`
- Flask: `http://localhost:5000`

## Endpoints

### 1. Health Check
**Endpoint:** `GET /health`

**Description:** Check if the API is running and get system status

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "nlp_model": "loaded",
  "dialogflow": "enabled"
}
```

---

### 2. Chat
**Endpoint:** `POST /api/chat`

**Description:** Main chatbot endpoint for symptom analysis and medical advice

**Request Body:**
```json
{
  "message": "I have a headache and fever",
  "user_id": "user123",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "response": "Based on your description, I've detected...",
  "detected_symptoms": ["headache", "fever"],
  "matched_conditions": [
    {
      "condition": "Flu (Influenza)",
      "symptoms": ["fever", "headache", "body aches"],
      "advice": "Rest, stay hydrated...",
      "severity": "moderate",
      "similarity_score": 0.85
    }
  ],
  "confidence": 0.75,
  "intent": "symptom_query"
}
```

---

### 3. Search Symptoms
**Endpoint:** `POST /api/symptoms`

**Description:** Search for conditions based on specific symptoms

**Request Body:**
```json
{
  "symptoms": ["fever", "cough", "fatigue"]
}
```

**Response:**
```json
{
  "symptoms": ["fever", "cough", "fatigue"],
  "matched_conditions": [
    {
      "condition": "Flu (Influenza)",
      "symptoms": ["high fever", "body aches", "fatigue"],
      "advice": "Rest, drink plenty of fluids...",
      "severity": "moderate"
    }
  ],
  "count": 3
}
```

---

### 4. Get All Conditions
**Endpoint:** `GET /api/conditions`

**Description:** Retrieve all medical conditions in the knowledge base

**Response:**
```json
{
  "conditions": [
    {
      "condition": "Common Cold",
      "symptoms": ["runny nose", "sneezing"],
      "advice": "Rest, stay hydrated...",
      "severity": "mild"
    }
  ],
  "count": 12
}
```

---

### 5. Get User History
**Endpoint:** `GET /api/history/{user_id}?limit=10`

**Description:** Get conversation history for a specific user

**Parameters:**
- `user_id` (path): User identifier
- `limit` (query, optional): Number of records to retrieve (default: 10)

**Response:**
```json
{
  "user_id": "user123",
  "history": [
    {
      "timestamp": "2024-02-14T10:30:00Z",
      "user_message": "I have a headache",
      "bot_response": "I understand you're experiencing...",
      "symptoms_detected": ["headache"],
      "conditions_matched": ["Migraine"]
    }
  ],
  "count": 5
}
```

---

### 6. Clear Session
**Endpoint:** `POST /api/clear-session`

**Description:** Clear conversation context and memory

**Response:**
```json
{
  "message": "Session cleared successfully"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Message is required"
}
```

### 500 Internal Server Error
```json
{
  "error": "Error processing request: [error details]"
}
```

---

## Example Usage

### cURL Examples

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Chat Request
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have a sore throat and fever",
    "user_id": "test_user"
  }'
```

#### Search Symptoms
```bash
curl -X POST http://localhost:8000/api/symptoms \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["fever", "cough"]
  }'
```

---

### Python Examples

#### Using requests library
```python
import requests

# Chat endpoint
response = requests.post(
    'http://localhost:8000/api/chat',
    json={
        'message': 'I have chest pain and shortness of breath',
        'user_id': 'user123'
    }
)

data = response.json()
print(f"Symptoms detected: {data['detected_symptoms']}")
print(f"Response: {data['response']}")
```

#### Using httpx (async)
```python
import httpx
import asyncio

async def chat():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://localhost:8000/api/chat',
            json={
                'message': 'I feel dizzy and nauseous',
                'user_id': 'user456'
            }
        )
        return response.json()

result = asyncio.run(chat())
print(result)
```

---

### JavaScript Examples

#### Using fetch
```javascript
// Chat request
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'I have stomach pain and diarrhea',
    user_id: 'web_user_123'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Symptoms:', data.detected_symptoms);
  console.log('Response:', data.response);
})
.catch(error => console.error('Error:', error));
```

#### Using axios
```javascript
import axios from 'axios';

const chat = async (message) => {
  try {
    const response = await axios.post('http://localhost:8000/api/chat', {
      message: message,
      user_id: 'user789'
    });
    
    return response.data;
  } catch (error) {
    console.error('Error:', error);
  }
};

chat('I have a persistent cough').then(data => {
  console.log(data);
});
```

---

## Response Fields

### Chat Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `response` | string | Generated chatbot response |
| `detected_symptoms` | array | List of symptoms detected in user message |
| `matched_conditions` | array | Possible medical conditions matching symptoms |
| `confidence` | float | Confidence score (0-1) |
| `intent` | string | Detected user intent (greeting, help, symptom_query, etc.) |

### Condition Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `condition` | string | Name of the medical condition |
| `symptoms` | array | Common symptoms for this condition |
| `advice` | string | Medical advice and recommendations |
| `severity` | string | Severity level (mild, moderate, serious) |
| `similarity_score` | float | Similarity score with user input (0-1) |

---

## Intent Types

- `greeting`: User greeting (hello, hi)
- `help`: User asking for help
- `symptom_query`: User describing symptoms
- `gratitude`: User thanking the bot
- `farewell`: User saying goodbye
- `emergency`: Emergency-related query

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider adding:
- Rate limiting middleware
- Authentication/Authorization
- Request throttling

---

## CORS Configuration

CORS is enabled for all origins in development. For production:
- Restrict allowed origins
- Configure credentials policy
- Set appropriate headers

---

## WebSocket Support (Future)

Future versions may include WebSocket support for real-time chat:
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Bot response:', data);
};

ws.send(JSON.stringify({
  message: 'I have symptoms',
  user_id: 'user123'
}));
```

---

## Interactive API Documentation

### FastAPI
Visit `http://localhost:8000/docs` for interactive Swagger UI documentation

### ReDoc
Visit `http://localhost:8000/redoc` for alternative documentation view

---

## Error Handling

Always check the response status code:
- `200`: Success
- `400`: Bad request (missing or invalid parameters)
- `500`: Internal server error

Example error handling:
```python
response = requests.post(url, json=data)
if response.status_code == 200:
    result = response.json()
elif response.status_code == 400:
    print("Bad request:", response.json()['error'])
else:
    print("Server error:", response.json()['error'])
```

---

## Best Practices

1. **Always include user_id**: Helps with conversation tracking
2. **Handle errors gracefully**: API may fail, implement retry logic
3. **Validate responses**: Check for expected fields before using
4. **Use session management**: Clear sessions when appropriate
5. **Include disclaimers**: Always remind users to consult healthcare professionals

---

## Support

For issues or questions:
- Check server logs
- Verify MongoDB connection
- Test with health endpoint first
- Review API documentation at `/docs`
