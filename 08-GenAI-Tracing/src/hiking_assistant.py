#!/usr/bin/env python3
"""
Hiking Assistant with Tracing - GenAI Lab
This script implements a hiking trail recommendation system with distributed tracing
"""

import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Load environment variables
load_dotenv()

# Configure OpenTelemetry with Application Insights
def configure_tracing():
    """Configure OpenTelemetry tracing with Azure Application Insights"""
    
    # Set up the tracer provider
    trace.set_tracer_provider(TracerProvider())
    tracer_provider = trace.get_tracer_provider()
    
    # Configure Azure Monitor exporter
    connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if connection_string:
        azure_exporter = AzureMonitorTraceExporter(
            connection_string=connection_string
        )
        tracer_provider.add_span_processor(
            BatchSpanProcessor(azure_exporter)
        )
    
    # Instrument OpenAI
    OpenAIInstrumentor().instrument()
    
    return trace.get_tracer(__name__)

# Initialize tracer
tracer = configure_tracing()

# Initialize Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

# Product catalog for gear matching
PRODUCT_CATALOG = {
    "hiking_boots": [
        {"name": "TrailBlazer Pro", "price": 189.99, "rating": 4.5},
        {"name": "Mountain Master", "price": 259.99, "rating": 4.8},
        {"name": "Budget Hiker", "price": 89.99, "rating": 3.9}
    ],
    "backpacks": [
        {"name": "Summit 65L", "price": 299.99, "rating": 4.7},
        {"name": "DayTripper 25L", "price": 79.99, "rating": 4.3},
        {"name": "UltraLight 40L", "price": 199.99, "rating": 4.6}
    ],
    "water_bottles": [
        {"name": "HydroFlow 1L", "price": 29.99, "rating": 4.4},
        {"name": "ThermoGuard 750ml", "price": 39.99, "rating": 4.6},
        {"name": "Basic Bottle 500ml", "price": 9.99, "rating": 3.8}
    ],
    "trekking_poles": [
        {"name": "Carbon Elite", "price": 149.99, "rating": 4.8},
        {"name": "Aluminum Pro", "price": 89.99, "rating": 4.2},
        {"name": "Adjustable Comfort", "price": 119.99, "rating": 4.5}
    ]
}

