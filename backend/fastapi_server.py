from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import MediBotDB
from nlp_pipeline import MedicalNLPPipeline
from langchain_integration import MedicalChatChain
from dialogflow_integration import DialogflowIntegration

# Initialize FastAPI app
app = FastAPI(
    title="MediBot API",
    description="AI-driven medical chatbot API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db = MediBotDB()
nlp_pipeline = MedicalNLPPipeline()
chat_chain = MedicalChatChain()
dialogflow = DialogflowIntegration()

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    user_id: str = "anonymous"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    detected_symptoms: List[str]
    matched_conditions: List[Dict]
    confidence: float
    intent: str

class SymptomSearchRequest(BaseModel):
    symptoms: List[str]

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    try:
        # Load medical knowledge from file
        knowledge_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 'data', 'medical_knowledge.json'
        )
        
        if os.path.exists(knowledge_path):
            with open(knowledge_path, 'r', encoding='utf-8') as f:
                medical_data = json.load(f)
            
            # Try to load into database (if available)
            db.initialize_knowledge_base(knowledge_path)
            
            # Always load into NLP pipeline from file (this is critical!)
            nlp_pipeline.load_medical_knowledge(medical_data)
            
            print(f"MediBot API initialized successfully with {len(medical_data)} conditions!")
        else:
            print(f"Warning: Knowledge base file not found at {knowledge_path}")
            print("Please ensure data/medical_knowledge.json exists")
            
    except Exception as e:
        print(f"Startup error: {e}")
        print("Continuing with limited functionality...")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MediBot API is running",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "symptoms": "/api/symptoms",
            "conditions": "/api/conditions",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if db.db is not None else "offline",
        "nlp_model": "loaded",
        "conditions_loaded": len(nlp_pipeline.conditions_data),
        "dialogflow": "enabled" if dialogflow.enabled else "disabled"
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint"""
    try:
        # Analyze user message with NLP pipeline
        analysis = nlp_pipeline.analyze_query(request.message)
        
        # Use Dialogflow for intent detection (if available)
        dialogflow_result = dialogflow.detect_intent(request.message)
        if dialogflow_result:
            analysis['intent'] = dialogflow_result['intent']
        
        # Generate response
        response_text = nlp_pipeline.generate_response(analysis)
        
        # Use LangChain for contextual enhancement
        if analysis['intent'] == 'symptom_query':
            response_text = chat_chain.process_with_context(
                request.message,
                analysis['detected_symptoms'],
                analysis['matched_conditions']
            )
        
        # Log conversation to database
        db.log_conversation(
            user_id=request.user_id,
            user_message=request.message,
            bot_response=response_text,
            symptoms=analysis['detected_symptoms'],
            matched_conditions=[c['condition'] for c in analysis['matched_conditions']]
        )
        
        return ChatResponse(
            response=response_text,
            detected_symptoms=analysis['detected_symptoms'],
            matched_conditions=analysis['matched_conditions'],
            confidence=analysis['confidence'],
            intent=analysis['intent']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/api/symptoms")
async def search_symptoms(request: SymptomSearchRequest):
    """Search conditions by symptoms"""
    try:
        conditions = db.search_by_symptoms(request.symptoms)
        return {
            "symptoms": request.symptoms,
            "matched_conditions": conditions,
            "count": len(conditions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching symptoms: {str(e)}")

@app.get("/api/conditions")
async def get_conditions():
    """Get all medical conditions"""
    try:
        # Try database first, fallback to NLP pipeline data
        conditions = db.get_all_conditions()
        if not conditions:
            conditions = nlp_pipeline.conditions_data
        
        return {
            "conditions": conditions,
            "count": len(conditions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conditions: {str(e)}")

@app.get("/api/history/{user_id}")
async def get_history(user_id: str, limit: int = 10):
    """Get conversation history for a user"""
    try:
        history = db.get_user_history(user_id, limit)
        return {
            "user_id": user_id,
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@app.post("/api/clear-session")
async def clear_session():
    """Clear conversation session"""
    chat_chain.clear_history()
    return {"message": "Session cleared successfully"}

if __name__ == "__main__":
    port = int(os.getenv('FASTAPI_PORT', 8000))
    uvicorn.run(
        "fastapi_server:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )