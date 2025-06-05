#!/usr/bin/env python3
"""
Test script for demonstrating the enhanced capabilities of the financial_metacognition.py script,
with region-specific analysis and optional sentiment analysis.
"""

import sys
import os
import json
import argparse

# Add parent directory to path to import the financial_metacognition module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from financial_metacognition import analyze_financial_prompt, format_analysis_report

def main():
    """Run a test demonstration of financial metacognition analysis with different configurations."""
    parser = argparse.ArgumentParser(
        description="Test the financial metacognition module with different regional configurations."
    )
    
    parser.add_argument(
        "--region", 
        choices=["US", "EU", "Asia"], 
        default="US",
        help="Region for terminology (US, EU, or Asia)"
    )
    
    parser.add_argument(
        "--sentiment", 
        action="store_true",
        help="Enable sentiment analysis"
    )
    
    parser.add_argument(
        "--accounting-standard", 
        choices=["GAAP", "IFRS"], 
        default="GAAP",
        help="Expected accounting standard (GAAP or IFRS)"
    )
    
    args = parser.parse_args()
    
    # Paths to example files
    examples_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_file = os.path.join(examples_dir, "financial_prompt.txt")
    response_file = os.path.join(examples_dir, "financial_response.txt")
    
    try:
        # Read example files
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read()
        
        with open(response_file, 'r', encoding='utf-8') as f:
            response = f.read()
        
        print(f"\n{'='*80}")
        print("TESTING FINANCIAL METACOGNITION ANALYSIS WITH CONFIGURATION:")
        print(f"Region: {args.region}")
        print(f"Sentiment Analysis: {'Enabled' if args.sentiment else 'Disabled'}")
        print(f"Expected Accounting Standard: {args.accounting_standard}")
        print(f"{'='*80}\n")
        
        # Run the analysis
        analysis = analyze_financial_prompt(prompt, response, region=args.region)
        
        # Check for accounting standard in response
        if args.accounting_standard == "GAAP" and "GAAP" not in response:
            if "reasoning_limitations" not in analysis:
                analysis["reasoning_limitations"] = []
            
            analysis["reasoning_limitations"].append({
                "type": "missing_accounting_standard",
                "description": "The response doesn't reference GAAP accounting standards",
                "impact": "May lack US-specific accounting context"
            })
        
        elif args.accounting_standard == "IFRS" and "IFRS" not in response:
            if "reasoning_limitations" not in analysis:
                analysis["reasoning_limitations"] = []
            
            analysis["reasoning_limitations"].append({
                "type": "missing_accounting_standard",
                "description": "The response doesn't reference IFRS accounting standards",
                "impact": "May lack international accounting context"
            })
        
        # Generate and print report
        report = format_analysis_report(analysis)
        print(report)
        
        # Save analysis to JSON file
        output_file = os.path.join(examples_dir, f"analysis_{args.region.lower()}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"\nAnalysis saved to {output_file}")
    
    except Exception as e:
        print(f"Error running test: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 