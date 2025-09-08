#!/usr/bin/env python3
"""
Key Phrase Extraction Test Script
Tests the key phrase extraction capabilities
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

def extract_key_phrases(texts: List[str], use_container: bool = True) -> Dict:
    """
    Extract key phrases from given texts
    
    Args:
        texts: List of text strings to analyze
        use_container: If True, use local container; if False, use cloud service
    
    Returns:
        Dictionary with key phrase results
    """
    
    # Prepare the request
    documents = [{"id": str(i+1), "text": text, "language": "en"} for i, text in enumerate(texts)]
    data = {"documents": documents}
    
    # Set endpoint based on container vs cloud
    if use_container:
        url = f"http://localhost:5000/text/analytics/v3.1/keyPhrases"
    else:
        url = f"{ENDPOINT}/text/analytics/v3.1/keyPhrases"
    
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": API_KEY
    }
    
    print(f"\n{'='*60}")
    print(f"Testing Key Phrase Extraction ({'Container' if use_container else 'Cloud'})")
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
            key_phrases = doc["keyPhrases"]
            
            print(f"\nDocument {doc_id}:")
            print(f"  Text Preview: {original_text[:150]}...")
            print(f"  \nExtracted Key Phrases ({len(key_phrases)} found):")
            
            if key_phrases:
                # Group phrases by approximate importance (longer phrases often more specific)
                sorted_phrases = sorted(key_phrases, key=lambda x: len(x.split()), reverse=True)
                
                print("\n  Most Specific Concepts:")
                for phrase in sorted_phrases[:5]:
                    print(f"    • {phrase}")
                
                if len(sorted_phrases) > 5:
                    print("\n  Additional Key Terms:")
                    for phrase in sorted_phrases[5:10]:
                        print(f"    • {phrase}")
                
                # Show word cloud representation
                print("\n  Word Frequency Visualization:")
                word_freq = {}
                for phrase in key_phrases:
                    words = phrase.lower().split()
                    for word in words:
                        word_freq[word] = word_freq.get(word, 0) + 1
                
                top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:8]
                for word, freq in top_words:
                    bar = "█" * (freq * 3)
                    print(f"    {word:15} {bar} ({freq})")
            else:
                print("    No key phrases extracted")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def main():
    """Main test function"""
    
    # Test samples from different domains
    test_texts = [
        # Technology article
        """Artificial intelligence and machine learning are revolutionizing the healthcare industry. 
        Deep learning algorithms can now detect diseases like cancer with remarkable accuracy. 
        Natural language processing helps doctors analyze patient records more efficiently. 
        Computer vision technologies enable automated analysis of medical imaging such as X-rays and MRI scans. 
        These AI-powered diagnostic tools are improving patient outcomes while reducing healthcare costs.""",
        
        # Business report
        """The quarterly earnings report shows strong revenue growth in the cloud computing division. 
        Digital transformation initiatives drove a 25% increase in enterprise software sales. 
        The company's strategic partnerships with leading technology providers enhanced market penetration. 
        Customer acquisition costs decreased while lifetime value increased significantly. 
        Investment in research and development remains a key priority for maintaining competitive advantage.""",
        
        # Scientific abstract
        """This study investigates the effects of climate change on coral reef ecosystems in the Pacific Ocean. 
        Rising ocean temperatures and acidification are causing widespread coral bleaching events. 
        Biodiversity loss threatens the marine food chain and coastal communities that depend on reef resources. 
        Conservation strategies including marine protected areas and coral restoration programs show promising results. 
        Sustainable fishing practices and reduced carbon emissions are essential for long-term reef survival.""",
        
        # Product review
        """The new smartphone features an impressive OLED display with 120Hz refresh rate. 
        Battery life lasts all day with moderate usage, and the fast charging is incredibly convenient. 
        The camera system includes telephoto and ultra-wide lenses that capture stunning photos. 
        5G connectivity provides blazing fast download speeds in supported areas. 
        The premium build quality justifies the high price point for power users."""
    ]
    
    print("\n" + "="*60)
    print("Azure AI Key Phrase Extraction Test")
    print("="*60)
    
    # Test with container (if running)
    print("\n1. Testing with Local Container:")
    container_result = extract_key_phrases(test_texts, use_container=True)
    
    # Analysis summary
    print("\n" + "="*60)
    print("Key Phrase Extraction Use Cases")
    print("="*60)
    print("✓ Content Summarization: Quickly identify main topics")
    print("✓ SEO Optimization: Extract relevant keywords for search")
    print("✓ Document Categorization: Classify documents by key concepts")
    print("✓ Trend Analysis: Track important terms over time")
    print("✓ Knowledge Extraction: Build knowledge graphs from text")

if __name__ == "__main__":
    main()