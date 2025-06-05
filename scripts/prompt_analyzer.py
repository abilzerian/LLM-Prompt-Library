#!/usr/bin/env python3
"""
Prompt Analyzer Script

This script analyzes the quality, complexity, and readability of prompt files,
providing actionable suggestions for improvements.
"""

import os
import re
import argparse
import json
import statistics
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Any
import random

# Check if nltk is available (for advanced text analysis)
NLTK_AVAILABLE = False
try:
    import nltk
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    NLTK_AVAILABLE = True
    
    # Download required NLTK resources
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
        
except ImportError:
    pass

class PromptAnalyzer:
    """Class for analyzing prompt files and providing quality feedback."""
    
    # These phrases often indicate clear instructions in prompts
    INSTRUCTION_INDICATORS = [
        "you will", "your task", "you should", "please", "i want you to",
        "do the following", "act as", "you are", "your job", "you must",
        "follow these steps", "your role", "i need you to"
    ]
    
    # These words indicate complexity that might reduce prompt effectiveness
    COMPLEXITY_INDICATORS = [
        "however", "furthermore", "nevertheless", "consequently", "additionally",
        "subsequently", "alternatively", "conversely", "accordingly", "notwithstanding",
        "complicated", "complex", "difficult", "intricate", "sophisticated"
    ]
    
    # Common configuration options in high-quality prompts
    CONFIG_OPTIONS = [
        "reset", "no quotes", "no explanations", "no apologies", "concise",
        "step by step", "bullet points", "be direct", "no preamble"
    ]
    
    def __init__(self, 
                 root_dir: str = "prompts", 
                 verbose: bool = False,
                 min_examples: int = 1,
                 thorough: bool = False):
        """
        Initialize the prompt analyzer.
        
        Args:
            root_dir: Root directory containing prompt files
            verbose: Whether to print detailed information
            min_examples: Minimum recommended number of examples in a prompt
            thorough: Whether to perform more thorough analysis (slower)
        """
        self.root_dir = root_dir
        self.verbose = verbose
        self.min_examples = min_examples
        self.thorough = thorough
        
        # Analysis results storage
        self.prompt_stats = {}
        self.global_stats = {
            "total_prompts": 0,
            "avg_readability_score": 0,
            "avg_clarity_score": 0,
            "avg_structure_score": 0,
            "avg_quality_score": 0,
            "categories": defaultdict(int)
        }
        
        # Initialize stopwords if NLTK is available
        self.stop_words = set()
        if NLTK_AVAILABLE:
            self.stop_words = set(stopwords.words('english'))
    
    def extract_code_blocks(self, content: str) -> List[str]:
        """
        Extract code blocks from markdown content.
        
        Args:
            content: Markdown content
            
        Returns:
            List of code blocks
        """
        # Find all code blocks (enclosed in ```...```)
        code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', content, re.DOTALL)
        return code_blocks
    
    def extract_sections(self, content: str) -> Dict[str, str]:
        """
        Extract key sections from a prompt file.
        
        Args:
            content: Content of the prompt file
            
        Returns:
            Dictionary with sections (title, config, instructions, examples, etc.)
        """
        sections = {
            "title": "",
            "config": "",
            "instructions": "",
            "examples": [],
            "metadata": {},
            "code_blocks": []
        }
        
        # Extract title
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            sections["title"] = title_match.group(1).strip()
        
        # Extract code blocks
        sections["code_blocks"] = self.extract_code_blocks(content)
        
        # Count configuration options
        config_count = 0
        for option in self.CONFIG_OPTIONS:
            if re.search(r'\b' + re.escape(option) + r'\b', content, re.IGNORECASE):
                config_count += 1
                if "config_options" not in sections["metadata"]:
                    sections["metadata"]["config_options"] = []
                sections["metadata"]["config_options"].append(option)
        
        sections["metadata"]["config_count"] = config_count
        
        # Look for instruction patterns
        instruction_indicators = 0
        for indicator in self.INSTRUCTION_INDICATORS:
            instruction_indicators += len(re.findall(r'\b' + re.escape(indicator) + r'\b', content, re.IGNORECASE))
        
        sections["metadata"]["instruction_indicators"] = instruction_indicators
        
        # Count examples (looking for example markers or numbered lists)
        example_patterns = [
            r'(?:Example|For example|Instance)(?:\s+\d+)?:\s*(.*?)(?=(?:Example|For example|Instance)(?:\s+\d+)?:|$)',
            r'(?:^|\n)(?:Examples?|Sample(?:s)?):\s*(.*?)(?=\n#|\n\n|$)',
            r'(?:^|\n)\d+\.\s*(.*?)(?=\n\d+\.|\n#|\n\n|$)'
        ]
        
        examples = []
        for pattern in example_patterns:
            examples.extend(re.findall(pattern, content, re.DOTALL))
        
        sections["examples"] = examples
        sections["metadata"]["example_count"] = len(examples)
        
        return sections
    
    def calculate_readability_score(self, text: str) -> float:
        """
        Calculate readability score based on sentence and word complexity.
        
        Args:
            text: Text to analyze
            
        Returns:
            Readability score (0-100, higher is better/more readable)
        """
        if not text or len(text) < 10:
            return 50.0  # Default score for very short text
            
        if NLTK_AVAILABLE:
            # Use NLTK for better sentence and word tokenization
            sentences = sent_tokenize(text)
            words = word_tokenize(text)
            words = [word for word in words if word.isalnum()]  # Filter out punctuation
        else:
            # Simple fallback
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            words = re.findall(r'\b\w+\b', text)
        
        if not sentences or not words:
            return 50.0
        
        # Calculate average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Calculate percentage of complex words (>6 letters)
        complex_words = [w for w in words if len(w) > 6]
        complex_word_percentage = len(complex_words) / len(words) if words else 0
        
        # Modified Flesch-Kincaid readability formula
        # Adjusted to output higher scores for more readable text
        # Normal F-K gives lower scores for better readability, so we invert it
        readability = 100 - (0.39 * avg_sentence_length + 11.8 * complex_word_percentage - 15.59)
        
        # Clamp to 0-100 range
        return max(0, min(100, readability))
    
    def calculate_structure_score(self, sections: Dict[str, Any]) -> float:
        """
        Calculate a score for the prompt structure.
        
        Args:
            sections: Extracted sections from the prompt
            
        Returns:
            Structure score (0-100)
        """
        score = 0
        
        # Check title
        if sections["title"]:
            score += 15
        
        # Check configuration options
        config_score = min(20, sections["metadata"].get("config_count", 0) * 5)
        score += config_score
        
        # Check for code blocks (indicating examples, structured output, etc.)
        code_block_score = min(15, len(sections["code_blocks"]) * 5)
        score += code_block_score
        
        # Check examples
        example_score = min(20, len(sections["examples"]) * 10)
        score += example_score
        
        # If any examples at all, increase slightly
        if sections["examples"]:
            score += 5
        
        # Instruction indicators
        instruction_score = min(20, sections["metadata"].get("instruction_indicators", 0) * 5)
        score += instruction_score
        
        # Normalize to 0-100
        return min(100, score)
    
    def calculate_clarity_score(self, content: str) -> float:
        """
        Calculate clarity score based on instruction clarity and complexity.
        
        Args:
            content: Prompt content
            
        Returns:
            Clarity score (0-100)
        """
        if not content:
            return 0
            
        # Count instruction indicators
        instruction_count = 0
        for indicator in self.INSTRUCTION_INDICATORS:
            indicator_pattern = r'\b' + re.escape(indicator) + r'\b'
            instruction_count += len(re.findall(indicator_pattern, content, re.IGNORECASE))
        
        # Count complexity indicators (negative factor)
        complexity_count = 0
        for indicator in self.COMPLEXITY_INDICATORS:
            indicator_pattern = r'\b' + re.escape(indicator) + r'\b'
            complexity_count += len(re.findall(indicator_pattern, content, re.IGNORECASE))
        
        # Calculate base score

        # More instructions are good, more complexity is bad
        base_score = 50 + (instruction_count * 5) - (complexity_count * 3)
        
        # Normalize result
        return max(0, min(100, base_score))
    
    def analyze_keyword_density(self, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Analyze keyword density in the text.
        
        Args:
            text: Text to analyze
            top_n: Number of top keywords to return
            
        Returns:
            List of (keyword, count) tuples
        """
        if not NLTK_AVAILABLE or not text:
            return []
            
        # Tokenize and normalize words
        words = word_tokenize(text.lower())
        
        # Remove stopwords and non-alphabetic words
        filtered_words = [word for word in words if word.isalpha() and word not in self.stop_words and len(word) > 2]
        
        # Count word frequencies
        word_freq = Counter(filtered_words)
        
        # Get top N keywords
        return word_freq.most_common(top_n)
    
    def generate_recommendations(self, 
                                analysis: Dict[str, Any], 
                                sections: Dict[str, Any]) -> List[str]:
        """
        Generate recommendations based on analysis results.
        
        Args:
            analysis: Analysis results
            sections: Extracted sections
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Check readability
        if analysis["readability_score"] < 60:
            recommendations.append("⚠️ Improve readability by using shorter sentences and simpler words.")
        
        # Check structure
        if analysis["structure_score"] < 60:
            if not sections["title"]:
                recommendations.append("📋 Add a clear title at the beginning of your prompt (# Title).")
            
            if sections["metadata"].get("config_count", 0) < 3:
                recommendations.append("⚙️ Add more configuration options like 'reset', 'no quotes', 'step by step'.")
            
            if len(sections["examples"]) < self.min_examples:
                recommendations.append(f"📝 Include at least {self.min_examples} examples to demonstrate the desired output.")
        
        # Check clarity
        if analysis["clarity_score"] < 60:
            recommendations.append("🔍 Use clearer instruction patterns like 'Your task is to' or 'You should'.")
            
            if sections["metadata"].get("instruction_indicators", 0) < 2:
                recommendations.append("📢 Add explicit instructions using phrases like 'you will', 'your task is to', etc.")
        
        # Check code blocks
        if not sections["code_blocks"]:
            recommendations.append("💻 Consider adding code blocks (```) to structure your prompt or example outputs.")
        
        # Add general recommendations if the overall score is low
        if analysis["quality_score"] < 70:
            general_recs = [
                "🔄 Start with a clear configuration section defining how the LLM should behave.",
                "📋 Include a clear section describing the task or role.",
                "🔢 Structure your prompt with clear sections for better parsing by the LLM.",
                "⚡ Use the right balance of constraints and freedom in your instructions."
            ]
            # Add 1-2 random general recommendations
            recommendations.extend(random.sample(general_recs, min(2, len(general_recs))))
        
        return recommendations

    def evaluate(self, prompt: str) -> float:
        """Evaluate a prompt string and return a quality score between 0 and 1."""
        if not prompt or len(prompt.strip()) < 10:
            return 0.0

        sections = self.extract_sections(prompt)
        readability = self.calculate_readability_score(prompt)
        structure = self.calculate_structure_score(sections)
        clarity = self.calculate_clarity_score(prompt)

        quality_score = (
            readability * 0.3 +
            structure * 0.4 +
            clarity * 0.3
        ) / 100

        return max(0.0, min(1.0, quality_score))

    def analyze_prompt(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a single prompt file.
        
        Args:
            file_path: Path to the prompt file
            
        Returns:
            Analysis results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip empty files
            if not content.strip():
                return {"error": "Empty file"}
            
            # Extract sections
            sections = self.extract_sections(content)
            
            # Calculate scores
            readability_score = self.calculate_readability_score(content)
            structure_score = self.calculate_structure_score(sections)
            clarity_score = self.calculate_clarity_score(content)
            
            # Overall quality score (weighted average)
            quality_score = (
                readability_score * 0.3 + 
                structure_score * 0.4 + 
                clarity_score * 0.3
            )
            
            # Analyze keyword density if thorough mode is enabled
            keywords = []
            if self.thorough and NLTK_AVAILABLE:
                keywords = self.analyze_keyword_density(content)
            
            # Generate recommendations
            analysis = {
                "readability_score": readability_score,
                "structure_score": structure_score,
                "clarity_score": clarity_score,
                "quality_score": quality_score
            }
            
            recommendations = self.generate_recommendations(analysis, sections)
            
            # Compile results
            result = {
                "file": file_path,
                "title": sections["title"],
                "scores": {
                    "readability": round(readability_score, 1),
                    "structure": round(structure_score, 1),
                    "clarity": round(clarity_score, 1),
                    "quality": round(quality_score, 1)
                },
                "metadata": {
                    "config_options": sections["metadata"].get("config_options", []),
                    "example_count": len(sections["examples"]),
                    "code_block_count": len(sections["code_blocks"]),
                    "instruction_indicators": sections["metadata"].get("instruction_indicators", 0),
                    "word_count": len(re.findall(r'\b\w+\b', content)),
                    "character_count": len(content)
                }
            }
            
            if keywords:
                result["keywords"] = keywords
                
            if recommendations:
                result["recommendations"] = recommendations
            
            return result
            
        except Exception as e:
            if self.verbose:
                print(f"Error analyzing {file_path}: {str(e)}")
            return {"error": str(e)}
    
    def analyze_all(self) -> Dict[str, Any]:
        """
        Analyze all prompt files in the root directory.
        
        Returns:
            Analysis results for all prompts
        """
        print(f"🔍 Analyzing prompt files in {self.root_dir}...")
        
        # Results storage
        results = {
            "prompts": [],
            "summary": {},
            "categories": {}
        }
        
        # Score statistics
        readability_scores = []
        structure_scores = []
        clarity_scores = []
        quality_scores = []
        
        # Category statistics
        category_stats = defaultdict(lambda: {
            "count": 0, 
            "avg_quality": 0,
            "files": []
        })
        
        # Process all markdown files
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, start=os.getcwd())
                    
                    # Get the category from the directory structure
                    category = os.path.relpath(root, self.root_dir).split(os.path.sep)[0]
                    if category == '.':
                        category = 'root'
                    
                    # Analyze the prompt
                    analysis = self.analyze_prompt(file_path)
                    
                    # Skip files with errors
                    if "error" in analysis:
                        if self.verbose:
                            print(f"❌ Error analyzing {relative_path}: {analysis['error']}")
                        continue
                    
                    # Update the relative path
                    analysis["file"] = relative_path
                    
                    # Add to results
                    results["prompts"].append(analysis)
                    
                    # Update statistics
                    readability_scores.append(analysis["scores"]["readability"])
                    structure_scores.append(analysis["scores"]["structure"])
                    clarity_scores.append(analysis["scores"]["clarity"])
                    quality_scores.append(analysis["scores"]["quality"])
                    
                    # Update category statistics
                    category_stats[category]["count"] += 1
                    category_stats[category]["files"].append({
                        "file": relative_path,
                        "quality": analysis["scores"]["quality"],
                        "title": analysis["title"]
                    })
                    
                    if self.verbose:
                        quality = analysis["scores"]["quality"]
                        if quality >= 80:
                            quality_marker = "🟢"
                        elif quality >= 60:
                            quality_marker = "🟡"
                        else:
                            quality_marker = "🔴"
                        print(f"{quality_marker} {relative_path}: Quality score: {quality:.1f}")
        
        # Calculate statistics
        if quality_scores:
            # Global summary
            results["summary"] = {
                "total_prompts": len(results["prompts"]),
                "avg_readability": round(statistics.mean(readability_scores), 1),
                "avg_structure": round(statistics.mean(structure_scores), 1),
                "avg_clarity": round(statistics.mean(clarity_scores), 1),
                "avg_quality": round(statistics.mean(quality_scores), 1),
                "quality_percentiles": {
                    "25th": round(statistics.quantiles(quality_scores, n=4)[0], 1),
                    "50th": round(statistics.quantiles(quality_scores, n=4)[1], 1),
                    "75th": round(statistics.quantiles(quality_scores, n=4)[2], 1),
                }
            }
            
            # Categories summary
            for category, stats in category_stats.items():
                quality_values = [file["quality"] for file in stats["files"]]
                stats["avg_quality"] = round(statistics.mean(quality_values), 1)
                
                # Get best and worst files in this category
                sorted_files = sorted(stats["files"], key=lambda x: x["quality"], reverse=True)
                stats["best_file"] = sorted_files[0] if sorted_files else None
                stats["worst_file"] = sorted_files[-1] if sorted_files else None
                
                # Keep file list for detailed analysis
                results["categories"][category] = stats
        
        return results
    
    def print_summary(self, results: Dict[str, Any]) -> None:
        """
        Print a summary of the analysis results.
        
        Args:
            results: Analysis results from analyze_all()
        """
        summary = results["summary"]
        prompts = results["prompts"]
        categories = results["categories"]
        
        print("\n📊 Prompt Quality Summary:")
        print(f"Total prompts analyzed: {summary['total_prompts']}")
        print(f"Average quality score: {summary['avg_quality']}/100")
        print(f"  - Readability: {summary['avg_readability']}/100")
        print(f"  - Structure: {summary['avg_structure']}/100")
        print(f"  - Clarity: {summary['avg_clarity']}/100")
        
        # Print quality distribution
        print("\nQuality score distribution:")
        print(f"  - 25% of prompts score below: {summary['quality_percentiles']['25th']}")
        print(f"  - 50% of prompts score below: {summary['quality_percentiles']['50th']} (median)")
        print(f"  - 75% of prompts score below: {summary['quality_percentiles']['75th']}")
        
        # Print category stats
        print("\n📂 Quality by Category:")
        sorted_categories = sorted(
            categories.items(),
            key=lambda x: x[1]["avg_quality"],
            reverse=True
        )
        for category, stats in sorted_categories:
            print(f"{category}: {stats['avg_quality']}/100 (across {stats['count']} prompts)")
        
        # Top 5 highest quality prompts
        print("\n🏆 Top 5 Highest Quality Prompts:")
        sorted_prompts = sorted(prompts, key=lambda x: x["scores"]["quality"], reverse=True)[:5]
        for prompt in sorted_prompts:
            print(f"{prompt['file']}: {prompt['scores']['quality']}/100")
        
        # Bottom 5 prompts (needs improvement)
        print("\n🔧 5 Prompts That Need Improvement:")
        sorted_prompts = sorted(prompts, key=lambda x: x["scores"]["quality"])[:5]
        for prompt in sorted_prompts:
            print(f"{prompt['file']}: {prompt['scores']['quality']}/100")
            if "recommendations" in prompt:
                for i, rec in enumerate(prompt["recommendations"], 1):
                    print(f"  {i}. {rec}")
    
    def export_results(self, results: Dict[str, Any], output_file: str) -> None:
        """
        Export analysis results to a JSON file.
        
        Args:
            results: Analysis results from analyze_all()
            output_file: Path to save results to
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✅ Analysis results exported to {output_file}")


def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(description="Analyze prompt quality and provide recommendations")
    parser.add_argument("--dir", default="prompts", help="Root directory of prompts to analyze")
    parser.add_argument("--file", help="Analyze a specific file instead of the entire directory")
    parser.add_argument("--min-examples", type=int, default=1, help="Minimum recommended examples in a prompt")
    parser.add_argument("--thorough", action="store_true", help="Perform more thorough analysis (slower)")
    parser.add_argument("--export", help="Export results to the specified JSON file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print detailed information")
    args = parser.parse_args()
    
    if not NLTK_AVAILABLE:
        print("⚠️  Warning: NLTK library not found. Some advanced analysis features will be limited.")
        print("   Install with: pip install nltk")
    
    analyzer = PromptAnalyzer(
        root_dir=args.dir,
        verbose=args.verbose,
        min_examples=args.min_examples,
        thorough=args.thorough
    )
    
    if args.file:
        # Analyze a single file
        if not os.path.exists(args.file):
            print(f"❌ Error: File not found: {args.file}")
            return
        
        print(f"🔍 Analyzing {args.file}...")
        analysis = analyzer.analyze_prompt(args.file)
        
        # Pretty print the results
        print("\n📊 Analysis Results:")
        print(f"Title: {analysis.get('title', 'No title found')}")
        print("\nScores:")
        print(f"  - Readability: {analysis['scores']['readability']}/100")
        print(f"  - Structure: {analysis['scores']['structure']}/100")
        print(f"  - Clarity: {analysis['scores']['clarity']}/100")
        print(f"  - Overall Quality: {analysis['scores']['quality']}/100")
        
        print("\nMetadata:")
        print(f"  - Word count: {analysis['metadata']['word_count']}")
        print(f"  - Examples: {analysis['metadata']['example_count']}")
        print(f"  - Code blocks: {analysis['metadata']['code_block_count']}")
        print(f"  - Configuration options: {len(analysis['metadata'].get('config_options', []))}")
        
        if "keywords" in analysis:
            print("\nTop Keywords:")
            for keyword, count in analysis["keywords"]:
                print(f"  - {keyword}: {count} occurrences")
        
        if "recommendations" in analysis:
            print("\n💡 Recommendations for Improvement:")
            for i, rec in enumerate(analysis["recommendations"], 1):
                print(f"{i}. {rec}")
                
        # Export if requested
        if args.export:
            with open(args.export, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2)
            print(f"\n✅ Analysis exported to {args.export}")
    else:
        # Analyze all files
        results = analyzer.analyze_all()
        analyzer.print_summary(results)
        
        if args.export:
            analyzer.export_results(results, args.export)


if __name__ == "__main__":
    main() 