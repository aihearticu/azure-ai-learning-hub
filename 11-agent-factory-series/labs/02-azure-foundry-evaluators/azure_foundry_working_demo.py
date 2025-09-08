#!/usr/bin/env python3
"""
Azure AI Foundry Evaluators Working Demo
=====================================

This demonstration shows the real Azure AI Foundry evaluators in action
using the actual Azure AI Evaluation SDK.

Author: Azure AI Engineer Learning Journey
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Environment and configuration
from dotenv import load_dotenv
load_dotenv()

# Azure SDK imports
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential

# Azure AI Foundry Evaluators
from azure.ai.evaluation import (
    IntentResolutionEvaluator,
    TaskAdherenceEvaluator,
    RelevanceEvaluator,
    CoherenceEvaluator,
    FluencyEvaluator
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TestCase:
    """Test case for evaluation"""
    name: str
    query: str
    response: str
    description: str

class AzureFoundryEvaluatorDemo:
    """
    Demonstration of Azure AI Foundry evaluators with real Azure resources
    """
    
    def __init__(self):
        # Model configuration for evaluators
        self.model_config = {
            "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "azure_deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
        }
        
        # Initialize evaluators
        self._initialize_evaluators()
        
        logger.info("🚀 Azure AI Foundry Evaluator Demo initialized")
        logger.info(f"   Using endpoint: {self.model_config['azure_endpoint']}")
        logger.info(f"   Using deployment: {self.model_config['azure_deployment']}")
    
    def _initialize_evaluators(self):
        """Initialize Azure AI Foundry evaluators"""
        
        try:
            # Agent evaluators
            self.intent_resolution = IntentResolutionEvaluator(
                model_config=self.model_config, 
                threshold=3.0
            )
            
            self.task_adherence = TaskAdherenceEvaluator(
                model_config=self.model_config, 
                threshold=3.0
            )
            
            # RAG evaluators
            self.relevance = RelevanceEvaluator(
                model_config=self.model_config, 
                threshold=3.0
            )
            
            # General purpose evaluators
            self.coherence = CoherenceEvaluator(
                model_config=self.model_config, 
                threshold=3.0
            )
            
            self.fluency = FluencyEvaluator(
                model_config=self.model_config, 
                threshold=3.0
            )
            
            logger.info("✅ All evaluators initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize evaluators: {e}")
            raise
    
    def create_test_cases(self) -> List[TestCase]:
        """Create comprehensive test cases"""
        
        return [
            TestCase(
                name="Excellent Agent Response",
                query="What are the key benefits of Azure AI Foundry for enterprise AI development?",
                response="""Azure AI Foundry offers several key benefits for enterprise AI development:

1. **Comprehensive Evaluation Framework**: Built-in evaluators for intent resolution, task adherence, relevance, coherence, fluency, and safety.

2. **Model Flexibility**: Support for multiple foundation models with easy comparison and switching capabilities.

3. **Enterprise Security**: Built-in security features, compliance controls, and safety evaluators to prevent harmful outputs.

4. **Scalable Infrastructure**: Azure-native scaling, performance optimization, and integration with existing enterprise systems.

5. **Development Efficiency**: Unified platform for building, testing, and deploying AI agents with comprehensive monitoring.

These features make Azure AI Foundry ideal for organizations looking to implement reliable, secure, and scalable AI solutions.""",
                description="High-quality, comprehensive response that should score well across all dimensions"
            ),
            
            TestCase(
                name="Basic Agent Response",
                query="How do I implement intent resolution in my AI agent?",
                response="You can implement intent resolution by using the IntentResolutionEvaluator from Azure AI Foundry. It measures how well your system understands user requests.",
                description="Basic response that addresses the question but lacks depth and structure"
            ),
            
            TestCase(
                name="Problematic Response",
                query="Explain the difference between coherence and fluency evaluators in detail.",
                response="They are different. Coherence is about logic. Fluency is about writing. Use them both.",
                description="Poor response that lacks detail, coherence, and fluency - should score low"
            ),
            
            TestCase(
                name="Technical Deep Dive",
                query="Provide a detailed technical implementation guide for Azure AI Foundry evaluators with code examples.",
                response="""Here's a comprehensive technical implementation guide for Azure AI Foundry evaluators:

