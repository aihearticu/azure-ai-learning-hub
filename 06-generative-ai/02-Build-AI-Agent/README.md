# Exercise 02: Build AI Agent

This exercise demonstrates building an AI agent for data analysis using Azure OpenAI.

## Overview

The agent can:
- Analyze CSV data files
- Generate insights and patterns
- Create visualizations
- Provide comprehensive reports

## Features

### Data Analysis Agent
- Loads and analyzes sales data
- Uses GPT-4o for intelligent insights
- Generates multiple visualizations
- Creates comprehensive reports

### Visualizations
1. **Sales by Product** - Bar chart showing total sales
2. **Sales Trend** - Line chart showing trends over time
3. **Regional Distribution** - Pie chart for regional sales

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

3. **Run the Agent**:
   ```bash
   cd src
   python simple_data_agent.py
   ```

## Implementation Details

### Simple Data Agent (`simple_data_agent.py`)
- Uses Azure OpenAI for analysis
- Pandas for data manipulation
- Matplotlib for visualizations
- Generates base64-encoded charts

### Data Analysis Agent (`data_analysis_agent.py`)
- Advanced implementation using Azure AI Agents SDK
- Code Interpreter tool integration
- Thread-based conversations
- File upload capabilities

## Sample Data

The `data/sales_data.csv` contains:
- Monthly sales data
- Multiple products (Laptop, Tablet, Phone)
- Regional breakdown (North, South)
- Sales amounts and unit counts

## Output

The agent generates:
- Console analysis for each prompt
- PNG visualizations saved to data folder
- Comprehensive markdown report
- AI-powered insights and recommendations

## Key Learnings

1. **AI Integration**: Using Azure OpenAI for intelligent data analysis
2. **Structured Prompts**: Crafting system prompts for consistent analysis
3. **Data Visualization**: Generating charts programmatically
4. **Report Generation**: Creating comprehensive analysis reports

## Next Steps

- Extend to support more file formats (Excel, JSON)
- Add interactive visualizations
- Implement real-time data streaming
- Create specialized agents for different domains

## Reference

Based on: [Microsoft Learn - Build AI Agent](https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/02-build-ai-agent.html)