def call_ai_model(messages, temperature=0.7, max_tokens=500):
    """Call Azure OpenAI model with tracing"""
    with tracer.start_as_current_span("call_ai_model") as span:
        span.set_attribute("model.temperature", temperature)
        span.set_attribute("model.max_tokens", max_tokens)
        span.set_attribute("model.deployment", os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"))
        
        try:
            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            content = response.choices[0].message.content
            span.set_attribute("response.length", len(content))
            span.set_status(Status(StatusCode.OK))
            
            return content
            
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            raise

def recommend_hikes(location, difficulty, duration):
    """Recommend hiking trails based on user preferences"""
    with tracer.start_as_current_span("recommend_hikes") as span:
        span.set_attribute("user.location", location)
        span.set_attribute("user.difficulty", difficulty)
        span.set_attribute("user.duration", duration)
        
        messages = [
            {"role": "system", "content": "You are a hiking expert. Recommend 3 hiking trails based on the user's preferences. Return as JSON array with fields: name, distance_km, elevation_gain_m, estimated_time_hours, difficulty, highlights"},
            {"role": "user", "content": f"Recommend 3 hiking trails near {location} with {difficulty} difficulty that take about {duration} hours."}
        ]
        
        response = call_ai_model(messages, temperature=0.8)
        
        try:
            trails = json.loads(response)
            span.set_attribute("trails.count", len(trails))
            return trails
        except json.JSONDecodeError:
            # If response isn't valid JSON, create a structured response
            span.add_event("JSON parsing failed, creating default response")
            return [
                {
                    "name": "Sample Trail",
                    "distance_km": 5,
                    "elevation_gain_m": 300,
                    "estimated_time_hours": duration,
                    "difficulty": difficulty,
                    "highlights": ["Scenic views", "Wildlife"]
                }
            ]

def generate_trip_profile(trails, user_experience):
    """Generate a personalized trip profile based on selected trails"""
    with tracer.start_as_current_span("generate_trip_profile") as span:
        span.set_attribute("user.experience", user_experience)
        span.set_attribute("trails.selected", len(trails))
        
        trail_summary = "\n".join([f"- {t['name']}: {t['distance_km']}km, {t['difficulty']}" for t in trails])
        
        messages = [
            {"role": "system", "content": "You are a hiking trip planner. Create a detailed trip profile with gear recommendations. Return as JSON with fields: trip_summary, required_gear, optional_gear, safety_tips, weather_considerations"},
            {"role": "user", "content": f"Create a trip profile for a {user_experience} hiker planning these trails:\n{trail_summary}"}
        ]
        
        response = call_ai_model(messages, temperature=0.7, max_tokens=600)
        
        try:
            profile = json.loads(response)
            span.set_attribute("profile.gear_items", len(profile.get("required_gear", [])))
            return profile
        except json.JSONDecodeError:
            span.add_event("JSON parsing failed, creating default profile")
            return {
                "trip_summary": "Hiking trip profile",
                "required_gear": ["hiking boots", "backpack", "water bottle"],
                "optional_gear": ["trekking poles", "GPS device"],
                "safety_tips": ["Tell someone your plans", "Check weather"],
                "weather_considerations": ["Check forecast", "Prepare for rain"]
            }

def match_products(gear_list):
    """Match recommended gear with products from catalog"""
    with tracer.start_as_current_span("match_products") as span:
        span.set_attribute("gear.requested", len(gear_list))
        
        matched_products = {}
        
        for gear_item in gear_list:
            with tracer.start_as_current_span(f"match_product_{gear_item}") as product_span:
                # Normalize gear item name for matching
                normalized_item = gear_item.lower().replace(" ", "_")
                
                # Find matching products in catalog
                for category, products in PRODUCT_CATALOG.items():
                    if normalized_item in category or category in normalized_item:
                        product_span.set_attribute("category.matched", category)
                        product_span.set_attribute("products.available", len(products))
                        
                        # Select best product based on rating
                        best_product = max(products, key=lambda x: x["rating"])
                        matched_products[gear_item] = best_product
                        
                        product_span.set_attribute("product.selected", best_product["name"])
                        product_span.set_attribute("product.price", best_product["price"])
                        break
        
        span.set_attribute("products.matched", len(matched_products))
        return matched_products

def main():
    """Main function to run the hiking assistant"""
    with tracer.start_as_current_span("hiking_assistant_main") as span:
        print("\n🏔️ Welcome to the AI Hiking Assistant with Tracing! 🏔️\n")
        
        # Get user preferences
        location = input("Where would you like to hike? (e.g., Seattle, Colorado): ") or "Seattle"
        difficulty = input("Difficulty level (easy/moderate/difficult): ").lower() or "moderate"
        duration = float(input("How many hours do you want to hike? (e.g., 3): ") or 3)
        experience = input("Your hiking experience (beginner/intermediate/expert): ").lower() or "intermediate"
        
        span.set_attribute("user.preferences.location", location)
        span.set_attribute("user.preferences.difficulty", difficulty)
        span.set_attribute("user.preferences.duration", duration)
        span.set_attribute("user.preferences.experience", experience)
        
        try:
            # Step 1: Recommend hikes
            print("\n🔍 Finding perfect trails for you...")
            trails = recommend_hikes(location, difficulty, duration)
            print(f"\n✅ Found {len(trails)} amazing trails!")
            
            for i, trail in enumerate(trails, 1):
                print(f"\n{i}. {trail.get('name', 'Unknown Trail')}")
                print(f"   Distance: {trail.get('distance_km', 'N/A')} km")
                print(f"   Elevation: {trail.get('elevation_gain_m', 'N/A')} m")
                print(f"   Time: {trail.get('estimated_time_hours', 'N/A')} hours")
            
            # Step 2: Generate trip profile
            print("\n📋 Creating your personalized trip profile...")
            profile = generate_trip_profile(trails, experience)
            
            print("\n🎒 Required Gear:")
            required_gear = profile.get("required_gear", [])
            for item in required_gear:
                print(f"   • {item}")
            
            # Step 3: Match products
            print("\n🛍️ Finding the best gear for your trip...")
            all_gear = required_gear + profile.get("optional_gear", [])
            products = match_products(all_gear)
            
            print("\n💰 Recommended Products:")
            total_cost = 0
            for gear, product in products.items():
                print(f"   {gear}: {product['name']} - ${product['price']:.2f} (⭐ {product['rating']})")
                total_cost += product['price']
            
            print(f"\n   Total estimated cost: ${total_cost:.2f}")
            
            # Add summary to span
            span.set_attribute("summary.trails", len(trails))
            span.set_attribute("summary.products", len(products))
            span.set_attribute("summary.total_cost", total_cost)
            span.set_status(Status(StatusCode.OK))
            
            print("\n✨ Your hiking plan is ready! Check Application Insights for trace details.")
            
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            print(f"\n❌ An error occurred: {e}")
            raise

if __name__ == "__main__":
    main()