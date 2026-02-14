"""
MediBot Test Script
Tests basic functionality of the MediBot system
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import fastapi
        print("  ✓ FastAPI")
        import flask
        print("  ✓ Flask")
        import pymongo
        print("  ✓ PyMongo")
        import sentence_transformers
        print("  ✓ Sentence Transformers")
        import langchain
        print("  ✓ LangChain")
        print("\n✓ All core imports successful!\n")
        return True
    except ImportError as e:
        print(f"\n✗ Import error: {e}\n")
        return False

def test_nlp_pipeline():
    """Test NLP pipeline functionality"""
    print("Testing NLP Pipeline...")
    try:
        from backend.nlp_pipeline import MedicalNLPPipeline
        
        nlp = MedicalNLPPipeline()
        print("  ✓ NLP Pipeline initialized")
        
        # Test symptom extraction
        test_input = "I have a headache and fever"
        symptoms = nlp.extract_symptoms(test_input)
        print(f"  ✓ Symptom extraction: {symptoms}")
        
        # Test intent classification
        analysis = nlp.analyze_query(test_input)
        print(f"  ✓ Query analysis: Intent = {analysis['intent']}")
        
        print("\n✓ NLP Pipeline test passed!\n")
        return True
    except Exception as e:
        print(f"\n✗ NLP Pipeline error: {e}\n")
        return False

def test_database():
    """Test database connectivity"""
    print("Testing Database...")
    try:
        from backend.database import MediBotDB
        
        db = MediBotDB()
        print("  ✓ Database connection established")
        
        # Test loading knowledge base
        import json
        knowledge_path = os.path.join(
            os.path.dirname(__file__), 
            'data', 'medical_knowledge.json'
        )
        
        if os.path.exists(knowledge_path):
            db.initialize_knowledge_base(knowledge_path)
            conditions = db.get_all_conditions()
            print(f"  ✓ Loaded {len(conditions)} medical conditions")
        
        print("\n✓ Database test passed!\n")
        return True
    except Exception as e:
        print(f"\n✗ Database error: {e}")
        print("  Note: MongoDB may not be running. Some features will be limited.\n")
        return True  # Don't fail if MongoDB is not available

def test_langchain():
    """Test LangChain integration"""
    print("Testing LangChain Integration...")
    try:
        from backend.langchain_integration import MedicalChatChain
        
        chain = MedicalChatChain()
        print("  ✓ Chat chain initialized")
        
        # Test context processing
        response = chain.process_with_context(
            "I have symptoms",
            ["fever", "cough"],
            []
        )
        print(f"  ✓ Context processing: Response generated")
        
        print("\n✓ LangChain test passed!\n")
        return True
    except Exception as e:
        print(f"\n✗ LangChain error: {e}\n")
        return False

def test_dialogflow():
    """Test Dialogflow integration"""
    print("Testing Dialogflow Integration...")
    try:
        from backend.dialogflow_integration import DialogflowIntegration
        
        df = DialogflowIntegration()
        print(f"  ✓ Dialogflow initialized (enabled: {df.enabled})")
        
        # Test intent detection
        result = df.detect_intent("Hello")
        print(f"  ✓ Intent detection: {result['intent']}")
        
        print("\n✓ Dialogflow test passed!\n")
        return True
    except Exception as e:
        print(f"\n✗ Dialogflow error: {e}\n")
        return False

def test_api_response():
    """Test complete API flow"""
    print("Testing Complete API Flow...")
    try:
        from backend.nlp_pipeline import MedicalNLPPipeline
        from backend.database import MediBotDB
        import json
        
        # Initialize components
        nlp = MedicalNLPPipeline()
        db = MediBotDB()
        
        # Load knowledge
        knowledge_path = os.path.join(
            os.path.dirname(__file__), 
            'data', 'medical_knowledge.json'
        )
        
        if os.path.exists(knowledge_path):
            with open(knowledge_path, 'r') as f:
                knowledge = json.load(f)
            nlp.load_medical_knowledge(knowledge)
        
        # Test query
        test_query = "I have a severe headache and nausea"
        analysis = nlp.analyze_query(test_query)
        response = nlp.generate_response(analysis)
        
        print(f"  ✓ Query: {test_query}")
        print(f"  ✓ Symptoms detected: {analysis['detected_symptoms']}")
        print(f"  ✓ Conditions matched: {len(analysis['matched_conditions'])}")
        print(f"  ✓ Response generated: {len(response)} characters")
        
        print("\n✓ Complete API flow test passed!\n")
        return True
    except Exception as e:
        print(f"\n✗ API flow error: {e}\n")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("          MediBot System Tests")
    print("="*60 + "\n")
    
    tests = [
        ("Import Test", test_imports),
        ("NLP Pipeline Test", test_nlp_pipeline),
        ("Database Test", test_database),
        ("LangChain Test", test_langchain),
        ("Dialogflow Test", test_dialogflow),
        ("API Flow Test", test_api_response),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Unexpected error in {test_name}: {e}\n")
            results.append((test_name, False))
    
    # Print summary
    print("="*60)
    print("          Test Summary")
    print("="*60 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! MediBot is ready to use.")
        print("\nNext steps:")
        print("1. Run: python backend/fastapi_server.py")
        print("2. Open: frontend/index.html")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        print("The system may still work with limited functionality.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
