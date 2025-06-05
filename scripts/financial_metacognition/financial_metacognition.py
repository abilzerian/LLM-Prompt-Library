#!/usr/bin/env python3
"""
Financial metacognition analysis tool for evaluating AI interpretations of financial prompts.
"""
import json
import argparse
import os
from typing import List, Dict, Any, Optional
import datetime
import spacy
from spacy.matcher import Matcher

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(SCRIPT_DIR, "config")

# Load financial term databases from JSON files
with open(os.path.join(CONFIG_DIR, "financial_concepts.json"), "r") as f:
    FINANCIAL_CONCEPTS = json.load(f)

with open(os.path.join(CONFIG_DIR, "bias_patterns.json"), "r") as f:
    BIAS_PATTERNS = json.load(f)

with open(os.path.join(CONFIG_DIR, "limitation_patterns.json"), "r") as f:
    LIMITATION_PATTERNS = json.load(f)

with open(os.path.join(CONFIG_DIR, "confidence_patterns.json"), "r") as f:
    CONFIDENCE_PATTERNS = json.load(f)

nlp = spacy.load("en_core_web_lg")

def analyze_financial_prompt(prompt: str, model_response: str, region: str = "US") -> Dict[str, Any]:
    """
    Analyze a financial prompt and the AI model's response to identify potential biases and limitations.

    Args:
        prompt (str): The financial prompt given to the AI model.
        model_response (str): The AI model's response to the prompt.
        region (str): The geographic region for region-specific analysis (default: "US").

    Returns:
        Dict[str, Any]: A dictionary containing the analysis results, including identified biases,
        limitations, financial concepts referenced, confidence assessment, and recommendations.
    """
    analysis = {
        "meta_analysis": {
            "timestamp": datetime.datetime.now().isoformat(),
            "prompt_length": len(prompt),
            "response_length": len(model_response),
            "region": region,
        },
        "financial_concepts": identify_financial_concepts(prompt, model_response, region),
        "potential_biases": identify_potential_biases(prompt, model_response),
        "reasoning_limitations": identify_reasoning_limitations(model_response),
        "confidence_assessment": assess_confidence(model_response),
        "recommendations": []
    }
    
    # Generate recommendations based on the analysis
    analysis["recommendations"] = generate_recommendations(analysis)
    
    return analysis

def identify_financial_concepts(prompt: str, response: str, region: str) -> Dict[str, Any]:
    """
    Identify financial concepts mentioned in the prompt and response using NLP, and analyze how they're interpreted.
    
    Args:
        prompt (str): The financial prompt.
        response (str): The model's response.
        region (str): The geographic region for region-specific concepts.
        
    Returns:
        Dict[str, Any]: Dictionary of financial concepts identified and their interpretation.
    """
    doc_prompt = nlp(prompt)
    doc_response = nlp(response)
    
    # Use spaCy's rule-based matching for concept identification
    matcher = Matcher(nlp.vocab)
    
    found_concepts = {}
    
    for category, terms in FINANCIAL_CONCEPTS[region].items():
        category_concepts = []
        
        # Add phrase patterns to the matcher
        patterns = [[{"LOWER": term.lower()}] for term in terms]
        matcher.add(category, patterns)
        
        # Find matches in the prompt and response
        prompt_matches = matcher(doc_prompt)
        response_matches = matcher(doc_response)
        
        for match_id, start, end in prompt_matches + response_matches:
            term = doc_prompt[start:end].text if match_id in prompt_matches else doc_response[start:end].text
            concept_info = {
                "term": term,
                "prompt_mentions": len([m for m in prompt_matches if m[0] == match_id]),
                "response_mentions": len([m for m in response_matches if m[0] == match_id]),
                "acknowledged": any(m[0] == match_id for m in prompt_matches) and any(m[0] == match_id for m in response_matches),
                "introduced_by_model": not any(m[0] == match_id for m in prompt_matches) and any(m[0] == match_id for m in response_matches)
            }
            category_concepts.append(concept_info)
        
        if category_concepts:
            found_concepts[category] = category_concepts
        
        # Clear the matcher for the next category
        matcher.remove(category)
    
    # Analyze how many concepts from prompt were addressed in response
    total_requested_concepts = sum(1 for cat in found_concepts.values() 
                                  for concept in cat if concept["prompt_mentions"] > 0)
    addressed_concepts = sum(1 for cat in found_concepts.values() 
                            for concept in cat if concept["acknowledged"])
    
    coverage = {
        "total_financial_concepts_in_prompt": total_requested_concepts,
        "concepts_addressed_in_response": addressed_concepts,
        "coverage_percentage": (addressed_concepts / total_requested_concepts * 100) if total_requested_concepts > 0 else 100,
        "model_introduced_concepts": sum(1 for cat in found_concepts.values() 
                                       for concept in cat if concept["introduced_by_model"])
    }
    
    return {
        "identified_concepts": found_concepts,
        "concept_coverage": coverage
    }

