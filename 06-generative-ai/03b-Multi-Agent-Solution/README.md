# Exercise 03b: Build Multi-Agent Solution

This exercise demonstrates building a multi-agent system for ticket triage using Azure OpenAI.

## Overview

The Ticket Triage System uses multiple specialized agents working together to:
- Assess ticket priority
- Determine team assignment
- Estimate resolution effort
- Generate comprehensive triage reports

## Architecture

### Specialized Agents

1. **Priority Assessment Agent**
   - Evaluates ticket severity (P1-P4)
   - Assigns priority score (1-10)
   - Provides reasoning for priority level

2. **Team Assignment Agent**
   - Determines appropriate team
   - Considers technical domain
   - Identifies secondary teams if needed

3. **Effort Estimation Agent**
   - Estimates resolution time
   - Categorizes effort level
   - Identifies key complexity factors

4. **Ticket Triage Orchestrator**
   - Coordinates all agents
   - Synthesizes analyses
   - Generates executive summary

## Setup

1. **Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Copy `.env.example` to `.env`
   - Add your Azure OpenAI credentials

3. **Run the System**:
   ```bash
   cd src
   python ticket_triage_agents.py              # Demo mode
   python ticket_triage_agents.py interactive  # Interactive mode
   ```

## Usage Modes

### Demo Mode
Processes 4 sample tickets demonstrating different scenarios:
- Critical production issues
- Minor cosmetic problems
- Performance degradation
- Access/security issues

### Interactive Mode
Allows custom ticket input for real-time triage analysis.

## Output

### Console Output
- Step-by-step agent analysis
- Real-time processing feedback
- Summary results

### Triage Reports
Markdown reports saved to `data/` containing:
- Full ticket description
- Priority assessment with reasoning
- Team assignment with justification
- Effort estimation with factors
- Executive summary
- Actionable recommendations

## Sample Triage Flow

```
1. Ticket submitted: "Database is down"
2. Priority Agent: "P1 - Critical, Score: 10/10"
3. Team Agent: "Infrastructure Team"
4. Effort Agent: "Quick Fix - 2 hours"
5. Summary: "Critical database outage requiring immediate Infrastructure Team response"
```

## Implementation Details

### Agent Communication
- Each agent has specialized instructions
- Context is passed between agents
- Results are parsed and structured

### Priority Levels
- **P1 (Critical)**: System down, major impact
- **P2 (High)**: Significant issues, workarounds exist
- **P3 (Medium)**: Moderate issues, limited impact
- **P4 (Low)**: Minor issues, cosmetic problems

### Team Categories
- Infrastructure Team
- Application Team
- Security Team
- Database Team
- Customer Success

### Effort Categories
- Quick Fix: < 2 hours
- Small: 2-8 hours
- Medium: 8-24 hours
- Large: 24-80 hours
- Extra Large: > 80 hours

## Key Features

1. **Multi-Agent Collaboration**: Agents work together sharing context
2. **Structured Analysis**: Consistent format for all assessments
3. **Comprehensive Reports**: Detailed documentation for each ticket
4. **Flexible Integration**: Can be adapted to existing ticketing systems

## File Structure
```
03b-Multi-Agent-Solution/
├── src/
│   └── ticket_triage_agents.py  # Main implementation
├── data/                        # Generated triage reports
├── requirements.txt
├── .env.example
└── README.md
```

## Key Learnings

1. **Agent Orchestration**: Coordinating multiple AI agents for complex tasks
2. **Context Sharing**: Passing information between specialized agents
3. **Result Synthesis**: Combining multiple analyses into actionable insights
4. **Structured Output**: Parsing and formatting agent responses

## Next Steps

- Integrate with real ticketing systems (ServiceNow, Jira)
- Add more specialized agents (Cost Estimator, Risk Assessor)
- Implement feedback loop for continuous improvement
- Create API endpoints for system integration

## Reference

Based on: [Microsoft Learn - Build Multi-Agent Solution](https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/03b-build-multi-agent-solution.html)