import os
from typing import Dict, Optional

class DialogflowIntegration:
    """
    Dialogflow integration for intent detection and entity extraction.
    This is optional and can work without actual Dialogflow API keys for demo purposes.
    """
    
    def __init__(self):
        self.project_id = os.getenv('DIALOGFLOW_PROJECT_ID', 'medibot-demo')
        self.session_id = os.getenv('DIALOGFLOW_SESSION_ID', 'medibot_session')
        self.enabled = False
        
        # Try to initialize Dialogflow
        try:
            import google.cloud.dialogflow as dialogflow
            self.session_client = dialogflow.SessionsClient()
            self.session_path = self.session_client.session_path(
                self.project_id, self.session_id
            )
            self.enabled = True
            print("Dialogflow integration enabled")
        except Exception as e:
            print(f"Dialogflow not available (working in offline mode): {e}")
            self.enabled = False
    
    def detect_intent(self, text: str, language_code: str = 'en') -> Optional[Dict]:
        """Detect intent using Dialogflow"""
        if not self.enabled:
            return self._fallback_intent_detection(text)
        
        try:
            import google.cloud.dialogflow as dialogflow
            
            text_input = dialogflow.TextInput(text=text, language_code=language_code)
            query_input = dialogflow.QueryInput(text=text_input)
            
            response = self.session_client.detect_intent(
                request={"session": self.session_path, "query_input": query_input}
            )
            
            return {
                'intent': response.query_result.intent.display_name,
                'confidence': response.query_result.intent_detection_confidence,
                'parameters': dict(response.query_result.parameters),
                'fulfillment_text': response.query_result.fulfillment_text
            }
        except Exception as e:
            print(f"Dialogflow error: {e}")
            return self._fallback_intent_detection(text)
    
    def _fallback_intent_detection(self, text: str) -> Dict:
        """Fallback intent detection without Dialogflow API"""
        text_lower = text.lower()
        
        # Simple rule-based intent detection
        if any(word in text_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            intent = 'greeting'
            confidence = 0.95
        elif any(word in text_lower for word in ['help', 'what can you do', 'how']):
            intent = 'help'
            confidence = 0.90
        elif any(word in text_lower for word in ['thank', 'thanks']):
            intent = 'gratitude'
            confidence = 0.95
        elif any(word in text_lower for word in ['bye', 'goodbye', 'see you']):
            intent = 'farewell'
            confidence = 0.95
        elif any(word in text_lower for word in ['emergency', 'urgent', 'severe', 'critical']):
            intent = 'emergency'
            confidence = 0.90
        else:
            intent = 'symptom_inquiry'
            confidence = 0.75
        
        return {
            'intent': intent,
            'confidence': confidence,
            'parameters': {},
            'fulfillment_text': '',
            'mode': 'fallback'
        }
    
    def extract_entities(self, text: str) -> Dict:
        """Extract entities from text"""
        entities = {
            'symptoms': [],
            'duration': None,
            'severity': None,
            'location': None
        }
        
        text_lower = text.lower()
        
        # Extract duration
        duration_patterns = ['day', 'week', 'month', 'hour']
        for pattern in duration_patterns:
            if pattern in text_lower:
                entities['duration'] = pattern
                break
        
        # Extract severity
        severity_words = ['mild', 'moderate', 'severe', 'extreme', 'slight']
        for word in severity_words:
            if word in text_lower:
                entities['severity'] = word
                break
        
        # Extract body location
        body_parts = ['head', 'chest', 'stomach', 'back', 'leg', 'arm', 'throat', 'eye']
        for part in body_parts:
            if part in text_lower:
                entities['location'] = part
                break
        
        return entities