def identify_potential_biases(prompt: str, response: str) -> List[Dict[str, str]]:
    """
    Identify potential biases in the AI model's financial analysis using NLP.
    
    Args:
        prompt (str): The financial prompt.
        response (str): The model's response.
        
    Returns:
        List[Dict[str, str]]: List of potential biases identified.
    """
    biases = []
    
    doc_response = nlp(response)
    
    for bias_type, patterns in BIAS_PATTERNS.items():
        matcher = Matcher(nlp.vocab)
        matcher.add(bias_type, patterns)
        
        matches = matcher(doc_response)
        
        if len(matches) >= 2:
            biases.append({
                "type": bias_type,
                "description": BIAS_PATTERNS[bias_type]["description"],
                "impact": BIAS_PATTERNS[bias_type]["impact"]
            })
    
    return biases

def identify_reasoning_limitations(response: str) -> List[Dict[str, str]]:
    """
    Identify potential limitations in the AI model's financial reasoning using NLP.
    
    Args:
        response (str): The model's response.
        
    Returns:
        List[Dict[str, str]]: List of identified reasoning limitations.
    """
    limitations = []
    
    doc_response = nlp(response)
    
    for limitation_type, patterns in LIMITATION_PATTERNS.items():
        matcher = Matcher(nlp.vocab)
        matcher.add(limitation_type, patterns)
        
        matches = matcher(doc_response)
        
        if not matches:
            limitations.append({
                "type": limitation_type,
                "description": LIMITATION_PATTERNS[limitation_type]["description"],
                "impact": LIMITATION_PATTERNS[limitation_type]["impact"]
            })
    
    return limitations

def assess_confidence(response: str) -> Dict[str, Any]:
    """
    Assess the implied confidence level in the model's financial response using NLP.
    
    Args:
        response (str): The model's response.
        
    Returns:
        Dict[str, Any]: Confidence assessment metrics.
    """
    doc_response = nlp(response)
    
    high_confidence_count = 0
    low_confidence_count = 0
    
    for pattern_type in ["high", "low"]:
        for pattern in CONFIDENCE_PATTERNS[pattern_type]:
            matcher = Matcher(nlp.vocab)
            matcher.add(pattern_type, [pattern])
            
            matches = matcher(doc_response)
            
            if pattern_type == "high":
                high_confidence_count += len(matches)
            else:
                low_confidence_count += len(matches)
    
    # Calculate confidence ratio
    total_markers = high_confidence_count + low_confidence_count
    confidence_ratio = high_confidence_count / total_markers if total_markers > 0 else 0.5
    
    # Determine confidence level based on ratio thresholds
    if confidence_ratio >= 0.8:
        confidence_level = "Very High"
        appropriateness = "Potentially Problematic"
        explanation = "Excessive confidence in financial forecasting is often unwarranted given market uncertainties."
    elif confidence_ratio >= 0.6:
        confidence_level = "High"
        appropriateness = "Questionable"
        explanation = "High confidence should be balanced with acknowledgment of uncertainty in financial matters."
    elif confidence_ratio >= 0.4:
        confidence_level = "Moderate"
        appropriateness = "Appropriate"
        explanation = "Balanced expression of confidence and uncertainty is suitable for most financial analyses."
    elif confidence_ratio >= 0.2:
        confidence_level = "Low"
        appropriateness = "Appropriate"
        explanation = "Conservative confidence level acknowledges the inherent uncertainty in financial markets."
    else:
        confidence_level = "Very Low"
        appropriateness = "May be overly cautious"
        explanation = "Extremely low confidence may miss opportunities to provide useful financial guidance."
    
    return {
        "confidence_level": confidence_level,
        "confidence_ratio": confidence_ratio,
        "high_confidence_markers": high_confidence_count,
        "uncertainty_markers": low_confidence_count,
        "appropriateness": appropriateness,
        "explanation": explanation
    }

