#!/usr/bin/env python3
"""
Hiking Assistant with Intentional Error - For Tracing Debug Exercise
This script has an intentional JSON parsing error to demonstrate error tracing
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
    
    trace.set_tracer_provider(TracerProvider())
    tracer_provider = trace.get_tracer_provider()
    
    connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if connection_string:
        azure_exporter = AzureMonitorTraceExporter(
            connection_string=connection_string
        )
        tracer_provider.add_span_processor(
            BatchSpanProcessor(azure_exporter)
        )
    
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

def call_ai_model_with_error(messages, temperature=0.7, max_tokens=500):
    """Call Azure OpenAI model - INTENTIONALLY RETURNS MALFORMED JSON"""
    with tracer.start_as_current_span("call_ai_model_with_error") as span:
        span.set_attribute("model.temperature", temperature)
        span.set_attribute("model.max_tokens", max_tokens)
        span.set_attribute("error.intentional", True)
        
        try:
            # Make a normal API call
            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # INTENTIONAL ERROR: Corrupt the JSON response
            content = response.choices[0].message.content
            
            # Add invalid JSON characters to cause parsing error
            corrupted_content = content.replace('"', "'").replace("{", "{{")
            
            span.set_attribute("response.corrupted", True)
            span.add_event("Intentionally corrupted JSON response for debugging exercise")
            
            return corrupted_content
            
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            raise

def recommend_hikes_with_error(location, difficulty, duration):
    """Recommend hiking trails - will fail due to JSON parsing error"""
    with tracer.start_as_current_span("recommend_hikes_with_error") as span:
        span.set_attribute("user.location", location)
        span.set_attribute("user.difficulty", difficulty)
        span.set_attribute("user.duration", duration)
        
        messages = [
            {"role": "system", "content": "You are a hiking expert. Recommend 3 hiking trails based on the user's preferences. Return as JSON array with fields: name, distance_km, elevation_gain_m, estimated_time_hours, difficulty, highlights"},
            {"role": "user", "content": f"Recommend 3 hiking trails near {location} with {difficulty} difficulty that take about {duration} hours."}
        ]
        
        # This will return corrupted JSON
        response = call_ai_model_with_error(messages, temperature=0.8)
        
        try:
            # This will fail due to corrupted JSON
            trails = json.loads(response)
            span.set_attribute("trails.count", len(trails))
            return trails
        except json.JSONDecodeError as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, f"JSON parsing failed: {str(e)}"))
            span.add_event("Failed to parse AI response as JSON", {"error": str(e), "response": response[:200]})
            
            print(f"\n❌ JSON Parsing Error Detected!")
            print(f"   Error: {e}")
            print(f"   Response preview: {response[:100]}...")
            print("\n📊 Check Application Insights to see the error trace!")
            raise

def main():
    """Main function to demonstrate error tracing"""
    with tracer.start_as_current_span("error_demo_main") as span:
        print("\n🔍 Hiking Assistant Error Tracing Demo 🔍\n")
        print("This demo intentionally causes an error to show tracing capabilities.\n")
        
        try:
            # This will fail and generate error traces
            trails = recommend_hikes_with_error("Seattle", "moderate", 3)
            print(f"Found {len(trails)} trails")
            
        except Exception as e:
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, str(e)))
            print(f"\n✅ Error successfully captured in traces!")
            print(f"   Navigate to Application Insights to inspect the error details.")

if __name__ == "__main__":
    main()