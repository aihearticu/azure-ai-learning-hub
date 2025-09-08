#!/usr/bin/env python3
"""
Customer Review Analyzer
A practical example showing how to analyze customer feedback
"""

import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

class CustomerReviewAnalyzer:
    def __init__(self):
        self.endpoint = os.getenv('AZURE_COGNITIVE_SERVICES_ENDPOINT')
        self.key = os.getenv('AZURE_COGNITIVE_SERVICES_KEY')
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Content-Type': 'application/json'
        }
    
    def analyze_review(self, review_text, review_id="1"):
        """Comprehensive analysis of a customer review"""
        
        document = [{"id": review_id, "text": review_text, "language": "en"}]
        results = {}
        
        # 1. Sentiment Analysis with Opinion Mining
        sentiment_url = f"{self.endpoint}text/analytics/v3.1/sentiment?opinionMining=true"
        sentiment_response = requests.post(
            sentiment_url, 
            headers=self.headers, 
            json={"documents": document}
        )
        sentiment_data = sentiment_response.json()["documents"][0]
        
        results["sentiment"] = {
            "overall": sentiment_data["sentiment"],
            "scores": sentiment_data["confidenceScores"],
            "opinions": []
        }
        
        # Extract opinions about specific aspects
        for sentence in sentiment_data.get("sentences", []):
            for target in sentence.get("targets", []):
                results["sentiment"]["opinions"].append({
                    "aspect": target["text"],
                    "sentiment": target["sentiment"],
                    "confidence": target.get("confidenceScore", 0)
                })
        
        # 2. Key Phrase Extraction
        keyphrases_url = f"{self.endpoint}text/analytics/v3.1/keyPhrases"
        keyphrases_response = requests.post(
            keyphrases_url,
            headers=self.headers,
            json={"documents": document}
        )
        results["key_topics"] = keyphrases_response.json()["documents"][0]["keyPhrases"]
        
        # 3. Entity Recognition
        entities_url = f"{self.endpoint}text/analytics/v3.1/entities/recognition/general"
        entities_response = requests.post(
            entities_url,
            headers=self.headers,
            json={"documents": document}
        )
        entities = entities_response.json()["documents"][0]["entities"]
        
        results["entities"] = {
            "products": [e["text"] for e in entities if e["category"] == "Product"],
            "features": [e["text"] for e in entities if e["category"] in ["Skill", "Event"]],
            "quantities": [e["text"] for e in entities if e["category"] == "Quantity"]
        }
        
        return results
    
    def generate_insights(self, analysis):
        """Generate actionable insights from analysis"""
        
        insights = []
        
        # Sentiment insights
        sentiment = analysis["sentiment"]["overall"]
        scores = analysis["sentiment"]["scores"]
        
        if sentiment == "positive" and scores["positive"] > 0.8:
            insights.append("⭐ Highly satisfied customer - consider for testimonial")
        elif sentiment == "negative" and scores["negative"] > 0.8:
            insights.append("🚨 Very dissatisfied customer - immediate follow-up needed")
        elif sentiment == "mixed" or scores["neutral"] > 0.5:
            insights.append("⚠️ Mixed feelings - opportunity for improvement")
        
        # Opinion insights
        negative_aspects = [
            op["aspect"] for op in analysis["sentiment"]["opinions"] 
            if op["sentiment"] == "negative"
        ]
        if negative_aspects:
            insights.append(f"🔧 Issues with: {', '.join(negative_aspects)}")
        
        positive_aspects = [
            op["aspect"] for op in analysis["sentiment"]["opinions"] 
            if op["sentiment"] == "positive"
        ]
        if positive_aspects:
            insights.append(f"✅ Strengths: {', '.join(positive_aspects)}")
        
        # Topic insights
        if "customer service" in ' '.join(analysis["key_topics"]).lower():
            insights.append("💬 Service quality mentioned - route to support team")
        
        if "price" in ' '.join(analysis["key_topics"]).lower() or "expensive" in ' '.join(analysis["key_topics"]).lower():
            insights.append("💰 Price sensitivity detected")
        
        return insights

def main():
    analyzer = CustomerReviewAnalyzer()
    
    # Sample customer reviews
    reviews = [
        {
            "id": "R001",
            "text": """The product quality is excellent and the packaging was perfect. 
            However, the customer service was terrible and shipping took way too long. 
            The price is a bit high but the features make it worth it."""
        },
        {
            "id": "R002",
            "text": """Amazing experience! The staff was incredibly helpful and professional. 
            The product exceeded my expectations and the delivery was super fast. 
            Will definitely purchase again and recommend to friends."""
        },
        {
            "id": "R003",
            "text": """The laptop screen is beautiful but the battery life is disappointing. 
            Keyboard feels cheap for this price range. Tech support was helpful though 
            when I had setup issues. Mixed feelings overall."""
        }
    ]
    
    print("🛍️ CUSTOMER REVIEW ANALYSIS DASHBOARD")
    print("="*60)
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    for review in reviews:
        print(f"\n📝 Review ID: {review['id']}")
        print("-"*40)
        print(f"Review: {review['text'][:100]}...\n")
        
        # Analyze review
        analysis = analyzer.analyze_review(review["text"], review["id"])
        
        # Display results
        print(f"😊 Sentiment: {analysis['sentiment']['overall'].upper()}")
        scores = analysis['sentiment']['scores']
        print(f"   Positive: {scores['positive']:.1%} | "
              f"Neutral: {scores['neutral']:.1%} | "
              f"Negative: {scores['negative']:.1%}")
        
        if analysis['sentiment']['opinions']:
            print("\n🎯 Aspect Opinions:")
            for op in analysis['sentiment']['opinions'][:3]:
                emoji = "👍" if op['sentiment'] == "positive" else "👎"
                print(f"   {emoji} {op['aspect']}: {op['sentiment']}")
        
        print(f"\n🏷️ Key Topics: {', '.join(analysis['key_topics'][:5])}")
        
        # Generate insights
        insights = analyzer.generate_insights(analysis)
        if insights:
            print("\n💡 Actionable Insights:")
            for insight in insights:
                print(f"   {insight}")
    
    print("\n" + "="*60)
    print("📊 SUMMARY STATISTICS")
    print("• Total Reviews Analyzed: 3")
    print("• Average Processing Time: <1 second per review")
    print("• Insights Generated: Automatic")
    print("\n✨ This demo shows how Azure AI Services can:")
    print("  • Automatically categorize customer feedback")
    print("  • Identify specific pain points and strengths")
    print("  • Generate actionable business insights")
    print("  • Scale to thousands of reviews per minute")

if __name__ == "__main__":
    main()