def generate_recommendations(analysis: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Generate recommendations based on the financial prompt analysis.
    
    Args:
        analysis (Dict[str, Any]): The analysis results.
        
    Returns:
        List[Dict[str, str]]: Recommendations for improving prompt-response quality.
    """
    recommendations = []
    
    # Recommendations based on concept coverage
    coverage = analysis["financial_concepts"]["concept_coverage"]["coverage_percentage"]
    if coverage < 80:
        recommendations.append({
            "category": "concept_coverage",
            "recommendation": "Reformulate prompt to encourage more comprehensive coverage of financial concepts.",
            "explanation": f"Only {coverage:.1f}% of financial concepts in your prompt were addressed in the response."
        })
    
    # Recommendations based on biases
    for bias in analysis["potential_biases"]:
        if bias["type"] == "recency_bias":
            recommendations.append({
                "category": "bias_mitigation",
                "recommendation": "Request historical context and long-term perspectives in your prompt.",
                "explanation": "The AI tends to focus on recent market events. Explicitly ask for historical patterns."
            })
        elif bias["type"] == "overconfidence":
            recommendations.append({
                "category": "bias_mitigation",
                "recommendation": "Ask the AI to express uncertainty and provide probability ranges.",
                "explanation": "The response showed overconfidence. Request explicit acknowledgment of uncertainty."
            })
        elif bias["type"] == "narrative_fallacy":
            recommendations.append({
                "category": "bias_mitigation",
                "recommendation": "Request multiple alternative explanations for financial phenomena.",
                "explanation": "The AI tends to create simple narratives. Ask for competing explanations."
            })
    
    # Recommendations based on reasoning limitations
    for limitation in analysis["reasoning_limitations"]:
        if limitation["type"] == "insufficient_uncertainty":
            recommendations.append({
                "category": "reasoning_improvement",
                "recommendation": "Explicitly ask for confidence levels and ranges in financial projections.",
                "explanation": "The response lacked uncertainty acknowledgment. Request probabilistic reasoning."
            })
        elif limitation["type"] == "oversimplification":
            recommendations.append({
                "category": "reasoning_improvement",
                "recommendation": "Ask the AI to explore the complexity and interconnections in financial systems.",
                "explanation": "The response oversimplified complex concepts. Request exploration of nuances."
            })
        elif limitation["type"] == "normalcy_bias":
            recommendations.append({
                "category": "reasoning_improvement",
                "recommendation": "Request analysis of tail risks and extreme scenarios.",
                "explanation": "The response didn't address potential black swan events. Ask specifically about worst-case scenarios."
            })
    
    # Recommendations based on confidence assessment
    confidence_level = analysis["confidence_assessment"]["confidence_level"]
    appropriateness = analysis["confidence_assessment"]["appropriateness"]
    
    if appropriateness == "Potentially Problematic" or appropriateness == "Questionable":
        recommendations.append({
            "category": "confidence_calibration",
            "recommendation": "Request more nuanced and calibrated expressions of confidence.",
            "explanation": f"The AI expressed {confidence_level.lower()} confidence, which may be inappropriate for financial forecasting."
        })
    
    # Add meta-recommendations
    recommendations.append({
        "category": "metacognitive_practice",
        "recommendation": "Include a request for the AI to 'think about its thinking' in financial analysis.",
        "explanation": "Ask the AI to explicitly reason about its own assumptions and limitations in financial contexts."
    })
    
    return recommendations

def analyze_from_files(prompt_file: str, response_file: str, output_file: Optional[str] = None, region: str = "US") -> Dict[str, Any]:
    """
    Analyze financial prompt and response from files.
    
    Args:
        prompt_file (str): Path to file containing the financial prompt.
        response_file (str): Path to file containing the model's response.
        output_file (Optional[str]): Path to save the analysis results as JSON.
        region (str): The geographic region for region-specific analysis (default: "US").
        
    Returns:
        Dict[str, Any]: The analysis results.
    """
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read()
        
        with open(response_file, 'r', encoding='utf-8') as f:
            response = f.read()
        
        analysis = analyze_financial_prompt(prompt, response, region)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2)
                print(f"Analysis saved to {output_file}")
        
        return analysis
    
    except Exception as e:
        print(f"Error analyzing files: {str(e)}")
        return {"error": str(e)}

def format_analysis_report(analysis: Dict[str, Any]) -> str:
    """
    Format the analysis results into a readable report.
    
    Args:
        analysis (Dict[str, Any]): The analysis results.
        
    Returns:
        str: Formatted report.
    """
    report = []
    
    # Header
    report.append("# AI Financial Interpretation Analysis Report")
    report.append(f"Generated on: {analysis['meta_analysis']['timestamp']}")
    report.append(f"Region: {analysis['meta_analysis']['region']}")
    report.append("\n## Summary")
    
    # Concept coverage summary
    concept_coverage = analysis["financial_concepts"]["concept_coverage"]
    report.append(f"- **Financial Concepts**: {concept_coverage['total_financial_concepts_in_prompt']} concepts in prompt, "
                 f"{concept_coverage['concepts_addressed_in_response']} addressed ({concept_coverage['coverage_percentage']:.1f}%)")
    
    # Bias summary
    report.append(f"- **Potential Biases**: {len(analysis['potential_biases'])} detected")
    
    # Limitations summary
    report.append(f"- **Reasoning Limitations**: {len(analysis['reasoning_limitations'])} identified")
    
    # Confidence summary
    report.append(f"- **Confidence Level**: {analysis['confidence_assessment']['confidence_level']} "
                 f"({analysis['confidence_assessment']['appropriateness']})")
    
    # Financial concepts section
    report.append("\n## Financial Concepts Analysis")
    
    # Add concept categories
    for category, concepts in analysis["financial_concepts"]["identified_concepts"].items():
        category_name = category.replace("_", " ").title()
        report.append(f"\n### {category_name}")
        
        for concept in concepts:
            term = concept["term"]
            prompt_mentions = concept["prompt_mentions"]
            response_mentions = concept["response_mentions"]
            
            status = ""
            if concept["acknowledged"]:
                status = "✓ Addressed"
            elif concept["introduced_by_model"]:
                status = "+ Introduced by AI"
            else:
                status = "✗ Not addressed"
            
            report.append(f"- **{term}**: {status} (Prompt: {prompt_mentions}, Response: {response_mentions})")
    
    # Biases section
    report.append("\n## Potential Biases")
    
    if not analysis["potential_biases"]:
        report.append("\nNo significant biases detected.")
    else:
        for bias in analysis["potential_biases"]:
            report.append(f"\n### {bias['type'].replace('_', ' ').title()}")
            report.append(f"**Description**: {bias['description']}")
            report.append(f"**Potential Impact**: {bias['impact']}")
    
    # Reasoning limitations section
    report.append("\n## Reasoning Limitations")
    
    if not analysis["reasoning_limitations"]:
        report.append("\nNo significant reasoning limitations detected.")
    else:
        for limitation in analysis["reasoning_limitations"]:
            report.append(f"\n### {limitation['type'].replace('_', ' ').title()}")
            report.append(f"**Description**: {limitation['description']}")
            report.append(f"**Potential Impact**: {limitation['impact']}")
    
    # Confidence assessment section
    report.append("\n## Confidence Assessment")
    confidence = analysis["confidence_assessment"]
    report.append(f"**Level**: {confidence['confidence_level']}")
    report.append(f"**Appropriateness**: {confidence['appropriateness']}")
    report.append(f"**Explanation**: {confidence['explanation']}")
    report.append(f"**Details**: {confidence['high_confidence_markers']} high confidence markers, "
                 f"{confidence['uncertainty_markers']} uncertainty markers "
                 f"(Confidence ratio: {confidence['confidence_ratio']:.2f})")
    
    # Recommendations section
    report.append("\n## Recommendations")
    
    for recommendation in analysis["recommendations"]:
        report.append(f"\n### {recommendation['category'].replace('_', ' ').title()}")
        report.append(f"**Recommendation**: {recommendation['recommendation']}")
        report.append(f"**Explanation**: {recommendation['explanation']}")
    
    return "\n".join(report)

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Analyze AI interpretations of financial prompts to identify biases and limitations."
    )
    
    # Add input options group
    input_group = parser.add_argument_group("Input Options")
    input_group.add_argument("--prompt", type=str, help="Financial prompt text (direct input)")
    input_group.add_argument("--response", type=str, help="AI model response text (direct input)")
    input_group.add_argument("--prompt-file", type=str, help="Path to file containing the financial prompt")
    input_group.add_argument("--response-file", type=str, help="Path to file containing the AI model response")
    
    # Add output options group
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument("--output", type=str, help="Path to save analysis results (JSON format)")
    output_group.add_argument("--report", type=str, help="Path to save human-readable analysis report (Markdown format)")
    output_group.add_argument("--print-report", action="store_true", help="Print the report to console")
    
    args = parser.parse_args()
    
    # Validate input options
    if (args.prompt is None and args.prompt_file is None) or (args.response is None and args.response_file is None):
        parser.error("You must provide either direct text input (--prompt and --response) or input files (--prompt-file and --response-file)")
        return
    
    # Get prompt and response from arguments or files
    prompt = args.prompt
    response = args.response
    
    if args.prompt_file:
        try:
            with open(args.prompt_file, 'r', encoding='utf-8') as f:
                prompt = f.read()
        except Exception as e:
            print(f"Error reading prompt file: {str(e)}")
            return
    
    if args.response_file:
        try:
            with open(args.response_file, 'r', encoding='utf-8') as f:
                response = f.read()
        except Exception as e:
            print(f"Error reading response file: {str(e)}")
            return
    
    # Perform analysis
    analysis = analyze_financial_prompt(prompt, response)
    
    # Generate report
    report = format_analysis_report(analysis)
    
    # Save JSON output if requested
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2)
            print(f"Analysis results saved to {args.output}")
        except Exception as e:
            print(f"Error saving analysis results: {str(e)}")
    
    # Save report if requested
    if args.report:
        try:
            with open(args.report, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Analysis report saved to {args.report}")
        except Exception as e:
            print(f"Error saving analysis report: {str(e)}")
    
    # Print report if requested
    if args.print_report:
        print("\n" + report)
    elif not args.output and not args.report:
        # If no output options were specified, print the report by default
        print("\n" + report)
    
if __name__ == "__main__":
    main()