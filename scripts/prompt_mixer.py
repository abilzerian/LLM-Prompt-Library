#!/usr/bin/env python3
"""
Prompt Mixer Tool

This script allows combining elements from different prompt files
to create new prompts with mixed elements.
"""

import os
import re
import argparse
import random
import datetime
from typing import Dict, Optional


class PromptElement:
    """Class representing a component of a prompt."""
    
    def __init__(self, element_type: str, content: str, source_file: str):
        self.element_type = element_type
        self.content = content
        self.source_file = source_file
    
    def __str__(self):
        return f"{self.element_type} from {self.source_file}"


class PromptParser:
    """Class to parse prompt files and extract their elements."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    def parse_file(self, file_path: str) -> Dict[str, PromptElement]:
        """
        Parse a prompt file and extract its elements.
        
        Returns:
            Dict with keys: 'title', 'config', 'instructions', 'examples', 'output_guidance'
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            elements = {}
            relative_path = os.path.relpath(file_path, start=os.getcwd())
            
            # Extract title (first line starting with # )
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if title_match:
                elements['title'] = PromptElement('title', title_match.group(1), relative_path)
            else:
                # Try to find any heading that might serve as a title
                heading_match = re.search(r'^#+\s+(.+)$', content, re.MULTILINE)
                if heading_match:
                    elements['title'] = PromptElement('title', heading_match.group(1), relative_path)
                else:
                    # Use filename as title if no heading found
                    filename = os.path.basename(file_path)
                    filename_title = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
                    elements['title'] = PromptElement('title', filename_title, relative_path)
            
            # Extract code blocks
            code_blocks = re.findall(r'```.*?\n(.*?)```', content, re.DOTALL)
            if code_blocks:
                main_block = code_blocks[0]
                
                # Extract configuration (lines with `command`)
                config_lines = re.findall(r'`[^`]+`', main_block)
                if config_lines:
                    elements['config'] = PromptElement('config', 
                                                      '\n'.join(config_lines), 
                                                      relative_path)
                else:
                    # Add default configs if none found
                    elements['config'] = PromptElement('config', 
                                                    '`reset`\n`no quotes`\n`no explanations`\n`no prompt`\n`no self-reference`', 
                                                    relative_path)
                
                # Extract instructions (text after config and before examples)
                # This is a simplification; actual logic would be more complex
                instruction_patterns = [
                    r'(?:Your task is|You will|Your job is|You are).*?(?=###|$)',
                    r'(?:I want you to|Please).*?(?=###|$)',
                    r'(?:Act as|You should).*?(?=###|$)'
                ]
                
                found_instructions = False
                for pattern in instruction_patterns:
                    instructions_match = re.search(pattern, main_block, re.DOTALL | re.IGNORECASE)
                    if instructions_match:
                        elements['instructions'] = PromptElement('instructions', 
                                                              instructions_match.group(0).strip(), 
                                                              relative_path)
                        found_instructions = True
                        break
                
                if not found_instructions:
                    # If no clear instructions, use the first paragraph as instructions
                    paragraphs = re.split(r'\n\s*\n', main_block)
                    if paragraphs:
                        # Skip config lines if they're in the first paragraph
                        first_para = paragraphs[0]
                        if not all(line.strip().startswith('`') for line in first_para.strip().split('\n')):
                            elements['instructions'] = PromptElement('instructions', first_para.strip(), relative_path)
                
                # Extract examples (sections starting with ###)
                examples_match = re.search(r'###.*?Example.*?\n(.*?)(?=###|$)', main_block, re.DOTALL | re.IGNORECASE)
                if examples_match:
                    elements['examples'] = PromptElement('examples', 
                                                        examples_match.group(1).strip(), 
                                                        relative_path)
                
                # Extract output guidance (text at the end, often about how to respond)
                output_patterns = [
                    r'(?:Once you have|When you are ready|Respond with).*?$',
                    r'(?:Your response should|Please format).*?$',
                    r'(?:In your answer|Please provide).*?$'
                ]
                
                found_output = False
                for pattern in output_patterns:
                    output_match = re.search(pattern, main_block, re.DOTALL | re.IGNORECASE)
                    if output_match:
                        elements['output_guidance'] = PromptElement('output_guidance', 
                                                                output_match.group(0).strip(), 
                                                                relative_path)
                        found_output = True
                        break
                        
                if not found_output and 'instructions' in elements:
                    # Add default output guidance if none found
                    elements['output_guidance'] = PromptElement('output_guidance', 
                                                             "Once you have fully understood these instructions, respond with 'I understand' and wait for my input.", 
                                                             relative_path)
            else:
                # Handle files without code blocks
                # Use the whole content as instructions
                if len(content.strip()) > 10:  # Only if there's meaningful content
                    elements['instructions'] = PromptElement('instructions', content.strip(), relative_path)
                    
                    # Add default configs and output guidance
                    elements['config'] = PromptElement('config', 
                                                    '`reset`\n`no quotes`\n`no explanations`\n`no prompt`\n`no self-reference`', 
                                                    'default')
                    
                    elements['output_guidance'] = PromptElement('output_guidance', 
                                                             "Once you have fully understood these instructions, respond with 'I understand' and wait for my input.", 
                                                             'default')
            
            if self.verbose:
                print(f"Parsed {relative_path}, found elements: {', '.join(elements.keys())}")
            
            return elements
        
        except Exception as e:
            if self.verbose:
                print(f"Error parsing {file_path}: {str(e)}")
            return {}


