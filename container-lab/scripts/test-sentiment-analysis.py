#!/usr/bin/env python3
"""
Sentiment Analysis Test Script
Tests sentiment analysis with opinion mining capabilities
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

def analyze_sentiment(texts: List[str], use_container: bool = True, show_opinions: bool = True) -> Dict:
    """
    Analyze sentiment for given texts with opinion mining
    
    Args:
        texts: List of text strings to analyze
        use_container: If True, use local container; if False, use cloud service
        show_opinions: If True, include opinion mining
    
    Returns:
        Dictionary with sentiment results
    """
    
    # Prepare the request
    documents = [{"id": str(i+1), "text": text, "language": "en"} for i, text in enumerate(texts)]
    data = {"documents": documents}
    
    # Set endpoint based on container vs cloud
    if use_container:
        url = f"http://localhost:5000/text/analytics/v3.1/sentiment"
    else:
        url = f"{ENDPOINT}/text/analytics/v3.1/sentiment"
    
    # Add opinion mining parameter if requested
    if show_opinions:
        url += "?opinionMining=true"
    
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": API_KEY
    }
    
    print(f"\n{'='*60}")
    print(f"Testing Sentiment Analysis ({'Container' if use_container else 'Cloud'})")
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
            original_text = texts[int(doc_id) - 1]
            
            print(f"\nDocument {doc_id}:")
            print(f"  Text: {original_text[:100]}...")
            print(f"  Overall Sentiment: {doc['sentiment'].upper()}")
            print(f"  Confidence Scores:")
            print(f"    • Positive: {doc['confidenceScores']['positive']:.3f}")
            print(f"    • Neutral:  {doc['confidenceScores']['neutral']:.3f}")
            print(f"    • Negative: {doc['confidenceScores']['negative']:.3f}")
            
            # Show sentence-level sentiment
            if "sentences" in doc:
                print(f"\n  Sentence-level Analysis:")
                for i, sentence in enumerate(doc["sentences"], 1):
                    print(f"    Sentence {i}: {sentence['sentiment']} "
                          f"(Pos: {sentence['confidenceScores']['positive']:.2f}, "
                          f"Neu: {sentence['confidenceScores']['neutral']:.2f}, "
                          f"Neg: {sentence['confidenceScores']['negative']:.2f})")
                    print(f"      \"{sentence['text'][:60]}...\"")
                    
                    # Show opinion mining results if available
                    if "targets" in sentence:
                        for target in sentence["targets"]:
                            print(f"      Target: '{target['text']}' - {target['sentiment']}")
                            if "assessments" in target:
                                for assessment in target["assessments"]:
                                    print(f"        Assessment: '{assessment['text']}' - {assessment['sentiment']}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def main():
    """Main test function"""
    
    # Test samples with various sentiments
    test_texts = [
        # Positive review
        "The restaurant was absolutely fantastic! The food was delicious, the service was impeccable, and the atmosphere was perfect. I highly recommend this place to everyone.",
        
        # Negative review
        "Terrible experience. The food was cold, the service was slow and rude, and the restaurant was dirty. I will never come back here again.",
        
        # Mixed sentiment with aspects
        "The laptop has an excellent screen and great battery life, but the keyboard is uncomfortable and the trackpad is unresponsive. The price is reasonable though.",
        
        # Neutral/factual text
        "The meeting is scheduled for 3 PM tomorrow in conference room B. Please bring your project reports and any relevant documentation.",
        
        # Complex sentiment with multiple opinions
        "I love the new features in this software update, especially the improved UI. However, the performance has gotten worse, and it crashes frequently. The customer support team was helpful when I reported the issues, but the fixes are taking too long."
    ]
    
    print("\n" + "="*60)
    print("Azure AI Sentiment Analysis Test")
    print("="*60)
    
    # Test with container (if running)
    print("\n1. Testing with Local Container:")
    container_result = analyze_sentiment(test_texts, use_container=True, show_opinions=True)
    
    # Show interpretation guide
    print("\n" + "="*60)
    print("Sentiment Analysis Interpretation Guide")
    print("="*60)
    print("• Positive: Confidence > 0.6 indicates positive sentiment")
    print("• Negative: Confidence > 0.6 indicates negative sentiment")
    print("• Neutral: High neutral score indicates factual/objective content")
    print("• Mixed: Similar scores across categories indicate mixed sentiment")
    print("\nOpinion Mining identifies:")
    print("• Targets: What is being discussed (product, service, feature)")
    print("• Assessments: How the target is described (good, bad, excellent)")

if __name__ == "__main__":
    main()