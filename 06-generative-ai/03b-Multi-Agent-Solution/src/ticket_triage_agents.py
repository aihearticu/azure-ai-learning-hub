import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

# Load environment variables
load_dotenv()

@dataclass
class TicketAssessment:
    """Data class for ticket assessment results."""
    priority: str
    priority_score: int
    priority_reasoning: str
    assigned_team: str
    team_reasoning: str
    estimated_effort: str
    effort_hours: int
    effort_reasoning: str
    summary: str

class SpecializedAgent:
    """Base class for specialized agents."""
    
    def __init__(self, name: str, description: str, instructions: str):
        self.name = name
        self.description = description
        self.instructions = instructions
        self.client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2024-02-15-preview"
        )
        self.deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
    
    def analyze(self, ticket_description: str, context: Dict = None) -> Dict:
        """Analyze the ticket based on agent's specialty."""
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": f"Analyze this ticket: {ticket_description}"}
        ]
        
        if context:
            messages.append({"role": "user", "content": f"Additional context: {json.dumps(context)}"})
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        
        return {
            "agent": self.name,
            "analysis": response.choices[0].message.content
        }

class PriorityAssessmentAgent(SpecializedAgent):
    """Agent specialized in assessing ticket priority."""
    
    def __init__(self):
        instructions = """You are a Priority Assessment Agent. Your role is to evaluate support tickets and determine their priority level.

Priority Levels:
- P1 (Critical): System down, major functionality broken, affecting many users
- P2 (High): Significant issues, workarounds exist, affecting multiple users
- P3 (Medium): Moderate issues, limited user impact
- P4 (Low): Minor issues, cosmetic problems, single user affected

Analyze the ticket and provide:
1. Priority level (P1-P4)
2. Priority score (1-10, where 10 is most critical)
3. Clear reasoning for the priority assignment

Format your response as:
Priority: [P1-P4]
Score: [1-10]
Reasoning: [Your detailed reasoning]"""
        
        super().__init__(
            name="Priority Assessment Agent",
            description="Assess the priority of support tickets",
            instructions=instructions
        )

class TeamAssignmentAgent(SpecializedAgent):
    """Agent specialized in team assignment."""
    
    def __init__(self):
        instructions = """You are a Team Assignment Agent. Your role is to determine which team should handle a support ticket.

Available Teams:
- Infrastructure Team: Server, network, hardware, system performance issues
- Application Team: Software bugs, feature requests, UI/UX issues
- Security Team: Access issues, security concerns, authentication problems
- Database Team: Data issues, query performance, backup/restore
- Customer Success: User training, documentation, general inquiries

Analyze the ticket and provide:
1. Recommended team assignment
2. Clear reasoning for the assignment
3. Any secondary teams that might need to be involved

Format your response as:
Team: [Primary team name]
Secondary Teams: [Any additional teams, or "None"]
Reasoning: [Your detailed reasoning]"""
        
        super().__init__(
            name="Team Assignment Agent",
            description="Determine which team should handle the ticket",
            instructions=instructions
        )

class EffortEstimationAgent(SpecializedAgent):
    """Agent specialized in effort estimation."""
    
    def __init__(self):
        instructions = """You are an Effort Estimation Agent. Your role is to estimate the effort required to resolve support tickets.

Effort Categories:
- Quick Fix: Less than 2 hours
- Small: 2-8 hours (1 day)
- Medium: 8-24 hours (1-3 days)
- Large: 24-80 hours (3-10 days)
- Extra Large: More than 80 hours (2+ weeks)

Consider factors like:
- Technical complexity
- Required research/investigation
- Testing requirements
- Documentation needs
- Potential blockers

Analyze the ticket and provide:
1. Effort category
2. Estimated hours
3. Key factors affecting the estimate

Format your response as:
Effort: [Category]
Hours: [Numeric estimate]
Factors: [Key factors considered]"""
        
        super().__init__(
            name="Effort Estimation Agent",
            description="Estimate effort required to resolve tickets",
            instructions=instructions
        )