class PromptMixer:
    """Class to mix elements from different prompt files."""
    
    def __init__(self, root_dir: str = "prompts", output_dir: str = "scripts/mixed_prompts", verbose: bool = False):
        """Initialize the mixer with the root directory of prompts."""
        self.root_dir = root_dir
        self.output_dir = output_dir
        self.verbose = verbose
        self.parser = PromptParser(verbose=verbose)
        self.elements_by_type = {
            'title': [],
            'config': [],
            'instructions': [],
            'examples': [],
            'output_guidance': []
        }
    
    def scan_prompts(self) -> None:
        """Scan all prompt files and extract their elements."""
        print(f"🔍 Scanning prompt files in {self.root_dir}...")
        
        # Recursively find all markdown files
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    elements = self.parser.parse_file(file_path)
                    
                    # Add parsed elements to our collection
                    for element_type, element in elements.items():
                        self.elements_by_type[element_type].append(element)
        
        # Print summary
        print("\n📊 Scan Summary:")
        for element_type, elements in self.elements_by_type.items():
            print(f"{element_type}: {len(elements)} elements found")
    
    def create_mixed_prompt(self, 
                           title: Optional[str] = None,
                           use_config_from: Optional[str] = None,
                           use_instructions_from: Optional[str] = None,
                           use_examples_from: Optional[str] = None,
                           use_output_from: Optional[str] = None,
                           output_file: Optional[str] = None) -> str:
        """
        Create a new prompt by mixing elements from different sources.
        
        Parameters:
            title: Custom title for the new prompt (if None, pick randomly)
            use_config_from: Source file for configuration (if None, pick randomly)
            use_instructions_from: Source file for instructions (if None, pick randomly)
            use_examples_from: Source file for examples (if None, pick randomly)
            use_output_from: Source file for output guidance (if None, pick randomly)
            output_file: Path to save the mixed prompt (if None, generate one)
        
        Returns:
            Path to the created prompt file
        """
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Either use provided title or generate one
        if title is None:
            if self.elements_by_type['title']:
                title_element = random.choice(self.elements_by_type['title'])
                title = f"Mixed: {title_element.content}"
            else:
                title = f"Mixed Prompt {datetime.datetime.now().strftime('%Y-%m-%d')}"
        
        # Map parameter names to element types
        source_mapping = {
            'config': use_config_from,
            'instructions': use_instructions_from,
            'examples': use_examples_from,
            'output_guidance': use_output_from
        }
        
        # Select elements based on provided sources or randomly
        selected_elements = {}
        
        for element_type, source_var in source_mapping.items():
            elements = self.elements_by_type[element_type]
            
            if not elements:
                # If we don't have any of this element type, add default ones for essentials
                if element_type == 'config':
                    selected_elements[element_type] = PromptElement('config', 
                                                                '`reset`\n`no quotes`\n`no explanations`\n`no prompt`\n`no self-reference`',
                                                                'default')
                elif element_type == 'output_guidance':
                    selected_elements[element_type] = PromptElement('output_guidance',
                                                                 "Once you have fully understood these instructions, respond with 'I understand' and wait for my input.",
                                                                 'default')
                continue
                
            if source_var is not None:
                # Find element from specified source
                found = False
                for element in elements:
                    if source_var in element.source_file:
                        selected_elements[element_type] = element
                        found = True
                        break
                
                if not found:
                    if self.verbose:
                        print(f"⚠️ Could not find {element_type} from {source_var}, using random selection")
                    if elements:
                        selected_elements[element_type] = random.choice(elements)
            else:
                # Random selection
                selected_elements[element_type] = random.choice(elements)
        
        # Ensure we have instructions
        if 'instructions' not in selected_elements or not selected_elements['instructions'].content.strip():
            print("⚠️ No valid instructions found. This is a required element. Exiting.")
            return None
        
        # Build the mixed prompt content
        content = f"# {title}\n\n```markdown\n"
        
        if 'config' in selected_elements:
            content += f"{selected_elements['config'].content}\n\n"
        
        if 'instructions' in selected_elements:
            content += f"{selected_elements['instructions'].content}\n\n"
        
        if 'examples' in selected_elements:
            content += f"### Example\n{selected_elements['examples'].content}\n\n"
        
        if 'output_guidance' in selected_elements:
            content += f"{selected_elements['output_guidance'].content}\n"
        
        content += "```\n"
        
        # Add a comment with sources
        content += "\n<!-- Mixed from:\n"
        for element_type, element in selected_elements.items():
            content += f"{element_type}: {element.source_file}\n"
        content += "-->\n"
        
        # Determine output file path
        if output_file is None:
            sanitized_title = re.sub(r'[^\w\-]', '_', title)
            output_file = os.path.join(self.output_dir, f"{sanitized_title}.md")
        elif not output_file.startswith(self.output_dir):
            # If output_file doesn't already include the output_dir, add it
            output_file = os.path.join(self.output_dir, os.path.basename(output_file))
        
        # Write the content to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created mixed prompt: {output_file}")
        return output_file


def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(description="Mix and match elements from different prompt files")
    parser.add_argument("--dir", default="prompts", help="Root directory of prompts to scan")
    parser.add_argument("--output", default="scripts/mixed_prompts", help="Directory to save mixed prompts")
    parser.add_argument("--title", help="Custom title for the mixed prompt")
    parser.add_argument("--config-from", help="Source file for configuration section")
    parser.add_argument("--instructions-from", help="Source file for instructions section")
    parser.add_argument("--examples-from", help="Source file for examples section")
    parser.add_argument("--output-from", help="Source file for output guidance section")
    parser.add_argument("--output-file", help="Custom filename for the output prompt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print detailed information")
    args = parser.parse_args()
    
    mixer = PromptMixer(root_dir=args.dir, output_dir=args.output, verbose=args.verbose)
    mixer.scan_prompts()
    
    mixer.create_mixed_prompt(
        title=args.title,
        use_config_from=args.config_from,
        use_instructions_from=args.instructions_from,
        use_examples_from=args.examples_from,
        use_output_from=args.output_from,
        output_file=args.output_file
    )


if __name__ == "__main__":
    main() 