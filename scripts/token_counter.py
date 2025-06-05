#!/usr/bin/env python3
"""
Token Counter Script

This script analyzes prompt files and counts tokens using various tokenization methods.
It can generate reports on token usage across all prompts or analyze individual files.
"""

import os
import re
import argparse
import sys
import json
from typing import Dict
from collections import defaultdict

# Check if tiktoken is available (for OpenAI models)
TIKTOKEN_AVAILABLE = False
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    pass

class TokenCounter:
    """Class for counting tokens in prompt files."""
    
    def __init__(self, 
                 root_dir: str = "prompts", 
                 tokenizer: str = "gpt-3.5-turbo", 
                 verbose: bool = False,
                 include_code_blocks: bool = True,
                 include_markdown: bool = False):
        """
        Initialize the token counter.
        
        Args:
            root_dir: Root directory containing prompt files
            tokenizer: Tokenizer model to use ('gpt-3.5-turbo', 'gpt-4', 'claude', etc.)
            verbose: Whether to print detailed information
            include_code_blocks: Whether to include code blocks in token counts
            include_markdown: Whether to include markdown formatting in token counts
        """
        self.root_dir = root_dir
        self.tokenizer = tokenizer
        self.verbose = verbose
        self.include_code_blocks = include_code_blocks
        self.include_markdown = include_markdown
        
        # Initialize tokenizer
        self.tiktoken_encoder = None
        if TIKTOKEN_AVAILABLE and tokenizer.startswith('gpt'):
            try:
                self.tiktoken_encoder = tiktoken.encoding_for_model(tokenizer)
            except KeyError:
                # Fall back to cl100k_base for unknown models
                self.tiktoken_encoder = tiktoken.get_encoding("cl100k_base")
        
        # Stats
        self.total_files = 0
        self.total_tokens = 0
        self.file_tokens = {}
        self.category_tokens = defaultdict(int)
        self.category_files = defaultdict(int)
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in the given text using the specified tokenizer.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        if self.tiktoken_encoder:
            # Use tiktoken for OpenAI models
            return len(self.tiktoken_encoder.encode(text))
        else:
            # Simple fallback tokenization (word-based)
            # This is a very rough approximation and will be inaccurate compared to model-specific tokenizers
            return len(text.split())
    
    def extract_content(self, file_content: str) -> str:
        """
        Extract the relevant content from a file for token counting.
        
        Args:
            file_content: Full content of the file
            
        Returns:
            Content to be counted
        """
        # Extract the main prompt content
        if not self.include_markdown:
            # Remove markdown formatting like headers, lists, etc.
            content = re.sub(r'^#+\s+.*$', '', file_content, flags=re.MULTILINE)  # Headers
            content = re.sub(r'^[*-]\s+.*$', '', content, flags=re.MULTILINE)     # List items
            content = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\1', content)       # Bold/italic
        else:
            content = file_content
        
        # Handle code blocks
        if not self.include_code_blocks:
            # Remove code blocks
            content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        
        return content.strip()
    
    def count_file_tokens(self, file_path: str) -> int:
        """
        Count tokens in a single file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Number of tokens in the file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract the relevant content
            extracted_content = self.extract_content(content)
            
            # Count tokens
            token_count = self.count_tokens(extracted_content)
            
            return token_count
        except Exception as e:
            if self.verbose:
                print(f"Error processing {file_path}: {str(e)}")
            return 0
    
    def analyze_all(self) -> Dict[str, Dict[str, int]]:
        """
        Analyze all prompt files and generate token count statistics.
        
        Returns:
            Dictionary containing token statistics
        """
        print(f"📊 Analyzing prompt files in {self.root_dir} using {self.tokenizer} tokenizer...")
        
        # Recursively process all markdown files
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, start=os.getcwd())
                    
                    # Get the category from the directory structure
                    category = os.path.relpath(root, self.root_dir).split(os.path.sep)[0]
                    if category == '.':
                        category = 'root'
                    
                    # Count tokens
                    token_count = self.count_file_tokens(file_path)
                    
                    # Update stats
                    self.total_files += 1
                    self.total_tokens += token_count
                    self.file_tokens[relative_path] = token_count
                    self.category_tokens[category] += token_count
                    self.category_files[category] += 1
                    
                    if self.verbose:
                        print(f"📄 {relative_path}: {token_count} tokens")
        
        # Prepare results
        results = {
            'total': {
                'files': self.total_files,
                'tokens': self.total_tokens,
                'avg_tokens_per_file': self.total_tokens / self.total_files if self.total_files > 0 else 0
            },
            'by_category': {
                category: {
                    'files': self.category_files[category],
                    'tokens': token_count,
                    'avg_tokens_per_file': token_count / self.category_files[category]
                }
                for category, token_count in self.category_tokens.items()
            },
            'by_file': self.file_tokens
        }
        
        return results
    
    def print_summary(self, results: Dict[str, Dict[str, int]]) -> None:
        """
        Print a summary of token usage.
        
        Args:
            results: Results from analyze_all()
        """
        print("\n📊 Token Usage Summary:")
        print(f"Total files analyzed: {results['total']['files']}")
        print(f"Total tokens: {results['total']['tokens']:,}")
        print(f"Average tokens per file: {results['total']['avg_tokens_per_file']:.1f}")
        
        print("\n📂 Token Usage by Category:")
        # Sort categories by token count (descending)
        sorted_categories = sorted(
            results['by_category'].items(),
            key=lambda x: x[1]['tokens'],
            reverse=True
        )
        for category, stats in sorted_categories:
            print(f"{category}: {stats['tokens']:,} tokens across {stats['files']} files (avg: {stats['avg_tokens_per_file']:.1f})")
        
        # Find top token-heavy files
        print("\n🔝 Top 10 Token-Heavy Files:")
        sorted_files = sorted(
            results['by_file'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        for file_path, token_count in sorted_files:
            print(f"{file_path}: {token_count:,} tokens")
        
        # Provide cost estimates for OpenAI models
        if self.tokenizer.startswith('gpt'):
            print("\n💰 Estimated API Costs (per prompt):")
            
            # Approximate costs per 1K tokens (as of early 2024)
            if 'gpt-4' in self.tokenizer:
                if 'turbo' in self.tokenizer:
                    input_cost = 0.01
                    output_cost = 0.03
                else:
                    input_cost = 0.03
                    output_cost = 0.06
            else:  # gpt-3.5
                input_cost = 0.0015
                output_cost = 0.002
            
            avg_tokens = results['total']['avg_tokens_per_file']
            print(f"Average prompt cost ({self.tokenizer}):")
            print(f"  Input only: ${(avg_tokens * input_cost / 1000):.4f}")
            print(f"  With ~500 token response: ${(avg_tokens * input_cost / 1000) + (500 * output_cost / 1000):.4f}")
    
    def export_results(self, results: Dict[str, Dict[str, int]], output_file: str) -> None:
        """
        Export results to a JSON file.
        
        Args:
            results: Results from analyze_all()
            output_file: Path to save results to
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✅ Results exported to {output_file}")


