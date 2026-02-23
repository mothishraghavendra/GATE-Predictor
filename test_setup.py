"""
Simple test script to verify the GATE Mark Predictor application setup
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import flask
        print("  ✅ Flask imported successfully")
    except ImportError as e:
        print(f"  ❌ Flask import failed: {e}")
        return False
    
    try:
        import flask_wtf
        print("  ✅ Flask-WTF imported successfully")
    except ImportError as e:
        print(f"  ❌ Flask-WTF import failed: {e}")
        return False
    
    try:
        import requests
        print("  ✅ Requests imported successfully")
    except ImportError as e:
        print(f"  ❌ Requests import failed: {e}")
        return False
    
    try:
        import bs4
        print("  ✅ BeautifulSoup4 imported successfully")
    except ImportError as e:
        print(f"  ❌ BeautifulSoup4 import failed: {e}")
        return False
    
    try:
        from scraper import ResponseSheetScraper
        print("  ✅ Scraper module imported successfully")
    except ImportError as e:
        print(f"  ❌ Scraper module import failed: {e}")
        return False
    
    try:
        from predictor import MarkPredictor
        print("  ✅ Predictor module imported successfully")
    except ImportError as e:
        print(f"  ❌ Predictor module import failed: {e}")
        return False
    
    return True

def test_predictor():
    """Test the mark predictor with sample data"""
    print("\n🧪 Testing Mark Predictor...")
    
    try:
        from predictor import MarkPredictor
        
        # Sample response data
        sample_data = {
            'questions': [
                {'number': i, 'response': 'A' if i % 2 == 0 else '', 'marked': i % 2 == 0}
                for i in range(1, 66)
            ],
            'statistics': {
                'total_questions': 65,
                'attempted': 33,
                'not_attempted': 32
            }
        }
        
        predictor = MarkPredictor()
        result = predictor.predict(sample_data)
        
        print(f"  ✅ Prediction successful!")
        print(f"     Predicted Score: {result['predicted_score']}")
        print(f"     Best Case: {result['best_case_score']}")
        print(f"     Worst Case: {result['worst_case_score']}")
        print(f"     Estimated Accuracy: {result['accuracy_estimate']}%")
        
        return True
    except Exception as e:
        print(f"  ❌ Predictor test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files and directories exist"""
    print("\n🧪 Testing file structure...")
    
    required_files = [
        'app.py',
        'config.py',
        'scraper.py',
        'predictor.py',
        'requirements.txt',
        'templates/base.html',
        'templates/index.html',
        'templates/result.html',
        'static/css/style.css'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path} exists")
        else:
            print(f"  ❌ {file_path} is missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("=" * 60)
    print("GATE Mark Predictor - Setup Verification")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: File structure
    results.append(("File Structure", test_file_structure()))
    
    # Test 2: Imports
    results.append(("Module Imports", test_imports()))
    
    # Test 3: Predictor
    results.append(("Mark Predictor", test_predictor()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✨ All tests passed! Your application is ready to run.")
        print("\n🚀 To start the application, run:")
        print("   ./run.sh")
        print("   OR")
        print("   python app.py")
        print("\n📍 Then visit: http://localhost:5000")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please install dependencies:")
        print("   pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
