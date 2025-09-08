#!/usr/bin/env python3
"""
Named Entity Recognition Test Script
Tests entity recognition including PII detection capabilities
"""

import requests
import json
import os
from dotenv import load_dotenv
from typing import List, Dict
import time
from collections import defaultdict

# Load environment variables
load_dotenv()

# Configuration
ENDPOINT = os.getenv('AZURE_COGNITIVE_SERVICES_ENDPOINT', 'http://localhost:5000')
API_KEY = os.getenv('AZURE_COGNITIVE_SERVICES_KEY')

def recognize_entities(texts: List[str], use_container: bool = True) -> Dict:
    """
    Recognize named entities in given texts
    
    Args:
        texts: List of text strings to analyze
        use_container: If True, use local container; if False, use cloud service
    
    Returns:
        Dictionary with entity recognition results
    """
    
    # Prepare the request
    documents = [{"id": str(i+1), "text": text, "language": "en"} for i, text in enumerate(texts)]
    data = {"documents": documents}
    
    # Set endpoint based on container vs cloud
    if use_container:
        url = f"http://localhost:5000/text/analytics/v3.1/entities/recognition/general"
    else:
        url = f"{ENDPOINT}/text/analytics/v3.1/entities/recognition/general"
    
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": API_KEY
    }
    
    print(f"\n{'='*60}")
    print(f"Testing Named Entity Recognition ({'Container' if use_container else 'Cloud'})")
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
            entities = doc.get("entities", [])
            
            print(f"\nDocument {doc_id}:")
            print(f"  Text Preview: {original_text[:150]}...")
            print(f"  \nRecognized Entities ({len(entities)} found):")
            
            # Group entities by category
            entities_by_category = defaultdict(list)
            for entity in entities:
                entities_by_category[entity["category"]].append(entity)
            
            # Display entities by category
            for category, category_entities in sorted(entities_by_category.items()):
                print(f"\n  {category}:")
                for entity in category_entities[:5]:  # Show max 5 per category
                    confidence = f" (confidence: {entity['confidenceScore']:.2f})" if 'confidenceScore' in entity else ""
                    subcategory = f" [{entity.get('subcategory', '')}]" if entity.get('subcategory') else ""
                    print(f"    • {entity['text']}{subcategory}{confidence}")
                    
                    # Show linked entity if available
                    if "links" in entity and entity["links"]:
                        for link in entity["links"][:1]:  # Show first link only
                            print(f"      Wikipedia: {link.get('url', 'N/A')}")
                
                if len(category_entities) > 5:
                    print(f"    ... and {len(category_entities) - 5} more")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return None

def recognize_pii(texts: List[str], use_container: bool = True) -> Dict:
    """
    Recognize PII (Personally Identifiable Information) in texts
    
    Args:
        texts: List of text strings to analyze
        use_container: If True, use local container; if False, use cloud service
    
    Returns:
        Dictionary with PII detection results
    """
    
    # Prepare the request
    documents = [{"id": str(i+1), "text": text, "language": "en"} for i, text in enumerate(texts)]
    data = {"documents": documents}
    
    # Set endpoint based on container vs cloud
    if use_container:
        url = f"http://localhost:5000/text/analytics/v3.1/entities/recognition/pii"
    else:
        url = f"{ENDPOINT}/text/analytics/v3.1/entities/recognition/pii"
    
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": API_KEY
    }
    
    print(f"\n{'='*60}")
    print(f"Testing PII Detection ({'Container' if use_container else 'Cloud'})")
    print(f"{'='*60}")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        print("\nPII Detection Results:")
        print("-" * 40)
        
        for doc in result.get("documents", []):
            doc_id = doc["id"]
            entities = doc.get("entities", [])
            redacted_text = doc.get("redactedText", "")
            
            print(f"\nDocument {doc_id}:")
            
            if entities:
                print(f"  ⚠️  {len(entities)} PII entities detected:")
                for entity in entities:
                    print(f"    • {entity['category']}: {entity['text']} (confidence: {entity['confidenceScore']:.2f})")
                
                if redacted_text:
                    print(f"\n  Redacted Text:")
                    print(f"    {redacted_text[:200]}...")
            else:
                print("  ✓ No PII detected")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error: {e}")
        return None

def main():
    """Main test function"""
    
    # Test samples with various entity types
    test_texts = [
        # Business context with organizations and people
        """Microsoft CEO Satya Nadella announced a strategic partnership with OpenAI in Seattle yesterday. 
        The $10 billion investment will accelerate AI development. The announcement took place at the 
        Microsoft headquarters in Redmond, Washington. Bill Gates, who founded Microsoft in 1975, 
        attended the event along with Sam Altman from OpenAI.""",
        
        # Travel and location entities
        """I'm planning a trip to Tokyo, Japan next summer. I'll fly from New York's JFK Airport 
        on United Airlines flight UA837. The hotel is near Mount Fuji, about 100 kilometers from Tokyo. 
        I plan to visit Kyoto's temples and experience the bullet train to Osaka. The trip costs $3,500 
        including flights and accommodation for 10 days.""",
        
        # Healthcare and scientific entities
        """Dr. Sarah Johnson from Johns Hopkins Hospital published groundbreaking research on COVID-19 
        treatments in the New England Journal of Medicine. The study involved 1,200 patients across 
        15 hospitals in the United States. The FDA approved the new treatment protocol last month. 
        Results show a 40% reduction in hospitalization rates.""",
        
        # PII sample text
        """Please contact John Smith at john.smith@email.com or call him at 555-123-4567. 
        His social security number is 123-45-6789 and his date of birth is January 15, 1985. 
        He lives at 123 Main Street, Apt 4B, New York, NY 10001. His credit card number 
        ending in 4532 was used for the purchase. His employee ID is EMP-2024-0156."""
    ]
    
    print("\n" + "="*60)
    print("Azure AI Entity Recognition Test Suite")
    print("="*60)
    
    # Test general entity recognition
    print("\n1. General Entity Recognition:")
    container_result = recognize_entities(test_texts, use_container=True)
    
    # Test PII detection
    print("\n2. PII Detection:")
    pii_result = recognize_pii([test_texts[-1]], use_container=True)  # Use only the PII sample
    
    # Show entity categories guide
    print("\n" + "="*60)
    print("Entity Categories Reference")
    print("="*60)
    print("General Entities:")
    print("• Person: Names of people")
    print("• Organization: Companies, agencies, institutions")
    print("• Location: Geographic locations, landmarks")
    print("• DateTime: Dates, times, periods")
    print("• Quantity: Numbers, amounts, percentages")
    print("• Product: Physical goods, vehicles, foods")
    print("• Event: Named hurricanes, battles, sports events")
    print("• Skill: Capabilities or expertise")
    print("\nPII Categories:")
    print("• Email, Phone Number, SSN")
    print("• Credit Card, Bank Account")
    print("• Address, Date of Birth")
    print("• Person Name, Organization")

if __name__ == "__main__":
    main()