def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(description="Count tokens in prompt files")
    parser.add_argument("--dir", default="prompts", help="Root directory of prompts to analyze")
    parser.add_argument("--tokenizer", default="gpt-3.5-turbo", 
                       help="Tokenizer to use (gpt-3.5-turbo, gpt-4, etc.)")
    parser.add_argument("--file", help="Analyze a specific file instead of the entire directory")
    parser.add_argument("--skip-code-blocks", action="store_true", 
                       help="Skip code blocks when counting tokens")
    parser.add_argument("--include-markdown", action="store_true", 
                       help="Include markdown formatting in token counts")
    parser.add_argument("--export", help="Export results to the specified JSON file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print detailed information")
    args = parser.parse_args()
    
    # Check if tiktoken is available
    if not TIKTOKEN_AVAILABLE and args.tokenizer.startswith('gpt'):
        print("⚠️  Warning: tiktoken library not found. Results will be less accurate.")
        print("   Install with: pip install tiktoken")
    
    counter = TokenCounter(
        root_dir=args.dir,
        tokenizer=args.tokenizer,
        verbose=args.verbose,
        include_code_blocks=not args.skip_code_blocks,
        include_markdown=args.include_markdown
    )
    
    if args.file:
        # Analyze a single file
        if not os.path.exists(args.file):
            print(f"❌ Error: File not found: {args.file}")
            sys.exit(1)
        
        token_count = counter.count_file_tokens(args.file)
        print(f"📄 {args.file}: {token_count:,} tokens")
        
        # Provide cost estimates
        if args.tokenizer.startswith('gpt'):
            # Approximate costs per 1K tokens (as of early 2024)
            if 'gpt-4' in args.tokenizer:
                if 'turbo' in args.tokenizer:
                    input_cost = 0.01
                    output_cost = 0.03
                else:
                    input_cost = 0.03
                    output_cost = 0.06
            else:  # gpt-3.5
                input_cost = 0.0015
                output_cost = 0.002
            
            print(f"\n💰 Estimated API Costs ({args.tokenizer}):")
            print(f"  Input only: ${(token_count * input_cost / 1000):.4f}")
            print(f"  With ~500 token response: ${(token_count * input_cost / 1000) + (500 * output_cost / 1000):.4f}")
    else:
        # Analyze all files
        results = counter.analyze_all()
        counter.print_summary(results)
        
        if args.export:
            counter.export_results(results, args.export)


if __name__ == "__main__":
    main() 