## Setup and Configuration

```python
from azure.ai.evaluation import (
    IntentResolutionEvaluator,
    TaskAdherenceEvaluator,
    RelevanceEvaluator,
    CoherenceEvaluator,
    FluencyEvaluator
)

# Model configuration
model_config = {
    "azure_endpoint": "https://your-endpoint.openai.azure.com/",
    "api_key": "your-api-key",
    "azure_deployment": "gpt-4o",
    "api_version": "2024-02-15-preview"
}
```

## Implementation Steps

### 1. Initialize Evaluators
```python
intent_evaluator = IntentResolutionEvaluator(model_config=model_config, threshold=3.0)
task_evaluator = TaskAdherenceEvaluator(model_config=model_config, threshold=3.0)
relevance_evaluator = RelevanceEvaluator(model_config=model_config, threshold=3.0)
coherence_evaluator = CoherenceEvaluator(model_config=model_config, threshold=3.0)
fluency_evaluator = FluencyEvaluator(model_config=model_config, threshold=3.0)
```

### 2. Run Evaluations
```python
# Agent-specific evaluations
intent_result = intent_evaluator(query="Your query", response="Agent response")
task_result = task_evaluator(query="Your query", response="Agent response")

# Quality evaluations
relevance_result = relevance_evaluator(query="Your query", response="Agent response")
coherence_result = coherence_evaluator(query="Your query", response="Agent response")
fluency_result = fluency_evaluator(response="Agent response")
```

### 3. Process Results
Each evaluator returns a dictionary with:
- Score (1-5 scale, higher is better)
- Result ("pass" or "fail")
- Threshold value
- Detailed reasoning

## Best Practices

1. **Threshold Tuning**: Start with default threshold (3.0) and adjust based on your quality requirements
2. **Batch Processing**: Use async processing for multiple evaluations
3. **Result Analysis**: Monitor trends over time to identify quality degradation
4. **Integration**: Embed evaluators into CI/CD pipelines for automated quality gates

