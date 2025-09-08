#!/usr/bin/env python3
"""
Language Detection Test Script
Tests the language detection capabilities of Azure AI Services Container
"""

import requests
import json
import os
from dotenv import load_dotenv
from typing import List, Dict
import time

# Load environment variables
load_dotenv()

# Configuration
ENDPOINT = os.getenv('AZURE_COGNITIVE_SERVICES_ENDPOINT', 'http://localhost:5000')
API_KEY = os.getenv('AZURE_COGNITIVE_SERVICES_KEY')

def detect_language(texts: List[str], use_container: bool = True) -> Dict:
    """
    Detect language for given texts
    
    Args:
        texts: List of text strings to analyze
        use_container: If True, use local container; if False, use cloud service
    
    Returns:
        Dictionary with detection results
    """
    
    # Prepare the request
    documents = [{"id": str(i+1), "text": text} for i, text in enumerate(texts)]
    data = {"documents": documents}
    
    # Set endpoint based on container vs cloud
    if use_container:
        url = f"http://localhost:5000/text/analytics/v3.1/languages"
    else:
        url = f"{ENDPOINT}/text/analytics/v3.1/languages"
    
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": API_KEY
    }
    
    print(f"\n{'='*60}")
    print(f"Testing Language Detection ({'Container' if use_container else 'Cloud'})")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        elapsed_time = time.time() - start_time
        
        print(f"\nResponse Time: {elapsed_time:.3f} seconds")
        print("\nResults:")
        print("-" * 40)
        
        for doc in result.get("documents", []):
            doc_id = doc["id"]
            original_text = texts[int(doc_id) - 1][:50] + "..." if len(texts[int(doc_id) - 1]) > 50 else texts[int(doc_id) - 1]
            detected_lang = doc["detectedLanguage"]
            
            print(f"\nDocument {doc_id}:")
            print(f"  Text: {original_text}")
            print(f"  Detected Language: {detected_lang['name']} ({detected_lang['iso6391Name']})")
            print(f"  Confidence Score: {detected_lang['confidenceScore']:.3f}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def main():
    """Main test function"""
    
    # Test samples in different languages
    test_texts = [
        "Hello, how are you doing today? This is a test of language detection.",  # English
        "Bonjour, comment allez-vous aujourd'hui? Ceci est un test.",  # French
        "Hola, ¿cómo estás hoy? Esta es una prueba de detección de idioma.",  # Spanish
        "こんにちは、今日はどうですか？これは言語検出のテストです。",  # Japanese
        "Здравствуйте, как у вас дела сегодня? Это тест определения языка.",  # Russian
        "你好，你今天好吗？这是语言检测测试。",  # Chinese
        "مرحبا، كيف حالك اليوم؟ هذا اختبار للكشف عن اللغة.",  # Arabic
        "Olá, como está hoje? Este é um teste de detecção de idioma.",  # Portuguese
    ]
    
    print("\n" + "="*60)
    print("Azure AI Language Detection Test")
    print("="*60)
    
    # Test with container (if running)
    print("\n1. Testing with Local Container:")
    container_result = detect_language(test_texts, use_container=True)
    
    # Optionally test with cloud service for comparison
    print("\n2. Testing with Cloud Service (for comparison):")
    cloud_result = detect_language(test_texts, use_container=False)
    
    # Performance comparison
    if container_result and cloud_result:
        print("\n" + "="*60)
        print("Performance Comparison Summary")
        print("="*60)
        print("✓ Both container and cloud service successfully processed the requests")
        print("✓ Container provides local processing without internet dependency")
        print("✓ Cloud service may have more recent model updates")

if __name__ == "__main__":
    main()