class TicketTriageOrchestrator:
    """Main orchestrator that coordinates all specialized agents."""
    
    def __init__(self):
        self.client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2024-02-15-preview"
        )
        self.deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
        
        # Initialize specialized agents
        self.priority_agent = PriorityAssessmentAgent()
        self.team_agent = TeamAssignmentAgent()
        self.effort_agent = EffortEstimationAgent()
        
        self.system_prompt = """You are the Ticket Triage Orchestrator. Your role is to coordinate the analysis of support tickets by:
        1. Understanding the ticket details
        2. Coordinating with specialized agents
        3. Synthesizing their analyses into a comprehensive assessment
        4. Providing actionable recommendations

You work with:
- Priority Assessment Agent
- Team Assignment Agent
- Effort Estimation Agent

Provide a clear, actionable summary of the ticket triage results."""
    
    def triage_ticket(self, ticket_description: str) -> TicketAssessment:
        """Perform complete ticket triage using all agents."""
        print("Starting ticket triage process...\n")
        
        # Step 1: Priority Assessment
        print("1. Assessing Priority...")
        priority_result = self.priority_agent.analyze(ticket_description)
        priority_analysis = priority_result['analysis']
        print(f"   {priority_analysis}\n")
        
        # Parse priority results
        priority, priority_score, priority_reasoning = self._parse_priority_result(priority_analysis)
        
        # Step 2: Team Assignment
        print("2. Determining Team Assignment...")
        team_result = self.team_agent.analyze(
            ticket_description,
            {"priority": priority, "priority_score": priority_score}
        )
        team_analysis = team_result['analysis']
        print(f"   {team_analysis}\n")
        
        # Parse team results
        assigned_team, team_reasoning = self._parse_team_result(team_analysis)
        
        # Step 3: Effort Estimation
        print("3. Estimating Effort...")
        effort_result = self.effort_agent.analyze(
            ticket_description,
            {"priority": priority, "team": assigned_team}
        )
        effort_analysis = effort_result['analysis']
        print(f"   {effort_analysis}\n")
        
        # Parse effort results
        effort_category, effort_hours, effort_reasoning = self._parse_effort_result(effort_analysis)
        
        # Step 4: Generate Summary
        print("4. Generating Summary...")
        summary = self._generate_summary(
            ticket_description,
            priority_analysis,
            team_analysis,
            effort_analysis
        )
        
        return TicketAssessment(
            priority=priority,
            priority_score=priority_score,
            priority_reasoning=priority_reasoning,
            assigned_team=assigned_team,
            team_reasoning=team_reasoning,
            estimated_effort=effort_category,
            effort_hours=effort_hours,
            effort_reasoning=effort_reasoning,
            summary=summary
        )
    
    def _parse_priority_result(self, analysis: str) -> Tuple[str, int, str]:
        """Parse priority agent results."""
        lines = analysis.strip().split('\n')
        priority = "P3"  # Default
        score = 5  # Default
        reasoning = ""
        
        for line in lines:
            if line.startswith("Priority:"):
                priority = line.split(":", 1)[1].strip()
            elif line.startswith("Score:"):
                try:
                    score = int(line.split(":", 1)[1].strip())
                except:
                    score = 5
            elif line.startswith("Reasoning:"):
                reasoning = line.split(":", 1)[1].strip()
        
        return priority, score, reasoning
    
    def _parse_team_result(self, analysis: str) -> Tuple[str, str]:
        """Parse team agent results."""
        lines = analysis.strip().split('\n')
        team = "Application Team"  # Default
        reasoning = ""
        
        for line in lines:
            if line.startswith("Team:"):
                team = line.split(":", 1)[1].strip()
            elif line.startswith("Reasoning:"):
                reasoning = line.split(":", 1)[1].strip()
        
        return team, reasoning
    
    def _parse_effort_result(self, analysis: str) -> Tuple[str, int, str]:
        """Parse effort agent results."""
        lines = analysis.strip().split('\n')
        effort = "Medium"  # Default
        hours = 16  # Default
        factors = ""
        
        for line in lines:
            if line.startswith("Effort:"):
                effort = line.split(":", 1)[1].strip()
            elif line.startswith("Hours:"):
                try:
                    hours = int(line.split(":", 1)[1].strip())
                except:
                    hours = 16
            elif line.startswith("Factors:"):
                factors = line.split(":", 1)[1].strip()
        
        return effort, hours, factors
    
    def _generate_summary(self, ticket_description: str, priority_analysis: str, 
                         team_analysis: str, effort_analysis: str) -> str:
        """Generate comprehensive summary using all analyses."""
        prompt = f"""Based on the following ticket and analyses, provide a concise executive summary:

Ticket: {ticket_description}

Priority Analysis: {priority_analysis}

Team Analysis: {team_analysis}

Effort Analysis: {effort_analysis}

Provide a 2-3 sentence summary with key recommendations."""
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        return response.choices[0].message.content