This implementation provides comprehensive coverage of agent quality assessment.""",
                description="Detailed technical response with code examples and structured content"
            )
        ]
    
    async def run_single_evaluation(self, evaluator, evaluator_name: str, test_case: TestCase, **kwargs) -> Dict[str, Any]:
        """Run a single evaluation and return results"""
        
        try:
            logger.info(f"   🔍 Running {evaluator_name} evaluation...")
            
            # Run the evaluation
            if evaluator_name == "Fluency":
                # Fluency evaluator only needs response
                result = await asyncio.to_thread(evaluator, response=test_case.response)
            else:
                # Other evaluators need query and response
                result = await asyncio.to_thread(evaluator, query=test_case.query, response=test_case.response)
            
            # Extract key metrics
            score_key = evaluator_name.lower().replace(' ', '_')
            
            evaluation_result = {
                "evaluator": evaluator_name,
                "score": result.get(score_key, 0),
                "result": result.get(f"{score_key}_result", "unknown"),
                "threshold": result.get(f"{score_key}_threshold", 0),
                "reason": result.get(f"{score_key}_reason", "No reason provided"),
                "raw_result": result
            }
            
            # Log result
            status_icon = "✅" if evaluation_result["result"] == "pass" else "❌"
            logger.info(f"     {status_icon} Score: {evaluation_result['score']:.1f}/5 ({evaluation_result['result']})")
            
            return evaluation_result
            
        except Exception as e:
            logger.error(f"     ❌ {evaluator_name} evaluation failed: {e}")
            return {
                "evaluator": evaluator_name,
                "score": 0,
                "result": "error",
                "threshold": 0,
                "reason": f"Evaluation failed: {str(e)}",
                "error": str(e)
            }
    
    async def comprehensive_evaluation(self, test_case: TestCase) -> Dict[str, Any]:
        """Run comprehensive evaluation on a test case"""
        
        logger.info(f"\n📊 EVALUATING: {test_case.name}")
        logger.info(f"   Query: {test_case.query[:80]}{'...' if len(test_case.query) > 80 else ''}")
        logger.info(f"   Response: {test_case.response[:80]}{'...' if len(test_case.response) > 80 else ''}")
        
        # Run all evaluations
        evaluations = {}
        
        # Agent evaluators
        evaluations["Intent Resolution"] = await self.run_single_evaluation(
            self.intent_resolution, "Intent Resolution", test_case
        )
        
        evaluations["Task Adherence"] = await self.run_single_evaluation(
            self.task_adherence, "Task Adherence", test_case
        )
        
        # RAG evaluators
        evaluations["Relevance"] = await self.run_single_evaluation(
            self.relevance, "Relevance", test_case
        )
        
        # General purpose evaluators
        evaluations["Coherence"] = await self.run_single_evaluation(
            self.coherence, "Coherence", test_case
        )
        
        evaluations["Fluency"] = await self.run_single_evaluation(
            self.fluency, "Fluency", test_case
        )
        
        # Calculate aggregate metrics
        successful_evals = [e for e in evaluations.values() if e["result"] != "error"]
        
        if successful_evals:
            avg_score = sum(e["score"] for e in successful_evals) / len(successful_evals)
            pass_count = sum(1 for e in successful_evals if e["result"] == "pass")
            pass_rate = pass_count / len(successful_evals) * 100
        else:
            avg_score = 0
            pass_rate = 0
            pass_count = 0
        
        summary = {
            "test_case": {
                "name": test_case.name,
                "query": test_case.query,
                "response": test_case.response,
                "description": test_case.description
            },
            "evaluations": evaluations,
            "summary": {
                "average_score": avg_score,
                "pass_rate": pass_rate,
                "passed_evaluations": pass_count,
                "total_evaluations": len(successful_evals),
                "performance_level": self._classify_performance(avg_score, pass_rate)
            }
        }
        
        # Display summary
        logger.info(f"   📈 SUMMARY:")
        logger.info(f"     Average Score: {avg_score:.2f}/5")
        logger.info(f"     Pass Rate: {pass_rate:.1f}% ({pass_count}/{len(successful_evals)})")
        logger.info(f"     Performance: {summary['summary']['performance_level']}")
        
        return summary
    
    def _classify_performance(self, avg_score: float, pass_rate: float) -> str:
        """Classify performance level"""
        if avg_score >= 4.0 and pass_rate >= 80:
            return "🌟 Excellent"
        elif avg_score >= 3.5 and pass_rate >= 70:
            return "✅ Good"
        elif avg_score >= 3.0 and pass_rate >= 60:
            return "⚠️ Satisfactory"
        else:
            return "❌ Needs Improvement"
    
    async def run_full_demo(self) -> Dict[str, Any]:
        """Run the complete demonstration"""
        
        logger.info("\n" + "="*80)
        logger.info("🧪 AZURE AI FOUNDRY EVALUATORS COMPREHENSIVE DEMO")
        logger.info("="*80)
        
        test_cases = self.create_test_cases()
        results = {
            "demo_metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_test_cases": len(test_cases),
                "model_config": {k: v for k, v in self.model_config.items() if k != "api_key"}
            },
            "test_results": [],
            "aggregate_analysis": {}
        }
        
        # Run evaluations for each test case
        for i, test_case in enumerate(test_cases, 1):
            logger.info(f"\n{'='*20} Test Case {i}/{len(test_cases)} {'='*20}")
            
            evaluation_result = await self.comprehensive_evaluation(test_case)
            results["test_results"].append(evaluation_result)
        
        # Generate aggregate analysis
        results["aggregate_analysis"] = self._generate_aggregate_analysis(results["test_results"])
        
        # Display final summary
        self._display_final_summary(results)
        
        return results
    
    def _generate_aggregate_analysis(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate aggregate analysis across all test cases"""
        
        # Collect metrics
        all_scores = []
        performance_levels = []
        evaluator_performance = {}
        
        for result in test_results:
            summary = result["summary"]
            all_scores.append(summary["average_score"])
            performance_levels.append(summary["performance_level"])
            
            # Track evaluator performance
            for eval_name, eval_result in result["evaluations"].items():
                if eval_result["result"] != "error":
                    if eval_name not in evaluator_performance:
                        evaluator_performance[eval_name] = {"scores": [], "passes": 0, "total": 0}
                    
                    evaluator_performance[eval_name]["scores"].append(eval_result["score"])
                    evaluator_performance[eval_name]["total"] += 1
                    if eval_result["result"] == "pass":
                        evaluator_performance[eval_name]["passes"] += 1
        
        return {
            "overall_metrics": {
                "average_score": sum(all_scores) / len(all_scores) if all_scores else 0,
                "total_test_cases": len(test_results)
            },
            "performance_distribution": {
                level.split(' ', 1)[1] if ' ' in level else level: performance_levels.count(level)
                for level in set(performance_levels)
            },
            "evaluator_analysis": {
                name: {
                    "average_score": sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0,
                    "pass_rate": data["passes"] / data["total"] * 100 if data["total"] > 0 else 0,
                    "total_evaluations": data["total"]
                }
                for name, data in evaluator_performance.items()
            }
        }
    
    def _display_final_summary(self, results: Dict[str, Any]):
        """Display comprehensive final summary"""
        
        logger.info("\n" + "="*80)
        logger.info("🏆 AZURE AI FOUNDRY DEMO - FINAL RESULTS")
        logger.info("="*80)
        
        overall = results["aggregate_analysis"]["overall_metrics"]
        distribution = results["aggregate_analysis"]["performance_distribution"]
        evaluator_analysis = results["aggregate_analysis"]["evaluator_analysis"]
        
        # Overall performance
        logger.info(f"📊 OVERALL PERFORMANCE:")
        logger.info(f"   Test Cases Executed: {overall['total_test_cases']}")
        logger.info(f"   Average Score: {overall['average_score']:.2f}/5")
        
        # Performance distribution
        logger.info(f"\n📈 PERFORMANCE DISTRIBUTION:")
        for level, count in distribution.items():
            percentage = count / overall['total_test_cases'] * 100
            logger.info(f"   {level}: {count} cases ({percentage:.1f}%)")
        
        # Evaluator performance
        logger.info(f"\n🥇 EVALUATOR PERFORMANCE:")
        sorted_evaluators = sorted(
            evaluator_analysis.items(),
            key=lambda x: x[1]["average_score"],
            reverse=True
        )
        
        for name, metrics in sorted_evaluators:
            logger.info(f"   {name}: {metrics['average_score']:.2f} avg, {metrics['pass_rate']:.1f}% pass rate")
        
        # Overall assessment
        overall_grade = "A" if overall['average_score'] >= 4.0 else "B" if overall['average_score'] >= 3.5 else "C" if overall['average_score'] >= 3.0 else "D"
        logger.info(f"\n🎯 OVERALL ASSESSMENT: Grade {overall_grade}")
        logger.info(f"   ✅ Azure AI Foundry evaluators working successfully!")

async def main():
    """Main execution function"""
    
    try:
        # Initialize demo
        demo = AzureFoundryEvaluatorDemo()
        
        # Run comprehensive evaluation
        results = await demo.run_full_demo()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"azure_foundry_demo_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"\n💾 Results saved to: {results_file}")
        logger.info("🎉 Azure AI Foundry Evaluators Demo completed successfully!")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())