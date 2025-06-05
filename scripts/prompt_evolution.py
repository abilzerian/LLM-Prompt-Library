#!/usr/bin/env python3
"""
Prompt Evolution Script

This script implements an autonomous prompt optimization system that
refines prompts through self-evolution, critique, and iterative improvement.
"""

import os
import re
import argparse
import json
import random
import time
from typing import Dict, List, Any
import statistics
from datetime import datetime

# Try to import optional dependencies for LLM integration
try:
    import openai
    OPENAI_AVAILABLE = True
    # Check if we're using the new OpenAI client (v1.0.0+)
    OPENAI_NEW_CLIENT = hasattr(openai, "OpenAI")
except ImportError:
    OPENAI_AVAILABLE = False
    OPENAI_NEW_CLIENT = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

try:
    from prompt_analyzer import PromptAnalyzer
    PROMPT_ANALYZER_AVAILABLE = True
except ImportError:
    PROMPT_ANALYZER_AVAILABLE = False

class PromptEvolution:
    """Class for evolving and refining prompts through iterative improvement."""
    
    # Critique dimensions to assess and refine prompts
    CRITIQUE_DIMENSIONS = [
        "clarity",
        "specificity",
        "conciseness",
        "completeness",
        "example_quality",
        "context_relevance",
        "instruction_logic",
        "output_guidance"
    ]
    
    # Mutation strategies for generating prompt variations
    MUTATION_STRATEGIES = [
        "add_examples",
        "refine_instructions",
        "restructure_prompt",
        "add_constraints",
        "enhance_clarity",
        "optimize_length",
        "improve_output_format",
        "strengthen_role_definition"
    ]
    
    def __init__(self, 
                 initial_prompt: str = "",
                 task_description: str = "",
                 output_dir: str = "scripts/evolved_prompts",
                 model: str = "gpt-4",
                 population_size: int = 5,
                 max_iterations: int = 10,
                 evaluation_samples: int = 3,
                 verbose: bool = False,
                 api_key: str = None):
        """
        Initialize the prompt evolution system.
        
        Args:
            initial_prompt: Starting prompt to evolve (can be empty for generation from scratch)
            task_description: Description of the task the prompt should accomplish
            output_dir: Directory to save evolved prompts
            model: LLM model to use for evolution
            population_size: Number of prompt variations to maintain per generation
            max_iterations: Maximum number of evolution iterations
            evaluation_samples: Number of test cases to use in evaluation
            verbose: Whether to print detailed progress information
            api_key: API key for LLM service
        """
        # Validate task description
        if not task_description or len(task_description.strip()) < 5:
            raise ValueError("Task description is required and must be descriptive")
            
        self.initial_prompt = initial_prompt
        self.task_description = task_description
        self.output_dir = output_dir
        self.model = model
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.evaluation_samples = evaluation_samples
        self.verbose = verbose
        self.api_key = api_key
        
        # Set up output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Evolution state
        self.current_generation = 0
        self.population = []
        self.best_prompt = None
        self.best_score = 0
        self.evolution_history = []
        
        # Initialize LLM client if available
        self.llm_client = None
        if OPENAI_AVAILABLE and model.startswith("gpt-"):
            if OPENAI_NEW_CLIENT:
                # New OpenAI client (v1.0.0+)
                self.llm_client = openai.OpenAI(api_key=api_key)
            else:
                # Legacy OpenAI client
                openai.api_key = api_key
                self.llm_client = "openai_legacy"
        elif ANTHROPIC_AVAILABLE and model.startswith("claude-"):
            self.llm_client = anthropic.Anthropic(api_key=api_key)
        
        # Initialize PromptAnalyzer if available
        self.prompt_analyzer = None
        if PROMPT_ANALYZER_AVAILABLE:
            self.prompt_analyzer = PromptAnalyzer()
    
    def generate_initial_population(self) -> List[Dict[str, Any]]:
        """
        Generate the initial population of prompts.
        
        Returns:
            List of prompt dictionaries with metadata
        """
        population = []
        
        # If initial prompt is provided, include it
        if self.initial_prompt:
            prompt_dict = {
                "id": "init-0",
                "prompt": self.initial_prompt,
                "score": 0,
                "generation": 0,
                "parent": None,
                "mutations": []
            }
            population.append(prompt_dict)
        
        # Generate additional variations if needed
        while len(population) < self.population_size:
            if self.llm_client:
                # Use LLM to create initial prompts
                new_prompt = self._generate_prompt_with_llm()
            else:
                # Create variations of the initial prompt or generate basics
                if self.initial_prompt:
                    new_prompt = self._create_variation(self.initial_prompt)
                else:
                    new_prompt = self._create_basic_prompt()
            
            prompt_dict = {
                "id": f"init-{len(population)}",
                "prompt": new_prompt,
                "score": 0,
                "generation": 0,
                "parent": None,
                "mutations": ["initial_generation"]
            }
            population.append(prompt_dict)
        
        return population
    
    def _create_basic_prompt(self) -> str:
        """
        Create a basic prompt template based on the task description.
        
        Returns:
            A basic prompt string
        """
        task = self.task_description if self.task_description else "Provide a helpful response"
        
        templates = [
            f"# {task.capitalize()}\n\n"
            f"I want you to {task.lower()}. Please follow these guidelines:\n"
            f"- Be thorough and comprehensive\n"
            f"- Provide step-by-step explanations\n"
            f"- Use clear, concise language\n\n"
            f"```\n"
            f"Examples of good outputs:\n"
            f"1. A well-structured response that addresses the request directly\n"
            f"2. A response that provides sufficient detail and context\n"
            f"```",
            
            f"# Assistant for {task.capitalize()}\n\n"
            f"reset, no quotes, no apologies, be direct\n\n"
            f"Your task is to {task.lower()}. When doing so:\n"
            f"- First, understand what is being asked\n"
            f"- Next, organize your thoughts logically\n"
            f"- Finally, provide a clear and helpful response\n\n"
            f"Example output format:\n"
            f"```\n"
            f"[Main response to the request]\n"
            f"[Additional details as needed]\n"
            f"[Any clarifying information]\n"
            f"```",
            
            f"# {task.capitalize()} Specialist\n\n"
            f"You are a specialist in {task.lower()}. Your goal is to provide expert assistance with this task.\n\n"
            f"Follow these instructions carefully:\n"
            f"1. Analyze the request thoroughly\n"
            f"2. Provide detailed, accurate information\n"
            f"3. Structure your response in a clear, organized manner\n"
            f"4. Include examples where helpful\n\n"
            f"Here's how your response should be structured:\n"
            f"```\n"
            f"[Main information]\n"
            f"[Explanatory details]\n"
            f"[Examples or illustrations]\n"
            f"[Conclusion or summary]\n"
            f"```"
        ]
        
        return random.choice(templates)
    
    def _create_variation(self, prompt: str) -> str:
        """
        Create a variation of an existing prompt.
        
        Args:
            prompt: The prompt to create a variation of
            
        Returns:
            A modified version of the prompt
        """
        # Apply basic mutations
        lines = prompt.split('\n')
        
        # Determine what kind of mutations to apply
        mutations = random.sample(self.MUTATION_STRATEGIES, k=min(3, len(self.MUTATION_STRATEGIES)))
        
        # Apply selected mutations
        for mutation in mutations:
            if mutation == "add_examples" and len(lines) > 5:
                # Add an example somewhere after the middle of the prompt
                insert_pos = random.randint(len(lines) // 2, len(lines) - 1)
                example = "Example: Here is a demonstration of how to effectively perform this task."
                lines.insert(insert_pos, example)
                
            elif mutation == "refine_instructions" and len(lines) > 3:
                # Find instruction-like lines and enhance them
                for i, line in enumerate(lines):
                    if any(marker in line.lower() for marker in ["you should", "please", "follow", "instructions"]):
                        lines[i] = line + " Be thorough and precise."
                        break
                
            elif mutation == "optimize_length" and len(lines) > 10:
                # Remove a random line to make it more concise
                remove_idx = random.randint(2, len(lines) - 2)  # Avoid removing first/last lines
                lines.pop(remove_idx)
                
            elif mutation == "enhance_clarity":
                # Add clarity markers
                lines.append("Note: Be clear, concise, and direct in your response.")
                
            elif mutation == "improve_output_format":
                # Add formatting guidance
                format_guidance = [
                    "```",
                    "Format your output as follows:",
                    "1. Main response",
                    "2. Additional details",
                    "3. Conclusion",
                    "```"
                ]
                lines.extend(format_guidance)
        
        return '\n'.join(lines)
    
    def _generate_prompt_with_llm(self) -> str:
        """
        Generate a new prompt using the LLM.
        
        Returns:
            A new prompt generated by the LLM
        """
        system_message = (
            "You are an expert prompt engineer. Your task is to create an effective prompt "
            "for an AI language model based on the task description provided."
        )
        
        user_message = f"Task: {self.task_description}\n\n"
        
        if self.initial_prompt:
            user_message += (
                f"I already have this initial prompt, but I'd like you to create a completely "
                f"new variation that might be more effective:\n\n{self.initial_prompt}\n\n"
                f"Create a new prompt that accomplishes the same task but uses a different "
                f"approach or structure. Include configuration options, clear instructions, "
                f"and example outputs if relevant."
            )
        else:
            user_message += (
                "Create a comprehensive prompt that will guide an AI to accomplish this task "
                "effectively. Include:\n"
                "1. A clear title\n"
                "2. Configuration options (like 'be concise', 'step by step', etc.)\n"
                "3. Detailed instructions\n"
                "4. Example outputs in a code block\n"
                "5. Any other elements that will make the prompt more effective"
            )
        
        # Simulate LLM response if not available
        if not self.llm_client:
            return self._create_basic_prompt()
        
        # Use appropriate LLM client based on model
        try:
            if isinstance(self.llm_client, openai.OpenAI):
                # New OpenAI client (v1.0.0+)
                response = self.llm_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                return response.choices[0].message.content
            elif self.llm_client == "openai_legacy":
                # Legacy OpenAI client
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                return response.choices[0].message.content
            elif isinstance(self.llm_client, anthropic.Anthropic):
                response = self.llm_client.messages.create(
                    model=self.model,
                    system=system_message,
                    messages=[{"role": "user", "content": user_message}],
                    temperature=0.7,
                    max_tokens=1500
                )
                return response.content[0].text
        except Exception as e:
            print(f"Error generating with LLM: {str(e)}")
            return self._create_basic_prompt()
        
        return self._create_basic_prompt()
    
    def evaluate_prompt(self, prompt: str) -> float:
        """
        Evaluate the quality of a prompt.
        
        Args:
            prompt: The prompt to evaluate
            
        Returns:
            A score between 0 and 1
        """
        if self.llm_client:
            return self._evaluate_with_llm(prompt)
        elif self.prompt_analyzer:
            return self._evaluate_with_analyzer(prompt)
        else:
            return self._simulate_evaluation(prompt)
    
    def _simulate_evaluation(self, prompt: str) -> float:
        """
        Simulate prompt evaluation without using an actual LLM.
        
        Args:
            prompt: The prompt to evaluate
            
        Returns:
            A simulated score between 0 and 1
        """
        score = 0.5  # Base score
        
        # Check for key elements that make a good prompt
        if prompt.strip().startswith("#"):
            score += 0.05  # Has a title
        
        # Check for instruction clarity
        instruction_indicators = ["you should", "your task", "please", "follow these", "instructions"]
        if any(indicator in prompt.lower() for indicator in instruction_indicators):
            score += 0.1  # Clear instructions
        
        # Check for examples
        if "example" in prompt.lower() or "```" in prompt:
            score += 0.1  # Has examples
        
        # Check for structure
        if prompt.count("\n\n") >= 2:
            score += 0.05  # Good paragraph separation
        
        # Check for configuration options
        config_options = ["reset", "no quotes", "be concise", "step by step"]
        config_count = sum(1 for option in config_options if option in prompt.lower())
        score += config_count * 0.02  # Rewards more config options
        
        # Add randomness to simulate different evaluations
        score += random.uniform(-0.1, 0.1)
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, score))
    
    def _evaluate_with_analyzer(self, prompt: str) -> float:
        """
        Evaluate prompt quality using PromptAnalyzer.
        
        Args:
            prompt: The prompt to evaluate
            
        Returns:
            A score between 0 and 1
        """
        return self.prompt_analyzer.evaluate(prompt)
    
    def _evaluate_with_llm(self, prompt: str) -> float:
        """
        Evaluate prompt quality using an LLM.
        
        Args:
            prompt: The prompt to evaluate
            
        Returns:
            A score between 0 and 1
        """
        system_message = (
            "You are an expert prompt evaluator. Your task is to critically assess the quality "
            "of an AI prompt based on clarity, specificity, structure, and potential effectiveness. "
            "You should provide a score between 0 and 100."
        )
        
        user_message = (
            f"Please evaluate the following prompt designed for this task: {self.task_description}\n\n"
            f"PROMPT TO EVALUATE:\n{prompt}\n\n"
            f"Provide your evaluation in this format:\n"
            f"SCORE: [0-100]\n"
            f"REASONING: [Your assessment]"
        )
        
        try:
            if isinstance(self.llm_client, openai.OpenAI):
                # New OpenAI client (v1.0.0+)
                response = self.llm_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                result = response.choices[0].message.content
            elif self.llm_client == "openai_legacy":
                # Legacy OpenAI client
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.3,
                    max_tokens=500
                )
                result = response.choices[0].message.content
            elif isinstance(self.llm_client, anthropic.Anthropic):
                response = self.llm_client.messages.create(
                    model=self.model,
                    system=system_message,
                    messages=[{"role": "user", "content": user_message}],
                    temperature=0.3,
                    max_tokens=500
                )
                result = response.content[0].text
            else:
                return self._simulate_evaluation(prompt)
            
            # Extract score from response with robust error handling
            score_match = re.search(r"SCORE:\s*(\d+)", result)
            if score_match:
                try:
                    score = int(score_match.group(1))
                    # Validate score is in expected range
                    if 0 <= score <= 100:
                        return score / 100.0
                    else:
                        print(f"Warning: LLM returned out-of-range score: {score}")
                        return self._simulate_evaluation(prompt)
                except (ValueError, TypeError):
                    print("Warning: Failed to parse score from LLM response")
                    return self._simulate_evaluation(prompt)
            else:
                print("Warning: Could not find score in LLM response")
                return self._simulate_evaluation(prompt)
                
        except Exception as e:
            print(f"Error evaluating with LLM: {str(e)}")
            return self._simulate_evaluation(prompt)
    
    def generate_mutations(self, prompt_dict: Dict[str, Any], num_mutations: int = 2) -> List[Dict[str, Any]]:
        """
        Generate mutations of a prompt for the next generation.
        
        Args:
            prompt_dict: Prompt dictionary with metadata
            num_mutations: Number of mutations to generate
            
        Returns:
            List of mutated prompt dictionaries
        """
        mutations = []
        prompt = prompt_dict["prompt"]
        
        for i in range(num_mutations):
            if self.llm_client:
                mutated_prompt = self._mutate_with_llm(prompt, prompt_dict["score"])
            else:
                mutated_prompt = self._create_variation(prompt)
            
            # Record which mutation strategies were applied
            applied_mutations = random.sample(self.MUTATION_STRATEGIES, 
                                              k=min(3, len(self.MUTATION_STRATEGIES)))
            
            mutation_dict = {
                "id": f"gen{self.current_generation}-{len(mutations)}",
                "prompt": mutated_prompt,
                "score": 0,  # Will be evaluated later
                "generation": self.current_generation,
                "parent": prompt_dict["id"],
                "mutations": applied_mutations
            }
            
            mutations.append(mutation_dict)
        
        return mutations
    
    def _mutate_with_llm(self, prompt: str, current_score: float) -> str:
        """
        Use an LLM to generate a mutation of a prompt.
        
        Args:
            prompt: The prompt to mutate
            current_score: Current evaluation score of the prompt
            
        Returns:
            A mutated version of the prompt
        """
        system_message = (
            "You are an expert prompt engineer specializing in refining and improving prompts. "
            "Your task is to take a prompt and produce an improved version based on constructive critique."
        )
        
        # Generate critique first
        critique_message = (
            f"Analyze the following prompt designed for this task: {self.task_description}\n\n"
            f"PROMPT TO CRITIQUE:\n{prompt}\n\n"
            f"Identify 3 specific ways this prompt could be improved. Consider clarity, "
            f"structure, specificity, and overall effectiveness."
        )
        
        try:
            critique = ""
            if isinstance(self.llm_client, openai.OpenAI):
                # New OpenAI client (v1.0.0+)
                critique_response = self.llm_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": critique_message}
                    ],
                    temperature=0.5,
                    max_tokens=500
                )
                critique = critique_response.choices[0].message.content
                
                # Now generate the improved prompt
                improvement_message = (
                    f"Based on the following critique, improve this prompt:\n\n"
                    f"ORIGINAL PROMPT:\n{prompt}\n\n"
                    f"CRITIQUE:\n{critique}\n\n"
                    f"Provide a complete, revised version of the prompt that addresses these issues."
                )
                
                improvement_response = self.llm_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": improvement_message}
                    ],
                    temperature=0.5,
                    max_tokens=1500
                )
                
                return improvement_response.choices[0].message.content
                
            elif self.llm_client == "openai_legacy":
                # Legacy OpenAI client
                critique_response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": critique_message}
                    ],
                    temperature=0.5,
                    max_tokens=500
                )
                critique = critique_response.choices[0].message.content
                
                # Now generate the improved prompt
                improvement_message = (
                    f"Based on the following critique, improve this prompt:\n\n"
                    f"ORIGINAL PROMPT:\n{prompt}\n\n"
                    f"CRITIQUE:\n{critique}\n\n"
                    f"Provide a complete, revised version of the prompt that addresses these issues."
                )
                
                improvement_response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": improvement_message}
                    ],
                    temperature=0.5,
                    max_tokens=1500
                )
                
                return improvement_response.choices[0].message.content
                
            elif isinstance(self.llm_client, anthropic.Anthropic):
                critique_response = self.llm_client.messages.create(
                    model=self.model,
                    system=system_message,
                    messages=[{"role": "user", "content": critique_message}],
                    temperature=0.5,
                    max_tokens=500
                )
                critique = critique_response.content[0].text
                
                # Now generate the improved prompt
                improvement_message = (
                    f"Based on the following critique, improve this prompt:\n\n"
                    f"ORIGINAL PROMPT:\n{prompt}\n\n"
                    f"CRITIQUE:\n{critique}\n\n"
                    f"Provide a complete, revised version of the prompt that addresses these issues."
                )
                
                improvement_response = self.llm_client.messages.create(
                    model=self.model,
                    system=system_message,
                    messages=[{"role": "user", "content": improvement_message}],
                    temperature=0.5,
                    max_tokens=1500
                )
                
                return improvement_response.content[0].text
                
            else:
                return self._create_variation(prompt)
                
        except Exception as e:
            print(f"Error mutating with LLM: {str(e)}")
            return self._create_variation(prompt)
    
    def create_next_generation(self) -> List[Dict[str, Any]]:
        """
        Create the next generation of prompts through selection and mutation.
        
        Returns:
            New population of prompts
        """
        # Sort current population by score
        sorted_population = sorted(self.population, key=lambda x: x["score"], reverse=True)
        
        # Select top performers for the next generation (elitism)
        elite_count = max(1, self.population_size // 5)
        next_generation = sorted_population[:elite_count]
        
        # Generate mutations from top performers
        mutation_candidates = sorted_population[:max(2, self.population_size // 2)]
        
        mutations_needed = self.population_size - len(next_generation)
        mutations_per_candidate = max(1, mutations_needed // len(mutation_candidates))
        
        # Generate mutations
        for prompt_dict in mutation_candidates:
            mutations = self.generate_mutations(prompt_dict, mutations_per_candidate)
            next_generation.extend(mutations)
        
        # If we have too many, trim to population size
        if len(next_generation) > self.population_size:
            next_generation = next_generation[:self.population_size]
        
        # If we have too few, add some random new ones
        while len(next_generation) < self.population_size:
            new_prompt = self._generate_prompt_with_llm() if self.llm_client else self._create_basic_prompt()
            
            prompt_dict = {
                "id": f"gen{self.current_generation}-random-{len(next_generation)}",
                "prompt": new_prompt,
                "score": 0,
                "generation": self.current_generation,
                "parent": None,
                "mutations": ["random_introduction"]
            }
            
            next_generation.append(prompt_dict)
        
        return next_generation
    
    def evolve(self) -> Dict[str, Any]:
        """
        Run the evolution process to improve prompts iteratively.
        
        Returns:
            Dictionary with evolution results and statistics
        """
        start_time = time.time()
        
        # Generate initial population
        self.population = self.generate_initial_population()
        
        # Main evolution loop
        for iteration in range(self.max_iterations):
            self.current_generation = iteration + 1
            
            if self.verbose:
                print(f"\n--- Generation {self.current_generation} ---")
            
            # Evaluate current population
            for prompt_dict in self.population:
                if prompt_dict["score"] == 0:  # Only evaluate if not already scored
                    score = self.evaluate_prompt(prompt_dict["prompt"])
                    prompt_dict["score"] = score
                    
                    if self.verbose:
                        print(f"Prompt {prompt_dict['id']}: score = {score:.3f}")
                    
                    # Update best prompt if better
                    if score > self.best_score:
                        self.best_score = score
                        self.best_prompt = prompt_dict.copy()
                        
                        if self.verbose:
                            print(f"New best prompt found! Score: {score:.3f}")
            
            # Record generation stats
            gen_stats = {
                "generation": self.current_generation,
                "avg_score": statistics.mean([p["score"] for p in self.population]),
                "max_score": max([p["score"] for p in self.population]),
                "min_score": min([p["score"] for p in self.population]),
                "best_prompt_id": max(self.population, key=lambda x: x["score"])["id"],
                "timestamp": datetime.now().isoformat()
            }
            
            self.evolution_history.append(gen_stats)
            
            # Check if we've reached maximum iterations
            if self.current_generation >= self.max_iterations:
                break
                
            # Create next generation
            self.population = self.create_next_generation()
        
        # Calculate evolution duration
        duration = time.time() - start_time
        
        # Gather final results
        results = {
            "best_prompt": self.best_prompt,
            "evolution_stats": {
                "generations": self.current_generation,
                "population_size": self.population_size,
                "duration_seconds": duration,
                "starting_score": self.evolution_history[0]["avg_score"] if self.evolution_history else 0,
                "final_score": self.best_score,
                "improvement": self.best_score - (self.evolution_history[0]["avg_score"] if self.evolution_history else 0)
            },
            "history": self.evolution_history
        }
        
        # Save results to output directory
        self.save_results(results)
        
        return results
    
    def save_results(self, results: Dict[str, Any]) -> None:
        """
        Save evolution results to files.
        
        Args:
            results: Evolution results dictionary
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save best prompt to a markdown file
        best_prompt_file = os.path.join(self.output_dir, f"best_prompt_{timestamp}.md")
        with open(best_prompt_file, 'w', encoding='utf-8') as f:
            f.write(results["best_prompt"]["prompt"])
        
        # Save full evolution data to JSON
        evolution_data_file = os.path.join(self.output_dir, f"evolution_data_{timestamp}.json")
        with open(evolution_data_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        # Save a summary report
        report_file = os.path.join(self.output_dir, f"evolution_report_{timestamp}.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Prompt Evolution Report\n\n")
            f.write(f"Task: {self.task_description}\n")
            f.write(f"Model: {self.model}\n")
            f.write(f"Generations: {self.current_generation}\n")
            f.write(f"Population size: {self.population_size}\n")
            f.write(f"Duration: {results['evolution_stats']['duration_seconds']:.2f} seconds\n\n")
            
            f.write("## Evolution Progress\n\n")
            f.write("Generation | Avg Score | Max Score | Min Score\n")
            f.write("----------- | --------- | --------- | ---------\n")
            
            for gen in self.evolution_history:
                f.write(f"{gen['generation']} | {gen['avg_score']:.3f} | {gen['max_score']:.3f} | {gen['min_score']:.3f}\n")
            
            f.write("\n## Best Prompt\n\n")
            f.write(f"Score: {self.best_score:.3f}\n\n")
            f.write("```\n")
            f.write(results["best_prompt"]["prompt"])
            f.write("\n```\n")
        
        if self.verbose:
            print(f"\nResults saved to {self.output_dir}/")
            print(f"Best prompt: {best_prompt_file}")
            print(f"Evolution data: {evolution_data_file}")
            print(f"Report: {report_file}")


def main():
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(description="Evolve and optimize prompts through automated iterations")
    parser.add_argument("--task", required=True, help="Description of the task the prompt should accomplish")
    parser.add_argument("--initial-prompt", default="", help="Path to a file containing the initial prompt (optional)")
    parser.add_argument("--output-dir", default="scripts/evolved_prompts", help="Directory to save evolved prompts")
    parser.add_argument("--model", default="gpt-4", help="LLM model to use (gpt-4, claude-3, etc.)")
    parser.add_argument("--population", type=int, default=5, help="Population size per generation")
    parser.add_argument("--iterations", type=int, default=5, help="Maximum number of evolution iterations")
    parser.add_argument("--api-key", help="API key for LLM service")
    parser.add_argument("--simulate", action="store_true", help="Simulate evolution without using an actual LLM API")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print detailed progress information")
    args = parser.parse_args()
    
    # Load initial prompt if provided
    initial_prompt = ""
    if args.initial_prompt and os.path.exists(args.initial_prompt):
        with open(args.initial_prompt, 'r', encoding='utf-8') as f:
            initial_prompt = f.read()
    
    # Check if required APIs are available
    if not args.simulate:
        if not OPENAI_AVAILABLE and not ANTHROPIC_AVAILABLE:
            print("Warning: Neither OpenAI nor Anthropic libraries are available.")
            print("Install them with: pip install openai anthropic")
            print("Falling back to simulation mode.")
            args.simulate = True
        elif args.model.startswith("gpt") and not OPENAI_AVAILABLE:
            print("Warning: OpenAI library not available but GPT model selected.")
            print("Install with: pip install openai")
            print("Falling back to simulation mode.")
            args.simulate = True
        elif args.model.startswith("claude") and not ANTHROPIC_AVAILABLE:
            print("Warning: Anthropic library not available but Claude model selected.")
            print("Install with: pip install anthropic")
            print("Falling back to simulation mode.")
            args.simulate = True
    
    # Create and run the prompt evolution
    evolution = PromptEvolution(
        initial_prompt=initial_prompt,
        task_description=args.task,
        output_dir=args.output_dir,
        model=args.model,
        population_size=args.population,
        max_iterations=args.iterations,
        verbose=args.verbose,
        api_key=args.api_key
    )
    
    print(f"Starting prompt evolution for task: {args.task}")
    print(f"Using model: {args.model if not args.simulate else 'Simulation mode'}")
    print(f"Population size: {args.population}, Max iterations: {args.iterations}")
    
    results = evolution.evolve()
    
    print("\n=== Evolution Complete ===")
    print(f"Best prompt score: {results['best_prompt']['score']:.3f}")
    print(f"Improvement: {results['evolution_stats']['improvement']:.3f}")
    print(f"Evolved over {results['evolution_stats']['generations']} generations")
    print(f"Results saved to {args.output_dir}/")


if __name__ == "__main__":
    main() 