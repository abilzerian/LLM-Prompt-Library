#!/usr/bin/env python3
"""
Prompt Validator Script

This script validates the format and contents of prompt files in the LLM-Prompt-Library.
It checks for required elements like titles, configuration blocks, instructions, etc.
"""

import os
import re
import argparse
import sys


class PromptValidator:
    def __init__(self, root_dir: str = "prompts", verbose: bool = False, strict: bool = False):
        """Initialize the validator with the root directory of prompts."""
        self.root_dir = root_dir
        self.verbose = verbose
        self.strict = strict  # Strict mode applies more rigorous validation
        self.valid_files = 0
        self.invalid_files = 0
        self.issues = []
        self.warnings = []

    def validate_all(self) -> bool:
        """Validate all prompt files in the repository."""
        print(f"🔍 Validating prompt files in {self.root_dir}...")
        
        # Recursively find all markdown files
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    self._validate_file(file_path)
        
        # Print summary
        print("\n📊 Validation Summary:")
        print(f"Total files checked: {self.valid_files + self.invalid_files}")
        print(f"Valid files: {self.valid_files}")
        print(f"Invalid files: {self.invalid_files}")
        
        if self.warnings:
            print("\n⚠️ Warnings (not failures):")
            for warning in self.warnings:
                print(f"- {warning}")
        
        if self.invalid_files > 0:
            print("\n❌ Issues found:")
            for issue in self.issues:
                print(f"- {issue}")
            return False
        
        print("\n✅ All prompt files are valid!")
        return True

    def _validate_file(self, file_path: str) -> bool:
        """Validate a single prompt file."""
        relative_path = os.path.relpath(file_path, start=os.getcwd())
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check basic structure
            is_valid = True
            file_issues = []
            file_warnings = []
            
            # Check for title (# Title at the beginning or within first 5 lines)
            title_match = re.search(r'^# .+', content, re.MULTILINE)
            if not title_match:
                # Check first 5 lines for a title-like line
                first_5_lines = content.split('\n')[:5]
                found_title = False
                for line in first_5_lines:
                    if line.startswith('#') and len(line) > 2:
                        found_title = True
                        break
                
                if not found_title:
                    if self.strict:
                        file_issues.append("Missing title (should start with '# Title')")
                        is_valid = False
                    else:
                        file_warnings.append("Missing standard title format (should start with '# Title')")
            
            # Check for some form of markdown code block, be more lenient
            code_block_found = False
            
            # Check for standard code blocks with triple backticks
            if re.search(r'```[\w]*\n', content):
                code_block_found = True
            
            # Also check for alternative code formatting (e.g., indented blocks)
            if not code_block_found:
                # Check for indented code blocks (4 spaces or tab)
                if re.search(r'(?:^    |\t).+', content, re.MULTILINE):
                    code_block_found = True
                # Check for any instruction-like content anywhere in the file
                elif re.search(r'(your task is|you will|your job is|you are|i want you to|please act as)', 
                              content, re.IGNORECASE):
                    code_block_found = True
            
            if not code_block_found:
                # Try to find other indicators of a prompt
                prompt_indicators = [
                    r'prompt:',
                    r'you will:',
                    r'your task is',
                    r'your job is',
                    r'act as',
                    r'i want you to'
                ]
                found_indicator = False
                for indicator in prompt_indicators:
                    if re.search(indicator, content, re.IGNORECASE):
                        found_indicator = True
                        break
                
                if not found_indicator:
                    if self.strict:
                        file_issues.append("Missing code block and no clear prompt indicators")
                        is_valid = False
                    else:
                        file_warnings.append("No clear code or instruction format detected")
            
            # Extract code block content for further analysis if we have triple backticks
            code_blocks = re.findall(r'```.*?\n(.*?)```', content, re.DOTALL)
            if code_blocks:
                main_block = code_blocks[0]
                
                # Check for configuration options - only in strict mode
                if self.strict:
                    config_patterns = [
                        r'`reset`', 
                        r'`no quotes`',
                        r'`no explanations`',
                        r'`no prompt`',
                        r'`no self-reference`',
                        r'`no apologies`',
                        r'`no filler`',
                        r'`just answer`'
                    ]
                    
                    found_configs = 0
                    for pattern in config_patterns:
                        if re.search(pattern, main_block, re.IGNORECASE):
                            found_configs += 1
                    
                    if found_configs < 3:  # Require at least 3 configuration options in strict mode
                        file_warnings.append(f"Few configuration options (found {found_configs}, recommended at least 3)")
                
                # Check for instructions - more lenient
                instruction_patterns = [
                    r'your task is', 
                    r'you will', 
                    r'your job is', 
                    r'you are',
                    r'i want you to',
                    r'please',
                    r'act as',
                    r'provide',
                    r'analyze',
                    r'summarize',
                    r'explain'
                ]
                
                found_instructions = False
                for pattern in instruction_patterns:
                    if re.search(pattern, main_block, re.IGNORECASE):
                        found_instructions = True
                        break
                
                if not found_instructions and self.strict:
                    file_warnings.append("No clear instruction patterns detected")
                
                # Check for basic content length
                if len(main_block.strip()) < 50:  # Very minimal length requirement
                    file_issues.append(f"Prompt content is too short ({len(main_block.strip())} chars)")
                    is_valid = False
            # If no code blocks with triple backticks but we consider it valid, check the whole content
            elif code_block_found and len(content.strip()) < 50:
                file_issues.append(f"Prompt content is too short ({len(content.strip())} chars)")
                is_valid = False
            
            # Update counters
            if is_valid:
                self.valid_files += 1
                if file_warnings:
                    warning_str = f"{relative_path}: {', '.join(file_warnings)}"
                    self.warnings.append(warning_str)
                
                if self.verbose:
                    if file_warnings:
                        print(f"⚠️ {relative_path}: Valid with warnings")
                    else:
                        print(f"✅ {relative_path}: Valid")
            else:
                self.invalid_files += 1
                issue_str = f"{relative_path}: {', '.join(file_issues)}"
                self.issues.append(issue_str)
                if self.verbose:
                    print(f"❌ {issue_str}")
            
            return is_valid
            
        except Exception as e:
            self.invalid_files += 1
            issue_str = f"{relative_path}: Error reading/parsing file - {str(e)}"
            self.issues.append(issue_str)
            if self.verbose:
                print(f"❌ {issue_str}")
            return False


def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(description="Validate prompt files in the LLM-Prompt-Library")
    parser.add_argument("--dir", default="prompts", help="Root directory of prompts to validate")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print detailed information")
    parser.add_argument("-s", "--strict", action="store_true", help="Use strict validation criteria")
    args = parser.parse_args()
    
    validator = PromptValidator(root_dir=args.dir, verbose=args.verbose, strict=args.strict)
    is_valid = validator.validate_all()
    
    # Exit with appropriate code for CI/CD integration
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main() 