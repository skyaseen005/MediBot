import re
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer, util
import numpy as np
import json

class MedicalNLPPipeline:
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        """Initialize NLP pipeline with sentence transformer"""
        print(f"Loading NLP model: {model_name}")
        self.model = SentenceTransformer(model_name)
        
        # Common symptom keywords
        self.symptom_keywords = [
            'pain', 'ache', 'fever', 'cough', 'headache', 'nausea', 'vomiting',
            'diarrhea', 'fatigue', 'tired', 'dizzy', 'weak', 'sore', 'swollen',
            'rash', 'itch', 'sneeze', 'congestion', 'runny nose', 'sore throat',
            'shortness of breath', 'chest pain', 'palpitations', 'anxiety',
            'depression', 'sad', 'worry', 'stress', 'blurred vision', 'thirst',
            'frequent urination', 'weight loss', 'weight gain', 'insomnia',
            'sleep problems', 'numbness', 'tingling', 'bleeding', 'bruising',
            'confusion', 'memory problems', 'difficulty concentrating'
        ]
        
        # Negation words
        self.negations = ['no', 'not', 'never', 'without', 'none', "don't", "doesn't", "didn't"]
        
        # Load medical knowledge base for embeddings
        self.conditions_data = []
        self.condition_embeddings = None
        
    def load_medical_knowledge(self, knowledge_base: List[Dict]):
        """Load and embed medical knowledge base"""
        self.conditions_data = knowledge_base
        
        # Handle empty knowledge base
        if not knowledge_base:
            print("Warning: Empty knowledge base provided")
            self.condition_embeddings = None
            return
        
        # Create text representations of conditions
        condition_texts = []
        for condition in knowledge_base:
            # Combine condition name and symptoms
            text = f"{condition['condition']}. Symptoms: {', '.join(condition['symptoms'])}"
            condition_texts.append(text)
        
        # Generate embeddings only if we have texts
        if condition_texts:
            print("Generating embeddings for medical conditions...")
            self.condition_embeddings = self.model.encode(condition_texts, convert_to_tensor=True)
            print(f"Loaded {len(self.conditions_data)} conditions")
        else:
            print("No conditions to embed")
            self.condition_embeddings = None
    
    def extract_symptoms(self, user_input: str) -> List[str]:
        """Extract symptoms from user input"""
        user_input_lower = user_input.lower()
        detected_symptoms = []
        
        # Check for each symptom keyword
        for symptom in self.symptom_keywords:
            if symptom in user_input_lower:
                # Check for negation
                is_negated = False
                symptom_position = user_input_lower.find(symptom)
                
                # Look for negation words before the symptom
                words_before = user_input_lower[:symptom_position].split()
                if len(words_before) > 0:
                    last_few_words = words_before[-3:]  # Check last 3 words
                    if any(neg in last_few_words for neg in self.negations):
                        is_negated = True
                
                if not is_negated:
                    detected_symptoms.append(symptom)
        
        # Remove duplicates
        detected_symptoms = list(set(detected_symptoms))
        return detected_symptoms
    
    def match_conditions(self, user_input: str, symptoms: List[str], top_k: int = 3) -> List[Dict]:
        """Match user input to medical conditions using semantic similarity"""
        if not self.conditions_data or self.condition_embeddings is None:
            return []
        
        # Create query from user input and symptoms
        if symptoms:
            query = f"{user_input}. Symptoms: {', '.join(symptoms)}"
        else:
            query = user_input
        
        # Encode query
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        
        # Calculate cosine similarities
        similarities = util.cos_sim(query_embedding, self.condition_embeddings)[0]
        
        # Get top-k matches
        top_indices = similarities.argsort(descending=True)[:top_k]
        
        results = []
        for idx in top_indices:
            idx = idx.item()
            similarity_score = similarities[idx].item()
            
            # Only include if similarity is above threshold
            if similarity_score > 0.2:
                condition = self.conditions_data[idx].copy()
                condition['similarity_score'] = float(similarity_score)
                results.append(condition)
        
        return results
    
    def analyze_query(self, user_input: str) -> Dict:
        """Complete analysis of user query"""
        # Extract symptoms
        symptoms = self.extract_symptoms(user_input)
        
        # Match conditions
        matched_conditions = self.match_conditions(user_input, symptoms)
        
        # Determine query intent
        intent = self._classify_intent(user_input)
        
        return {
            'user_input': user_input,
            'detected_symptoms': symptoms,
            'matched_conditions': matched_conditions,
            'intent': intent,
            'confidence': self._calculate_confidence(symptoms, matched_conditions)
        }
    
    def _classify_intent(self, user_input: str) -> str:
        """Classify user intent"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return 'greeting'
        elif any(word in user_input_lower for word in ['help', 'what can you do', 'how do you work']):
            return 'help'
        elif any(word in user_input_lower for word in ['thank', 'thanks', 'appreciate']):
            return 'gratitude'
        elif any(word in user_input_lower for word in ['bye', 'goodbye', 'see you']):
            return 'farewell'
        else:
            return 'symptom_query'
    
    def _calculate_confidence(self, symptoms: List[str], conditions: List[Dict]) -> float:
        """Calculate confidence score"""
        if not conditions:
            return 0.0
        
        # Base confidence on number of symptoms and match scores
        symptom_score = min(len(symptoms) * 0.2, 0.5)
        match_score = conditions[0].get('similarity_score', 0) * 0.5
        
        return min(symptom_score + match_score, 1.0)
    
    def generate_response(self, analysis: Dict) -> str:
        """Generate chatbot response based on analysis"""
        intent = analysis['intent']
        
        if intent == 'greeting':
            return ("Hello! I'm MediBot, your AI health assistant. I can help you understand "
                   "your symptoms and provide preliminary health advice. Please describe your symptoms, "
                   "and I'll do my best to assist you. Remember, I'm not a replacement for professional "
                   "medical advice.")
        
        elif intent == 'help':
            return ("I can help you by:\n"
                   "1. Analyzing your symptoms\n"
                   "2. Suggesting possible conditions\n"
                   "3. Providing preliminary health advice\n"
                   "4. Recommending when to see a doctor\n\n"
                   "Just describe your symptoms, and I'll assist you!")
        
        elif intent == 'gratitude':
            return "You're welcome! Take care and don't hesitate to reach out if you need more help."
        
        elif intent == 'farewell':
            return "Goodbye! Stay healthy and take care. Consult a healthcare professional if symptoms persist."
        
        else:  # symptom_query
            return self._generate_medical_response(analysis)
    
    def _generate_medical_response(self, analysis: Dict) -> str:
        """Generate response for symptom queries"""
        symptoms = analysis['detected_symptoms']
        conditions = analysis['matched_conditions']
        confidence = analysis['confidence']
        
        if not symptoms and not conditions:
            return ("I couldn't detect any specific symptoms from your message. "
                   "Could you please describe your symptoms in more detail? "
                   "For example, 'I have a headache and fever' or 'I'm experiencing chest pain'.")
        
        response = ""
        
        if symptoms:
            response += f"Based on your description, I've detected the following symptoms:\n"
            response += "- " + "\n- ".join(symptoms) + "\n\n"
        
        if conditions:
            response += "Possible conditions that match your symptoms:\n\n"
            
            for i, condition in enumerate(conditions, 1):
                response += f"{i}. **{condition['condition']}** (Severity: {condition['severity']})\n"
                response += f"   Common symptoms: {', '.join(condition['symptoms'][:5])}\n"
                response += f"   Advice: {condition['advice']}\n\n"
            
            response += "\n⚠️ **Important Disclaimer:**\n"
            response += ("This is preliminary information only. Please consult a qualified healthcare "
                        "professional for proper diagnosis and treatment. If you're experiencing severe "
                        "symptoms or a medical emergency, call emergency services immediately.")
        else:
            response += ("I found some symptoms but couldn't match them to specific conditions in my "
                        "knowledge base. Please consult a healthcare professional for proper evaluation.")
        
        return response