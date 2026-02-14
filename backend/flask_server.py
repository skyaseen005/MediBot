from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import MediBotDB
from nlp_pipeline import MedicalNLPPipeline
from langchain_integration import MedicalChatChain
from dialogflow_integration import DialogflowIntegration

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
db = MediBotDB()
nlp_pipeline = MedicalNLPPipeline()
chat_chain = MedicalChatChain()
dialogflow = DialogflowIntegration()

# Initialize on startup
def initialize():
    """Initialize components"""
    knowledge_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 'data', 'medical_knowledge.json'
    )
    db.initialize_knowledge_base(knowledge_path)
    conditions = db.get_all_conditions()
    nlp_pipeline.load_medical_knowledge(conditions)
    print("MediBot Flask API initialized!")

@app.route('/')
def root():
    """Root endpoint"""
    return jsonify({
        "message": "MediBot Flask API is running",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "symptoms": "/api/symptoms",
            "conditions": "/api/conditions",
            "health": "/health"
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "database": "connected" if db.db is not None else "offline",
        "nlp_model": "loaded",
        "dialogflow": "enabled" if dialogflow.enabled else "disabled"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        # Analyze user message
        analysis = nlp_pipeline.analyze_query(message)
        
        # Use Dialogflow
        dialogflow_result = dialogflow.detect_intent(message)
        if dialogflow_result:
            analysis['intent'] = dialogflow_result['intent']
        
        # Generate response
        response_text = nlp_pipeline.generate_response(analysis)
        
        # Use LangChain for context
        if analysis['intent'] == 'symptom_query':
            response_text = chat_chain.process_with_context(
                message,
                analysis['detected_symptoms'],
                analysis['matched_conditions']
            )
        
        # Log conversation
        db.log_conversation(
            user_id=user_id,
            user_message=message,
            bot_response=response_text,
            symptoms=analysis['detected_symptoms'],
            matched_conditions=[c['condition'] for c in analysis['matched_conditions']]
        )
        
        return jsonify({
            "response": response_text,
            "detected_symptoms": analysis['detected_symptoms'],
            "matched_conditions": analysis['matched_conditions'],
            "confidence": analysis['confidence'],
            "intent": analysis['intent']
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/symptoms', methods=['POST'])
def search_symptoms():
    """Search conditions by symptoms"""
    try:
        data = request.get_json()
        symptoms = data.get('symptoms', [])
        
        if not symptoms:
            return jsonify({"error": "Symptoms are required"}), 400
        
        conditions = db.search_by_symptoms(symptoms)
        return jsonify({
            "symptoms": symptoms,
            "matched_conditions": conditions,
            "count": len(conditions)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conditions', methods=['GET'])
def get_conditions():
    """Get all medical conditions"""
    try:
        conditions = db.get_all_conditions()
        return jsonify({
            "conditions": conditions,
            "count": len(conditions)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/<user_id>', methods=['GET'])
def get_history(user_id):
    """Get conversation history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = db.get_user_history(user_id, limit)
        return jsonify({
            "user_id": user_id,
            "history": history,
            "count": len(history)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/clear-session', methods=['POST'])
def clear_session():
    """Clear conversation session"""
    chat_chain.clear_history()
    return jsonify({"message": "Session cleared successfully"})

if __name__ == '__main__':
    initialize()
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )
