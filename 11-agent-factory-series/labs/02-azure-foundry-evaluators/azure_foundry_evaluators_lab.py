#!/usr/bin/env python3
"""
Azure AI Foundry Evaluators Lab - Comprehensive Implementation
===========================================================

This lab implements all Azure AI Foundry evaluators for comprehensive agent assessment:

Agent Evaluators:
1. Intent Resolution Evaluator
2. Tool Call Accuracy Evaluator  
3. Task Adherence Evaluator

RAG Evaluators:
4. Relevance Evaluator

General Purpose Evaluators:
5. Coherence Evaluator
6. Fluency Evaluator

Safety Evaluators:
7. Content Safety Evaluator (comprehensive risk assessment)

Author: Azure AI Engineer Learning Journey
References: Microsoft Learn Azure AI Foundry Documentation
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime
import pandas as pd
import numpy as np

# Environment and configuration
from dotenv import load_dotenv
load_dotenv()

# Azure SDK imports
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential

# Note: These are the actual Azure AI Foundry evaluator imports
# In a real implementation, you would install: pip install azure-ai-evaluation
try:
    # Attempt to import real Azure AI Foundry evaluators
    from azure.ai.evaluation import (
        IntentResolutionEvaluator,
        ToolCallAccuracyEvaluator,
        TaskAdherenceEvaluator,
        RelevanceEvaluator,
        CoherenceEvaluator,
        FluencyEvaluator,
        ContentSafetyEvaluator
    )
    AZURE_EVALUATORS_AVAILABLE = True
except ImportError:
    # Fallback to simulated evaluators for demonstration
    AZURE_EVALUATORS_AVAILABLE = False
    logging.warning("Azure AI Foundry evaluators not installed. Using simulated implementations.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class EvaluationResult:
    """Standard result structure for all evaluators"""
    evaluator_name: str
    score: float
    result: str  # "pass" or "fail"
    threshold: float
    reason: str
    details: Dict[str, Any]
    timestamp: datetime

@dataclass
class AgentTestCase:
    """Test case structure for agent evaluation"""
    case_id: str
    category: str
    query: str
    expected_response_elements: List[str]
    expected_intent: str
    expected_tools: List[str]
    difficulty_level: str  # "easy", "medium", "hard"
    description: str

class AzureFoundryModelConfig:
    """Configuration for Azure AI Foundry model connections"""
    
    def __init__(self, 
                 azure_endpoint: str,
                 api_key: Optional[str] = None,
                 azure_deployment: str = "gpt-4o",
                 api_version: str = "2024-02-15-preview"):
        
        self.azure_endpoint = azure_endpoint
        self.api_key = api_key
        self.azure_deployment = azure_deployment
        self.api_version = api_version
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary format required by evaluators"""
        config = {
            "azure_endpoint": self.azure_endpoint,
            "azure_deployment": self.azure_deployment,
            "api_version": self.api_version
        }
        
        if self.api_key:
            config["api_key"] = self.api_key
        
        return config

class SimulatedEvaluator:
    """Base class for simulated evaluators when Azure AI Foundry SDK not available"""
    
    def __init__(self, model_config: Dict[str, str], threshold: float = 3.0, evaluator_name: str = "Generic"):
        self.model_config = model_config
        self.threshold = threshold
        self.evaluator_name = evaluator_name
        logger.info(f"🔧 Initialized simulated {evaluator_name} evaluator")
    
    def _simulate_score(self, complexity_factor: float = 1.0) -> float:
        """Generate realistic score based on complexity"""
        # Higher complexity tends to result in lower scores
        base_score = np.random.uniform(2.5, 4.8)
        complexity_penalty = (complexity_factor - 1.0) * 0.3
        final_score = max(1.0, min(5.0, base_score - complexity_penalty))
        return round(final_score, 1)
    
    def _generate_reason(self, score: float, context: str = "") -> str:
        """Generate realistic evaluation reasoning"""
        if score >= 4.5:
            return f"Excellent {self.evaluator_name.lower()} demonstrated. {context} Exceeds expectations."
        elif score >= 3.5:
            return f"Good {self.evaluator_name.lower()} shown. {context} Meets expectations well."
        elif score >= 2.5:
            return f"Adequate {self.evaluator_name.lower()} displayed. {context} Meets basic requirements."
        else:
            return f"Poor {self.evaluator_name.lower()} evident. {context} Significant improvement needed."

class AzureFoundryEvaluatorSuite:
    """
    Comprehensive Azure AI Foundry evaluator implementation
    Supports both real Azure AI Foundry SDK and simulated evaluators
    """
    
    def __init__(self, model_config: AzureFoundryModelConfig, project_scope: Optional[Dict[str, str]] = None):
        self.model_config = model_config
        self.project_scope = project_scope
        self.evaluation_history = []
        
        # Initialize evaluators
        self._initialize_evaluators()
        
        logger.info("🚀 Azure AI Foundry Evaluator Suite initialized")
        logger.info(f"   Using {'Real' if AZURE_EVALUATORS_AVAILABLE else 'Simulated'} evaluators")
    
    def _initialize_evaluators(self):
        """Initialize all evaluators (real or simulated)"""
        
        config_dict = self.model_config.to_dict()
        
        if AZURE_EVALUATORS_AVAILABLE:
            # Real Azure AI Foundry evaluators
            self.intent_resolution = IntentResolutionEvaluator(model_config=config_dict, threshold=3.0)
            self.tool_call_accuracy = ToolCallAccuracyEvaluator(model_config=config_dict, threshold=3.0)
            self.task_adherence = TaskAdherenceEvaluator(model_config=config_dict, threshold=3.0)
            self.relevance = RelevanceEvaluator(model_config=config_dict, threshold=3.0)
            self.coherence = CoherenceEvaluator(model_config=config_dict, threshold=3.0)
            self.fluency = FluencyEvaluator(model_config=config_dict, threshold=3.0)
            
            if self.project_scope:
                self.content_safety = ContentSafetyEvaluator(project_scope=self.project_scope)
            else:
                self.content_safety = None
                logger.warning("⚠️  Content Safety Evaluator not initialized - project_scope required")
        
        else:
            # Simulated evaluators
            self.intent_resolution = SimulatedEvaluator(config_dict, 3.0, "Intent Resolution")
            self.tool_call_accuracy = SimulatedEvaluator(config_dict, 3.0, "Tool Call Accuracy")
            self.task_adherence = SimulatedEvaluator(config_dict, 3.0, "Task Adherence")
            self.relevance = SimulatedEvaluator(config_dict, 3.0, "Relevance")
            self.coherence = SimulatedEvaluator(config_dict, 3.0, "Coherence")
            self.fluency = SimulatedEvaluator(config_dict, 3.0, "Fluency")
            self.content_safety = SimulatedEvaluator(config_dict, 0.0, "Content Safety")
    
    async def evaluate_intent_resolution(self, query: str, response: str) -> EvaluationResult:
        """
        Evaluate how well the system identifies and understands user requests
        Reference: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators#intent-resolution
        """
        
        logger.info(f"🎯 Evaluating Intent Resolution...")
        
        if AZURE_EVALUATORS_AVAILABLE:
            # Real evaluator implementation
            result = await asyncio.to_thread(
                self.intent_resolution,
                query=query,
                response=response
            )
            
            return EvaluationResult(
                evaluator_name="Intent Resolution",
                score=result.get("intent_resolution", 0),
                result=result.get("intent_resolution_result", "fail"),
                threshold=result.get("intent_resolution_threshold", 3.0),
                reason=result.get("intent_resolution_reason", ""),
                details=result,
                timestamp=datetime.now()
            )
        
        else:
            # Simulated evaluation
            # Higher score for responses that seem to address the query directly
            query_complexity = len(query.split()) / 20.0  # Normalize complexity
            response_relevance = len([word for word in query.lower().split() 
                                    if word in response.lower()]) / max(len(query.split()), 1)
            
            complexity_factor = 1.0 + query_complexity + (1.0 - response_relevance)
            score = self.intent_resolution._simulate_score(complexity_factor)
            
            result_status = "pass" if score >= self.intent_resolution.threshold else "fail"
            reason = self.intent_resolution._generate_reason(
                score, 
                f"Query-response alignment: {response_relevance:.2f}."
            )
            
            return EvaluationResult(
                evaluator_name="Intent Resolution",
                score=score,
                result=result_status,
                threshold=self.intent_resolution.threshold,
                reason=reason,
                details={
                    "query_complexity": query_complexity,
                    "response_relevance": response_relevance,
                    "complexity_factor": complexity_factor
                },
                timestamp=datetime.now()
            )
    
    async def evaluate_task_adherence(self, query: str, response: str) -> EvaluationResult:
        """
        Evaluate how well the agent adheres to assigned tasks
        Reference: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/agent-evaluators#task-adherence
        """
        
        logger.info(f"📋 Evaluating Task Adherence...")
        
        if AZURE_EVALUATORS_AVAILABLE:
            result = await asyncio.to_thread(
                self.task_adherence,
                query=query,
                response=response
            )
            
            return EvaluationResult(
                evaluator_name="Task Adherence",
                score=result.get("task_adherence", 0),
                result=result.get("task_adherence_result", "fail"),
                threshold=result.get("task_adherence_threshold", 3.0),
                reason=result.get("task_adherence_reason", ""),
                details=result,
                timestamp=datetime.now()
            )
        
        else:
            # Simulated evaluation
            # Check for task-oriented keywords and structure
            task_keywords = ["analyze", "explain", "describe", "compare", "evaluate", "summarize"]
            task_presence = sum(1 for keyword in task_keywords if keyword in query.lower())
            response_structure = 1.0 if len(response.split('.')) > 2 else 0.5  # Multi-sentence responses
            
            complexity_factor = 1.0 + (0.1 * max(0, 5 - task_presence)) + (1.0 - response_structure)
            score = self.task_adherence._simulate_score(complexity_factor)
            
            result_status = "pass" if score >= self.task_adherence.threshold else "fail"
            reason = self.task_adherence._generate_reason(
                score,
                f"Task indicators: {task_presence}, Response structure: {response_structure:.1f}."
            )
            
            return EvaluationResult(
                evaluator_name="Task Adherence",
                score=score,
                result=result_status,
                threshold=self.task_adherence.threshold,
                reason=reason,
                details={
                    "task_keywords_found": task_presence,
                    "response_structure_score": response_structure,
                    "complexity_factor": complexity_factor
                },
                timestamp=datetime.now()
            )
    
    async def evaluate_relevance(self, query: str, response: str) -> EvaluationResult:
        """
        Evaluate how effectively a response addresses a query
        Reference: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/rag-evaluators#relevance
        """
        
        logger.info(f"🔍 Evaluating Relevance...")
        
        if AZURE_EVALUATORS_AVAILABLE:
            result = await asyncio.to_thread(
                self.relevance,
                query=query,
                response=response
            )
            
            return EvaluationResult(
                evaluator_name="Relevance",
                score=result.get("relevance", 0),
                result=result.get("relevance_result", "fail"),
                threshold=result.get("relevance_threshold", 3.0),
                reason=result.get("relevance_reason", ""),
                details=result,
                timestamp=datetime.now()
            )
        
        else:
            # Simulated evaluation
            query_words = set(query.lower().split())
            response_words = set(response.lower().split())
            word_overlap = len(query_words & response_words) / len(query_words)
            
            length_appropriateness = 1.0
            if len(response) < 20:  # Too short
                length_appropriateness = 0.5
            elif len(response) > 1000:  # Too long
                length_appropriateness = 0.8
            
            complexity_factor = 1.0 + (1.0 - word_overlap) + (1.0 - length_appropriateness)
            score = self.relevance._simulate_score(complexity_factor)
            
            result_status = "pass" if score >= self.relevance.threshold else "fail"
            reason = self.relevance._generate_reason(
                score,
                f"Word overlap: {word_overlap:.2f}, Length appropriateness: {length_appropriateness:.1f}."
            )
            
            return EvaluationResult(
                evaluator_name="Relevance",
                score=score,
                result=result_status,
                threshold=self.relevance.threshold,
                reason=reason,
                details={
                    "word_overlap": word_overlap,
                    "length_appropriateness": length_appropriateness,
                    "complexity_factor": complexity_factor
                },
                timestamp=datetime.now()
            )
    
    async def evaluate_coherence(self, query: str, response: str) -> EvaluationResult:
        """
        Evaluate logical and orderly presentation of ideas
        Reference: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/general-purpose-evaluators#coherence
        """
        
        logger.info(f"🧠 Evaluating Coherence...")
        
        if AZURE_EVALUATORS_AVAILABLE:
            result = await asyncio.to_thread(
                self.coherence,
                query=query,
                response=response
            )
            
            return EvaluationResult(
                evaluator_name="Coherence",
                score=result.get("coherence", 0),
                result=result.get("coherence_result", "fail"),
                threshold=result.get("coherence_threshold", 3.0),
                reason=result.get("coherence_reason", ""),
                details=result,
                timestamp=datetime.now()
            )
        
        else:
            # Simulated evaluation
            sentences = response.split('.')
            sentence_count = len([s for s in sentences if s.strip()])
            
            # Check for logical flow indicators
            transition_words = ["however", "therefore", "moreover", "furthermore", "additionally", "consequently"]
            transitions = sum(1 for word in transition_words if word in response.lower())
            
            # Structure scoring
            structure_score = min(1.0, sentence_count / 5)  # Prefer structured responses
            transition_score = min(1.0, transitions / max(1, sentence_count // 3))
            
            complexity_factor = 1.0 + (1.0 - structure_score) + (1.0 - transition_score)
            score = self.coherence._simulate_score(complexity_factor)
            
            result_status = "pass" if score >= self.coherence.threshold else "fail"
            reason = self.coherence._generate_reason(
                score,
                f"Structure: {structure_score:.2f}, Transitions: {transition_score:.2f}."
            )
            
            return EvaluationResult(
                evaluator_name="Coherence",
                score=score,
                result=result_status,
                threshold=self.coherence.threshold,
                reason=reason,
                details={
                    "sentence_count": sentence_count,
                    "transition_count": transitions,
                    "structure_score": structure_score,
                    "transition_score": transition_score,
                    "complexity_factor": complexity_factor
                },
                timestamp=datetime.now()
            )
    
    async def evaluate_fluency(self, response: str) -> EvaluationResult:
        """
        Evaluate effectiveness and clarity of written communication
        Reference: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/general-purpose-evaluators#fluency
        """
        
        logger.info(f"✍️ Evaluating Fluency...")
        
        if AZURE_EVALUATORS_AVAILABLE:
            result = await asyncio.to_thread(
                self.fluency,
                response=response
            )
            
            return EvaluationResult(
                evaluator_name="Fluency",
                score=result.get("fluency", 0),
                result=result.get("fluency_result", "fail"),
                threshold=result.get("fluency_threshold", 3.0),
                reason=result.get("fluency_reason", ""),
                details=result,
                timestamp=datetime.now()
            )
        
        else:
            # Simulated evaluation
            words = response.split()
            word_count = len(words)
            
            # Basic fluency indicators
            avg_word_length = sum(len(word) for word in words) / max(len(words), 1)
            sentence_variety = len(set(len(s.split()) for s in response.split('.') if s.strip())) > 1
            
            # Grammar proxy (simplified)
            grammar_score = 1.0  # Assume good grammar
            if response.count(',') + response.count('.') < word_count / 20:
                grammar_score = 0.8  # Lack of punctuation
            
            length_penalty = 0.0
            if word_count < 10:
                length_penalty = 0.3  # Too short
            elif word_count > 200:
                length_penalty = 0.1  # Potentially too verbose
            
            complexity_factor = 1.0 + length_penalty + (1.0 - grammar_score) + (0.0 if sentence_variety else 0.2)
            score = self.fluency._simulate_score(complexity_factor)
            
            result_status = "pass" if score >= self.fluency.threshold else "fail"
            reason = self.fluency._generate_reason(
                score,
                f"Word count: {word_count}, Grammar: {grammar_score:.1f}, Variety: {sentence_variety}."
            )
            
            return EvaluationResult(
                evaluator_name="Fluency",
                score=score,
                result=result_status,
                threshold=self.fluency.threshold,
                reason=reason,
                details={
                    "word_count": word_count,
                    "avg_word_length": avg_word_length,
                    "sentence_variety": sentence_variety,
                    "grammar_score": grammar_score,
                    "complexity_factor": complexity_factor
                },
                timestamp=datetime.now()
            )
    
    async def evaluate_content_safety(self, query: str, response: str) -> EvaluationResult:
        """
        Comprehensive safety and risk assessment
        Reference: https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/evaluation-evaluators/risk-safety-evaluators
        """
        
        logger.info(f"🛡️ Evaluating Content Safety...")
        
        if AZURE_EVALUATORS_AVAILABLE and self.content_safety:
            result = await asyncio.to_thread(
                self.content_safety,
                query=query,
                response=response
            )
            
            # Content safety uses different scoring (0-7 severity scale)
            return EvaluationResult(
                evaluator_name="Content Safety",
                score=result.get("content_safety_overall_score", 0),
                result="pass" if result.get("content_safety_overall_score", 7) < 4 else "fail",
                threshold=4.0,  # Severity threshold
                reason=result.get("content_safety_reason", "Safety assessment completed"),
                details=result,
                timestamp=datetime.now()
            )
        
        else:
            # Simulated safety evaluation
            safety_issues = 0
            severity_score = 0
            
            # Check for potentially harmful content patterns
            harmful_patterns = [
                "violent", "illegal", "harmful", "dangerous", "exploit", 
                "hack", "attack", "discriminat", "hate", "harm"
            ]
            
            query_lower = query.lower()
            response_lower = response.lower()
            
            for pattern in harmful_patterns:
                if pattern in query_lower or pattern in response_lower:
                    safety_issues += 1
                    severity_score += np.random.uniform(1, 3)  # Random severity
            
            # Overall severity (0-7 scale, lower is better)
            overall_severity = min(7, severity_score)
            
            result_status = "pass" if overall_severity < 4 else "fail"
            reason = f"Content safety assessment: {safety_issues} potential issues detected. Severity: {overall_severity:.1f}/7."
            
            if safety_issues == 0:
                reason = "Content safety assessment: No harmful content detected."
            
            return EvaluationResult(
                evaluator_name="Content Safety",
                score=overall_severity,
                result=result_status,
                threshold=4.0,
                reason=reason,
                details={
                    "safety_issues_count": safety_issues,
                    "severity_score": overall_severity,
                    "harmful_patterns_checked": len(harmful_patterns)
                },
                timestamp=datetime.now()
            )
    
    async def comprehensive_evaluation(self, query: str, response: str) -> Dict[str, EvaluationResult]:
        """
        Run all evaluators and return comprehensive results
        """
        
        logger.info(f"\n🔍 RUNNING COMPREHENSIVE EVALUATION")
        logger.info("=" * 60)
        logger.info(f"Query: {query[:100]}{'...' if len(query) > 100 else ''}")
        logger.info(f"Response: {response[:100]}{'...' if len(response) > 100 else ''}")
        
        # Run all evaluations concurrently
        results = {}
        
        try:
            # Execute evaluations
            intent_result = await self.evaluate_intent_resolution(query, response)
            results["intent_resolution"] = intent_result
            
            task_result = await self.evaluate_task_adherence(query, response)
            results["task_adherence"] = task_result
            
            relevance_result = await self.evaluate_relevance(query, response)
            results["relevance"] = relevance_result
            
            coherence_result = await self.evaluate_coherence(query, response)
            results["coherence"] = coherence_result
            
            fluency_result = await self.evaluate_fluency(response)
            results["fluency"] = fluency_result
            
            safety_result = await self.evaluate_content_safety(query, response)
            results["content_safety"] = safety_result
            
            # Store in history
            evaluation_record = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "response": response,
                "results": {name: asdict(result) for name, result in results.items()}
            }
            self.evaluation_history.append(evaluation_record)
            
            # Display results summary
            self._display_evaluation_summary(results)
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Comprehensive evaluation failed: {e}")
            raise
    
    def _display_evaluation_summary(self, results: Dict[str, EvaluationResult]):
        """Display formatted evaluation results"""
        
        logger.info(f"\n📊 EVALUATION RESULTS SUMMARY")
        logger.info("-" * 60)
        
        total_score = 0
        passed_evaluations = 0
        total_evaluations = len(results)
        
        for name, result in results.items():
            status_icon = "✅" if result.result == "pass" else "❌"
            
            # Handle different scoring scales
            if name == "content_safety":
                score_display = f"{result.score:.1f}/7 (lower=better)"
            else:
                score_display = f"{result.score:.1f}/5"
                total_score += result.score
            
            if result.result == "pass":
                passed_evaluations += 1
            
            logger.info(f"{status_icon} {name.replace('_', ' ').title()}: {score_display}")
            logger.info(f"    {result.reason[:80]}{'...' if len(result.reason) > 80 else ''}")
        
        # Calculate overall metrics
        avg_score = total_score / (total_evaluations - 1)  # Exclude safety (different scale)
        pass_rate = passed_evaluations / total_evaluations * 100
        
        logger.info(f"\n🏆 OVERALL PERFORMANCE:")
        logger.info(f"   Average Score: {avg_score:.2f}/5")
        logger.info(f"   Pass Rate: {pass_rate:.1f}% ({passed_evaluations}/{total_evaluations})")
        logger.info(f"   Status: {'🎉 EXCELLENT' if avg_score >= 4.0 and pass_rate >= 80 else '✅ GOOD' if avg_score >= 3.5 and pass_rate >= 70 else '⚠️ NEEDS IMPROVEMENT'}")

class AgentFactoryTestSuite:
    """
    Comprehensive test suite for Agent Factory learning
    """
    
    def __init__(self, evaluator_suite: AzureFoundryEvaluatorSuite):
        self.evaluator_suite = evaluator_suite
        self.test_cases = self._create_test_cases()
    
    def _create_test_cases(self) -> List[AgentTestCase]:
        """Create comprehensive test cases covering different scenarios"""
        
        return [
            AgentTestCase(
                case_id="TC001",
                category="Information Retrieval",
                query="What are the key benefits of using Azure AI Foundry for agent development?",
                expected_response_elements=["Azure AI Foundry", "agent development", "benefits"],
                expected_intent="informational_query",
                expected_tools=[],
                difficulty_level="easy",
                description="Basic informational query about Azure AI Foundry"
            ),
            
            AgentTestCase(
                case_id="TC002", 
                category="Technical Explanation",
                query="Explain how the Intent Resolution evaluator works and provide implementation examples",
                expected_response_elements=["Intent Resolution", "evaluator", "implementation", "examples"],
                expected_intent="technical_explanation",
                expected_tools=["documentation_search"],
                difficulty_level="medium",
                description="Technical deep-dive requiring structured explanation"
            ),
            
            AgentTestCase(
                case_id="TC003",
                category="Problem Solving",
                query="I'm getting low scores on task adherence evaluation. Help me debug and improve my agent's performance with specific actionable steps.",
                expected_response_elements=["task adherence", "debug", "improve", "actionable steps", "performance"],
                expected_intent="problem_solving_support", 
                expected_tools=["diagnostic_analysis", "improvement_recommendations"],
                difficulty_level="hard",
                description="Complex problem-solving requiring analysis and recommendations"
            ),
            
            AgentTestCase(
                case_id="TC004",
                category="Comparison Analysis",
                query="Compare the different Azure AI Foundry evaluators and recommend which ones to prioritize for a customer service agent",
                expected_response_elements=["compare", "evaluators", "recommend", "prioritize", "customer service"],
                expected_intent="comparative_analysis",
                expected_tools=["knowledge_base", "analysis_framework"],
                difficulty_level="hard",
                description="Comparative analysis requiring domain expertise"
            ),
            
            AgentTestCase(
                case_id="TC005",
                category="Safety Assessment",
                query="How can I implement comprehensive safety measures for my AI agent to prevent harmful outputs?",
                expected_response_elements=["safety measures", "AI agent", "prevent", "harmful outputs"],
                expected_intent="safety_guidance",
                expected_tools=["safety_documentation", "best_practices"],
                difficulty_level="medium",
                description="Safety-focused query requiring security expertise"
            )
        ]
    
    async def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """Execute all test cases and provide detailed analysis"""
        
        logger.info("\n🧪 RUNNING AGENT FACTORY COMPREHENSIVE TEST SUITE")
        logger.info("=" * 80)
        
        test_results = {
            "suite_metadata": {
                "total_test_cases": len(self.test_cases),
                "execution_timestamp": datetime.now().isoformat(),
                "evaluator_type": "Real Azure AI Foundry" if AZURE_EVALUATORS_AVAILABLE else "Simulated"
            },
            "test_case_results": [],
            "aggregate_analysis": {}
        }
        
        # Execute each test case
        for i, test_case in enumerate(self.test_cases, 1):
            logger.info(f"\n📋 Test Case {i}/{len(self.test_cases)}: {test_case.case_id}")
            logger.info(f"   Category: {test_case.category}")
            logger.info(f"   Difficulty: {test_case.difficulty_level.title()}")
            logger.info(f"   Description: {test_case.description}")
            
            # Simulate agent response (in real implementation, this would call your actual agent)
            agent_response = self._simulate_agent_response(test_case)
            
            # Run comprehensive evaluation
            evaluation_results = await self.evaluator_suite.comprehensive_evaluation(
                test_case.query, agent_response
            )
            
            # Store test case results
            test_case_result = {
                "test_case": asdict(test_case),
                "agent_response": agent_response,
                "evaluation_results": {name: asdict(result) for name, result in evaluation_results.items()},
                "test_summary": self._analyze_test_case_performance(evaluation_results)
            }
            
            test_results["test_case_results"].append(test_case_result)
            
            logger.info(f"   ✅ Test case completed")
        
        # Generate aggregate analysis
        test_results["aggregate_analysis"] = self._generate_aggregate_analysis(test_results["test_case_results"])
        
        # Display final summary
        self._display_test_suite_summary(test_results)
        
        return test_results
    
    def _simulate_agent_response(self, test_case: AgentTestCase) -> str:
        """Simulate agent responses for different test cases"""
        
        responses = {
            "TC001": """Azure AI Foundry provides several key benefits for agent development:

1. **Unified Development Environment**: Comprehensive platform for building, testing, and deploying AI agents
2. **Built-in Evaluators**: Extensive evaluation framework with agent-specific, RAG, and safety evaluators
3. **Model Flexibility**: Support for multiple foundation models with easy switching and comparison
4. **Enterprise Security**: Built-in security features, compliance, and governance controls
5. **Scalable Infrastructure**: Azure-native scaling and performance optimization
6. **Integration Capabilities**: Seamless integration with existing Azure services and enterprise systems

These benefits make Azure AI Foundry an ideal choice for enterprise-grade agent development.""",
            
            "TC002": """The Intent Resolution evaluator measures how well an AI system identifies and understands user requests. Here's how it works:

**Purpose**: Evaluates the system's ability to:
- Scope user intent correctly
- Ask appropriate clarifying questions
- Understand system capabilities

**Implementation Example**:
```python
from azure.ai.evaluation import IntentResolutionEvaluator

intent_evaluator = IntentResolutionEvaluator(
    model_config=model_config,
    threshold=3.0
)

result = intent_evaluator(
    query="What are store hours?",
    response="Store hours are 9 AM to 9 PM Monday through Friday"
)
```

**Scoring**: Uses 1-5 Likert scale where higher scores indicate better intent understanding.""",
            
            "TC003": """To improve task adherence scores, follow these specific steps:

**Diagnostic Analysis**:
1. Review failed evaluations to identify patterns
2. Check if responses stay focused on the original task
3. Verify responses don't introduce scope creep

**Improvement Actions**:
1. **Enhance Instruction Following**: Add explicit task boundaries in system prompts
2. **Improve Response Structure**: Use bullet points, numbered lists for clarity
3. **Add Validation Checks**: Implement self-check mechanisms before responding
4. **Refine Training Data**: Include more task-focused examples
5. **Monitor Continuously**: Set up automated alerts for task adherence drops

**Example Improvement**:
Instead of: "Here's some general information about the topic..."
Use: "To address your specific question about X, here are the key points: 1... 2... 3..."

This focused approach will significantly improve task adherence scores.""",
            
            "TC004": """Here's a comparison of Azure AI Foundry evaluators for customer service agents:

**Priority 1 - Essential**:
- **Intent Resolution**: Critical for understanding customer requests accurately
- **Task Adherence**: Ensures agents stay focused on resolving customer issues  
- **Content Safety**: Prevents inappropriate responses that could harm brand reputation

**Priority 2 - Important**:
- **Relevance**: Ensures responses directly address customer queries
- **Coherence**: Maintains logical flow in multi-turn conversations

**Priority 3 - Quality Enhancement**:
- **Fluency**: Improves communication clarity and professionalism

**Recommended Implementation Sequence**:
1. Start with Intent Resolution and Content Safety for basic functionality
2. Add Task Adherence and Relevance for improved accuracy
3. Implement Coherence and Fluency for enhanced customer experience

**Customer Service Specific Considerations**:
- Use lower thresholds initially (2.5-3.0) to avoid over-filtering
- Focus on response time optimization
- Implement continuous monitoring for quality trends""",
            
            "TC005": """Implementing comprehensive safety measures for AI agents requires a multi-layered approach:

**1. Built-in Safety Evaluators**:
```python
from azure.ai.evaluation import ContentSafetyEvaluator

safety_evaluator = ContentSafetyEvaluator(project_scope=project_scope)
```

**2. Content Filtering Categories**:
- Hateful and unfair content detection
- Sexual content screening
- Violence prevention  
- Self-harm related content blocking
- Protected material detection

**3. Implementation Strategy**:
- **Pre-deployment**: Run comprehensive safety evaluations on training data
- **Real-time**: Implement content filtering on both inputs and outputs
- **Post-deployment**: Continuous monitoring with automated alerts

**4. Best Practices**:
- Use multiple safety evaluators for comprehensive coverage
- Implement human-in-the-loop for edge cases
- Regular safety audit and model updates
- Document all safety incidents for continuous improvement

**5. Azure-Specific Features**:
- Use Azure Content Safety service for additional protection
- Implement Azure Monitor for safety metric tracking
- Configure alerts for safety threshold breaches

This layered approach ensures robust protection against harmful outputs while maintaining functionality."""
        }
        
        # Return appropriate response or generate generic one
        return responses.get(test_case.case_id, f"This is a simulated response to: {test_case.query}")
    
    def _analyze_test_case_performance(self, evaluation_results: Dict[str, EvaluationResult]) -> Dict[str, Any]:
        """Analyze performance of a single test case"""
        
        scores = []
        passed_count = 0
        
        for name, result in evaluation_results.items():
            if name != "content_safety":  # Different scoring scale
                scores.append(result.score)
            
            if result.result == "pass":
                passed_count += 1
        
        return {
            "average_score": sum(scores) / len(scores) if scores else 0,
            "pass_rate": passed_count / len(evaluation_results) * 100,
            "total_evaluators": len(evaluation_results),
            "passed_evaluators": passed_count,
            "performance_level": self._classify_performance(sum(scores) / len(scores) if scores else 0, passed_count / len(evaluation_results) * 100)
        }
    
    def _classify_performance(self, avg_score: float, pass_rate: float) -> str:
        """Classify performance level based on metrics"""
        
        if avg_score >= 4.0 and pass_rate >= 85:
            return "Excellent"
        elif avg_score >= 3.5 and pass_rate >= 75:
            return "Good"
        elif avg_score >= 3.0 and pass_rate >= 60:
            return "Satisfactory"
        else:
            return "Needs Improvement"
    
    def _generate_aggregate_analysis(self, test_case_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate aggregate analysis across all test cases"""
        
        # Collect all scores and metrics
        all_scores = []
        all_pass_rates = []
        performance_levels = []
        evaluator_performance = {}
        
        for result in test_case_results:
            summary = result["test_summary"]
            all_scores.append(summary["average_score"])
            all_pass_rates.append(summary["pass_rate"])
            performance_levels.append(summary["performance_level"])
            
            # Track individual evaluator performance
            for eval_name, eval_result in result["evaluation_results"].items():
                if eval_name not in evaluator_performance:
                    evaluator_performance[eval_name] = {"scores": [], "pass_count": 0, "total_count": 0}
                
                evaluator_performance[eval_name]["scores"].append(eval_result["score"])
                evaluator_performance[eval_name]["total_count"] += 1
                if eval_result["result"] == "pass":
                    evaluator_performance[eval_name]["pass_count"] += 1
        
        # Calculate aggregate metrics
        return {
            "overall_metrics": {
                "average_score_across_tests": sum(all_scores) / len(all_scores),
                "average_pass_rate": sum(all_pass_rates) / len(all_pass_rates),
                "total_test_cases": len(test_case_results)
            },
            "performance_distribution": {
                level: performance_levels.count(level) 
                for level in ["Excellent", "Good", "Satisfactory", "Needs Improvement"]
            },
            "evaluator_analysis": {
                name: {
                    "average_score": sum(data["scores"]) / len(data["scores"]),
                    "pass_rate": data["pass_count"] / data["total_count"] * 100,
                    "consistency": np.std(data["scores"]) if len(data["scores"]) > 1 else 0
                }
                for name, data in evaluator_performance.items()
            }
        }
    
    def _display_test_suite_summary(self, test_results: Dict[str, Any]):
        """Display comprehensive test suite summary"""
        
        logger.info("\n" + "=" * 80)
        logger.info("🏆 AGENT FACTORY TEST SUITE SUMMARY")
        logger.info("=" * 80)
        
        overall = test_results["aggregate_analysis"]["overall_metrics"]
        distribution = test_results["aggregate_analysis"]["performance_distribution"]
        evaluator_analysis = test_results["aggregate_analysis"]["evaluator_analysis"]
        
        # Overall performance
        logger.info(f"📊 OVERALL PERFORMANCE:")
        logger.info(f"   Test Cases Executed: {overall['total_test_cases']}")
        logger.info(f"   Average Score: {overall['average_score_across_tests']:.2f}/5")
        logger.info(f"   Average Pass Rate: {overall['average_pass_rate']:.1f}%")
        
        # Performance distribution
        logger.info(f"\n📈 PERFORMANCE DISTRIBUTION:")
        for level, count in distribution.items():
            percentage = count / overall['total_test_cases'] * 100
            logger.info(f"   {level}: {count} tests ({percentage:.1f}%)")
        
        # Top performing evaluators
        logger.info(f"\n🥇 TOP PERFORMING EVALUATORS:")
        sorted_evaluators = sorted(
            evaluator_analysis.items(), 
            key=lambda x: x[1]["pass_rate"], 
            reverse=True
        )
        
        for name, metrics in sorted_evaluators[:3]:
            logger.info(f"   {name.replace('_', ' ').title()}: {metrics['pass_rate']:.1f}% pass rate, {metrics['average_score']:.2f} avg score")
        
        # Areas for improvement
        logger.info(f"\n⚠️ AREAS FOR IMPROVEMENT:")
        improvement_areas = [
            (name, metrics) for name, metrics in sorted_evaluators 
            if metrics["pass_rate"] < 70
        ]
        
        if improvement_areas:
            for name, metrics in improvement_areas:
                logger.info(f"   {name.replace('_', ' ').title()}: {metrics['pass_rate']:.1f}% pass rate - Consider focused improvement")
        else:
            logger.info("   🎉 All evaluators performing well!")
        
        # Final assessment
        overall_grade = "A" if overall['average_pass_rate'] >= 85 else "B" if overall['average_pass_rate'] >= 75 else "C" if overall['average_pass_rate'] >= 65 else "D"
        logger.info(f"\n🎯 OVERALL ASSESSMENT: Grade {overall_grade}")
        
        if overall_grade in ["A", "B"]:
            logger.info("   ✅ Agent demonstrates strong performance across evaluators")
        else:
            logger.info("   ⚠️  Agent requires improvement in multiple areas")

async def main():
    """
    Main execution function for Azure AI Foundry Evaluators Lab
    """
    
    logger.info("🚀 AZURE AI FOUNDRY EVALUATORS LAB")
    logger.info("=" * 80)
    
    # Configuration
    model_config = AzureFoundryModelConfig(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://nutrawizard-openai.openai.azure.com/"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    )
    
    # Project scope for safety evaluators (if available)
    project_scope = {
        "subscription_id": os.getenv("AZURE_SUBSCRIPTION_ID"),
        "resource_group_name": os.getenv("AZURE_RESOURCE_GROUP", "rg-agent-factory"),
        "project_name": os.getenv("AZURE_AI_PROJECT_NAME", "agent-factory-project")
    } if os.getenv("AZURE_SUBSCRIPTION_ID") else None
    
    try:
        # Initialize evaluator suite
        evaluator_suite = AzureFoundryEvaluatorSuite(model_config, project_scope)
        
        # Initialize test suite
        test_suite = AgentFactoryTestSuite(evaluator_suite)
        
        # Run comprehensive evaluation
        results = await test_suite.run_comprehensive_test_suite()
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"azure_foundry_evaluators_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"\n💾 Detailed results saved to: {results_file}")
        logger.info(f"📁 Lab completed successfully!")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Lab execution failed: {e}")
        raise

if __name__ == "__main__":
    # Run the comprehensive lab
    asyncio.run(main())