def save_triage_report(ticket_description: str, assessment: TicketAssessment):
    """Save the triage report to a file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"../data/triage_report_{timestamp}.md"
    
    report = f"""# Ticket Triage Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Ticket Description
{ticket_description}

## Triage Assessment

### Priority
- **Level**: {assessment.priority}
- **Score**: {assessment.priority_score}/10
- **Reasoning**: {assessment.priority_reasoning}

### Team Assignment
- **Assigned To**: {assessment.assigned_team}
- **Reasoning**: {assessment.team_reasoning}

### Effort Estimation
- **Category**: {assessment.estimated_effort}
- **Estimated Hours**: {assessment.effort_hours}
- **Key Factors**: {assessment.effort_reasoning}

## Executive Summary
{assessment.summary}

## Recommendations
1. Assign to {assessment.assigned_team} immediately
2. Set priority as {assessment.priority}
3. Allocate {assessment.effort_hours} hours for resolution
4. Monitor progress based on priority score of {assessment.priority_score}/10
"""
    
    os.makedirs("../data", exist_ok=True)
    with open(filename, 'w') as f:
        f.write(report)
    
    print(f"\nReport saved to: {filename}")
    return filename

def main():
    """Main function to demonstrate multi-agent ticket triage."""
    print("=== Multi-Agent Ticket Triage System ===\n")
    
    # Sample tickets for demonstration
    sample_tickets = [
        {
            "title": "Production Database Down",
            "description": "Our main production database is completely unresponsive. All customer transactions are failing. This started 30 minutes ago after a routine maintenance window. Error logs show connection timeouts and the database service won't restart. Affecting all 5000+ active users."
        },
        {
            "title": "Login Button Color Wrong",
            "description": "The login button on the homepage is showing as blue instead of our brand color green. This is only happening on the mobile version of the site. Desktop version looks correct."
        },
        {
            "title": "API Performance Degradation",
            "description": "Our REST API response times have increased from 200ms average to 2-3 seconds over the past week. Some endpoints are timing out. This is affecting our mobile app performance and third-party integrations. No recent deployments were made."
        },
        {
            "title": "New Employee Cannot Access Email",
            "description": "A new employee (John Smith) who started today cannot access their email account. They can log into the main portal but get an 'Access Denied' error when trying to open Outlook. Their manager confirmed they should have standard access."
        }
    ]
    
    orchestrator = TicketTriageOrchestrator()
    
    # Process each ticket
    for i, ticket in enumerate(sample_tickets, 1):
        print(f"\n{'='*60}")
        print(f"TICKET {i}: {ticket['title']}")
        print(f"{'='*60}\n")
        print(f"Description: {ticket['description']}\n")
        
        # Perform triage
        assessment = orchestrator.triage_ticket(ticket['description'])
        
        # Save report
        report_file = save_triage_report(ticket['description'], assessment)
        
        print(f"\n{'='*60}\n")
        
        # Brief pause between tickets
        import time
        time.sleep(2)

def interactive_mode():
    """Interactive mode for custom ticket triage."""
    print("=== Multi-Agent Ticket Triage System - Interactive Mode ===")
    print("Enter ticket descriptions for triage analysis.")
    print("Type 'quit' to exit.\n")
    
    orchestrator = TicketTriageOrchestrator()
    
    while True:
        print("\n" + "-"*60)
        ticket_description = input("Enter ticket description: ").strip()
        
        if ticket_description.lower() == 'quit':
            print("Exiting triage system. Goodbye!")
            break
        
        if not ticket_description:
            print("Please enter a valid ticket description.")
            continue
        
        # Perform triage
        assessment = orchestrator.triage_ticket(ticket_description)
        
        # Display results
        print(f"\n{'='*40}")
        print("TRIAGE RESULTS")
        print(f"{'='*40}")
        print(f"Priority: {assessment.priority} (Score: {assessment.priority_score}/10)")
        print(f"Assign to: {assessment.assigned_team}")
        print(f"Effort: {assessment.estimated_effort} ({assessment.effort_hours} hours)")
        print(f"\nSummary: {assessment.summary}")
        
        # Save report
        save_triage_report(ticket_description, assessment)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_mode()
    else:
        main()