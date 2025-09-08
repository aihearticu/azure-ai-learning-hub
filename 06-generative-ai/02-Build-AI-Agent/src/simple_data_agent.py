import os
import json
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Load environment variables
load_dotenv()

class SimpleDataAgent:
    """Simplified AI Agent for data analysis."""
    
    def __init__(self):
        """Initialize the Azure OpenAI client."""
        self.client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version="2024-02-15-preview"
        )
        self.deployment_name = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
        
        # Agent instructions
        self.system_prompt = """You are a data analyst AI agent. Your role is to:
        1. Analyze data provided by users
        2. Generate insights and recommendations
        3. Suggest appropriate visualizations
        4. Provide clear explanations of findings
        
        When analyzing data:
        - First understand the data structure
        - Identify key patterns and trends
        - Recommend appropriate charts/graphs
        - Summarize findings clearly
        
        Output your analysis in a structured format with sections for:
        - Data Overview
        - Key Insights
        - Visualization Recommendations
        - Summary"""
    
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from CSV file."""
        print(f"Loading data from: {file_path}")
        df = pd.read_csv(file_path)
        print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    
    def analyze_data(self, df: pd.DataFrame, user_prompt: str) -> str:
        """Analyze data using AI."""
        # Create data summary for the AI
        data_summary = f"""
        Data Shape: {df.shape}
        Columns: {list(df.columns)}
        Data Types: {df.dtypes.to_dict()}
        
        First 5 rows:
        {df.head().to_string()}
        
        Statistical Summary:
        {df.describe().to_string()}
        """
        
        # Create the analysis prompt
        analysis_prompt = f"""
        User Request: {user_prompt}
        
        Data Information:
        {data_summary}
        
        Please provide a comprehensive analysis based on the user's request.
        """
        
        # Get AI analysis
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    def create_visualizations(self, df: pd.DataFrame) -> dict:
        """Create basic visualizations from the data."""
        visualizations = {}
        
        # 1. Sales by Product
        plt.figure(figsize=(10, 6))
        product_sales = df.groupby('Product')['Sales'].sum().sort_values(ascending=False)
        product_sales.plot(kind='bar', color='skyblue')
        plt.title('Total Sales by Product')
        plt.xlabel('Product')
        plt.ylabel('Total Sales ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save to base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        visualizations['sales_by_product'] = base64.b64encode(buf.read()).decode()
        plt.close()
        
        # 2. Sales Trend Over Time
        plt.figure(figsize=(12, 6))
        df['Date'] = pd.to_datetime(df['Date'])
        for product in df['Product'].unique():
            product_data = df[df['Product'] == product]
            monthly_sales = product_data.groupby('Date')['Sales'].sum()
            plt.plot(monthly_sales.index, monthly_sales.values, marker='o', label=product, linewidth=2)
        
        plt.title('Sales Trend Over Time by Product')
        plt.xlabel('Date')
        plt.ylabel('Sales ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save to base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        visualizations['sales_trend'] = base64.b64encode(buf.read()).decode()
        plt.close()
        
        # 3. Regional Performance
        plt.figure(figsize=(10, 6))
        region_sales = df.groupby('Region')['Sales'].sum()
        plt.pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%', startangle=90)
        plt.title('Sales Distribution by Region')
        plt.axis('equal')
        
        # Save to base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        visualizations['regional_distribution'] = base64.b64encode(buf.read()).decode()
        plt.close()
        
        return visualizations
    
    def generate_report(self, df: pd.DataFrame, analysis: str, visualizations: dict) -> str:
        """Generate a comprehensive report."""
        report = f"""
# Data Analysis Report

## Dataset Overview
- **Total Records**: {len(df)}
- **Date Range**: {df['Date'].min()} to {df['Date'].max()}
- **Products**: {', '.join(df['Product'].unique())}
- **Regions**: {', '.join(df['Region'].unique())}

## AI Analysis
{analysis}

## Key Metrics
- **Total Sales**: ${df['Sales'].sum():,.2f}
- **Average Sale**: ${df['Sales'].mean():,.2f}
- **Total Units Sold**: {df['Units'].sum():,}

## Visualizations Generated
1. Sales by Product - Bar chart showing total sales for each product
2. Sales Trend - Line chart showing sales trends over time
3. Regional Distribution - Pie chart showing sales distribution by region

## Data Summary by Product
"""
        # Add product summary
        product_summary = df.groupby('Product').agg({
            'Sales': ['sum', 'mean', 'count'],
            'Units': 'sum'
        }).round(2)
        
        report += product_summary.to_string()
        
        return report

def main():
    """Main function to demonstrate the data analysis agent."""
    print("=== Simple Data Analysis Agent ===\n")
    
    # Initialize agent
    agent = SimpleDataAgent()
    
    # Load data
    data_file = "../data/sales_data.csv"
    if os.path.exists(data_file):
        df = agent.load_data(data_file)
        
        # Analyze data with different prompts
        prompts = [
            "Analyze this sales data and identify the top-performing products and regions.",
            "What are the sales trends over time? Are there any seasonal patterns?",
            "Which product-region combination generates the most revenue?"
        ]
        
        print("\n" + "="*50 + "\n")
        
        for i, prompt in enumerate(prompts, 1):
            print(f"Analysis {i}: {prompt}")
            print("-" * 50)
            
            # Get AI analysis
            analysis = agent.analyze_data(df, prompt)
            print(analysis)
            print("\n" + "="*50 + "\n")
        
        # Create visualizations
        print("Generating visualizations...")
        visualizations = agent.create_visualizations(df)
        
        # Save visualizations
        for name, data in visualizations.items():
            with open(f"../data/{name}.png", "wb") as f:
                f.write(base64.b64decode(data))
            print(f"Saved: {name}.png")
        
        # Generate comprehensive report
        print("\nGenerating comprehensive report...")
        report = agent.generate_report(df, analysis, visualizations)
        
        # Save report
        with open("../data/analysis_report.md", "w") as f:
            f.write(report)
        print("Report saved: analysis_report.md")
        
    else:
        print(f"Data file not found: {data_file}")

if __name__ == "__main__":
    main()