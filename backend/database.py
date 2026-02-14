import os
from datetime import datetime
from typing import List, Dict
import json
from pymongo import MongoClient


class MediBotDB:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.db_name = os.getenv("MONGODB_DB_NAME", "medibot")
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        """Connect to MongoDB with proper error handling"""
        try:
            # Try to connect with shorter timeout
            self.client = MongoClient(
                self.mongo_uri,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
            
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            print(f"Connected to MongoDB: {self.db_name}")
            
        except Exception as e:
            print(f"MongoDB connection error: {e}")
            print("Running in offline mode without database")
            self.db = None
            self.client = None

    def initialize_knowledge_base(self, json_file_path: str):
        """Load medical knowledge into database"""
        if self.db is None:
            print("Database not available, using in-memory storage")
            return

        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                medical_data = json.load(f)

            collection = self.db["medical_knowledge"]
            collection.delete_many({})
            collection.insert_many(medical_data)

            print(f"Loaded {len(medical_data)} medical conditions into database")

        except Exception as e:
            print(f"Error loading knowledge base: {e}")

    def get_all_conditions(self) -> List[Dict]:
        """Retrieve all medical conditions"""
        if self.db is None:
            return []

        try:
            collection = self.db["medical_knowledge"]
            return list(collection.find({}, {"_id": 0}))
        except Exception as e:
            print(f"Error retrieving conditions: {e}")
            return []

    def search_by_symptoms(self, symptoms: List[str]) -> List[Dict]:
        """Search conditions by symptoms"""
        if self.db is None or not symptoms:
            return []

        try:
            collection = self.db["medical_knowledge"]
            query = {
                "$or": [
                    {"symptoms": {"$regex": symptom, "$options": "i"}}
                    for symptom in symptoms
                ]
            }
            return list(collection.find(query, {"_id": 0}))
        except Exception as e:
            print(f"Error searching symptoms: {e}")
            return []

    def log_conversation(
        self,
        user_id: str,
        user_message: str,
        bot_response: str,
        symptoms: List[str],
        matched_conditions: List[str]
    ):
        """Log conversation for analytics"""
        if self.db is None:
            return

        try:
            collection = self.db["conversations"]
            collection.insert_one({
                "user_id": user_id,
                "timestamp": datetime.utcnow(),
                "user_message": user_message,
                "bot_response": bot_response,
                "symptoms_detected": symptoms,
                "conditions_matched": matched_conditions
            })
        except Exception as e:
            print(f"Error logging conversation: {e}")

    def get_user_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history for a user"""
        if self.db is None:
            return []

        try:
            collection = self.db["conversations"]
            return list(
                collection.find({"user_id": user_id}, {"_id": 0})
                .sort("timestamp", -1)
                .limit(limit)
            )
        except Exception as e:
            print(f"Error retrieving history: {e}")
            return []

    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")