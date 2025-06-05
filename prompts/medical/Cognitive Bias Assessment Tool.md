# Cognitive Bias Assessment Tool

## Purpose
Detect cognitive biases and propaganda in text.

## Instructions
```markdown
Analyze the following text for cognitive biases, propaganda techniques, and manipulation tactics that exploit System 1 (fast, automatic) thinking to bypass critical analysis.

TEXT TO ANALYZE:
"{}"

CONTEXT ON DUAL PROCESSING MODEL:
Most manipulation techniques exploit System 1 (fast, automatic, emotional, subconscious) thinking to bypass System 2 (slow, deliberate, logical, conscious) analysis. Effective propaganda targets cognitive biases and emotional reactions to prevent critical thinking.

INSTRUCTIONS:
1. Identify ALL cognitive biases and propaganda techniques present in the text from these categories:

   A. SPEED-BASED BIASES (exploiting quick judgments):
      - Action Bias: Preference for doing something over nothing
      - Attentional Bias: Focusing on certain elements while ignoring others
      - Authority Bias: Excessive trust in authority figures
      - Distinction Bias: Viewing options as more distinct when evaluated simultaneously
      - Functional Fixedness: Difficulty thinking beyond conventional uses
      - Fundamental Attribution Error: Underestimating situational influences on behavior
      - Hard-easy Effect: Confidence disproportionate to task difficulty
      - Hyperbolic Discounting: Overvaluing immediate rewards vs long-term benefits
      - IKEA Effect: Overvaluing things we helped create
      - Identifiable Victim Effect: Higher likelihood of helping specific individuals vs groups
      - Illusion of Control: Overestimating personal control over events
      - Incentivization: Working harder when promised rewards
      - Law of the Instrument: Overrelying on familiar tools/methods
      - Less-is-Better Effect: Preference changes based on evaluation method
      - Loss Aversion: Strong preference for avoiding losses over acquiring gains
      - Negativity Bias: Stronger impact of negative events than positive ones
      - Omission Bias: Preferring harm by omission over harm by commission
      - Optimism Bias: Overestimating success probability
      - Ostrich Effect: Avoiding negative information
      - Reactive Devaluation: Devaluing proposals from adversaries
      - Regret Aversion: Making decisions to avoid future regret
      - Self-serving Bias: Attributing success to self and failure to external factors
      - Social Norms: Following others' behavior
      - Status Quo Bias: Preferring current state over change
      - Take-the-best Heuristic: Using single criterion for comparison
      - Sunk Cost Fallacy: Continuing investment despite losses
      - Zero Risk Bias: Seeking complete elimination of risks

   B. AMBIGUITY-BASED BIASES (exploiting unclear situations):
      - Affect Heuristic: Relying on emotions for quick decisions
      - Ambiguity Effect: Preferring known options over unknown ones
      - Anchoring Bias: Over-reliance on first information received
      - Bandwagon Effect: Following majority opinions
      - Barnum Effect: Accepting vague personality descriptions as personally accurate
      - Benjamin Franklin Effect: Increased liking after doing someone a favor
      - Bundling Bias: Undervaluing bundled items
      - Cashless Effect: Increased spending with non-physical payment methods
      - Category Size Bias: Misjudging probabilities based on category size
      - Declinism: Believing past was better than future
      - Dunning-Kruger Effect: Overestimating abilities due to incompetence
      - Einstellung Effect: Past experiences preventing optimal solutions
      - False Consensus Effect: Overestimating agreement with our views
      - Gambler's Fallacy: Misunderstanding probability in random events
      - Halo Effect: Positive impressions in one area influencing opinions in other areas
      - Hot Hand Fallacy: Expecting continued success after streak
      - Illusion of Transparency: Overestimating others' ability to read our feelings
      - Illusion of Validity: Overconfidence in predictions
      - Illusory Correlation: Perceiving relationships between unrelated things
      - Impact Bias: Overestimating emotional reactions to future events
      - In-group Bias: Favoring members of one's own group
      - Just-world Hypothesis: Believing people get what they deserve
      - Look-elsewhere Effect: Continued searching after failing to find significance
      - Mental Accounting: Treating money differently based on source/purpose
      - Mere Exposure Effect: Preference for familiar things
      - Messenger Effect: Judging message based on messenger
      - Motivating Uncertainty Effect: Increased motivation with uncertain rewards
      - Naive Allocation: Preference for spreading resources across options
      - Naive Realism: Believing in objective understanding of reality
      - Noble Edge Effect: Favoring brands showing social concern
      - Normalcy Bias: Assuming nothing bad will happen
      - Pessimism Bias: Expecting failure
      - Planning Fallacy: Underestimating task completion time
      - Pluralistic Ignorance: Misperceiving group consensus
      - Projection Bias: Expecting preferences to remain unchanged
      - Representativeness Heuristic: Using similarity to judge probability
      - Restraint Bias: Overestimating self-control

   C. MEMORY-BASED BIASES (exploiting memory limitations):
      - Availability Heuristic: Overestimating likelihood of recently recalled events
      - Belief Perseverance: Maintaining beliefs despite contradictory evidence
      - Bye-Now Effect: Increased spending after reading "bye"
      - Confirmation Bias: Favoring information confirming existing beliefs
      - Extrinsic Incentive Bias: Misattributing others' motivations as financial
      - Google Effect: Forgetting information easily found online
      - Hindsight Bias: Events seeming predictable only after they occur
      - Lag Effect: Improved retention through spaced repetition
      - Leveling and Sharpening: Exaggerating some details while minimizing others
      - Levels of Processing: Better remembering information with personal significance
      - Nostalgia Effect: Past sentiment influencing present actions
      - Peak-end Rule: Memories differing from experiences
      - Primacy Effect: Better remembering first items in list
      - Priming: Ideas unconsciously prompting related ideas later
      - Recency Effect: Better remembering recent information
      - Response Bias: Giving false survey responses
      - Rosy Retrospection: Viewing past more positively than present
      - Serial Position Effect: Better recall for beginning/end of list
      - Source Confusion: Forgetting origins of memories
      - Spacing Effect: Better retention with spaced learning
      - Telescoping Effect: Distorting time perception of past events

   D. INFORMATION OVERLOAD BIASES (exploiting processing limitations):
      - Base Rate Fallacy: Relying on specific information over statistics
      - Choice Overload: Difficulty choosing with many options
      - Decoy Effect: Changed preferences after introducing third option
      - Disposition Effect: Holding onto losing investments
      - Framing Effect: Decisions changing based on how options are presented
      - Observer Expectancy Effect: Behavior changing when being watched
      - Overjustification Effect: Losing interest after external rewards
      - Salience Bias: Focusing on prominent items/information
      - Sexual Overperception Bias: Misperceiving friendly behavior as sexual interest
      - Spotlight Effect: Overestimating others' attention to us
      - Suggestibility: Being swayed by others
      - Survivorship Bias: Judging groups by only visible successes
      - The Illusion of Explanatory Depth: Overestimating understanding of complex systems
      - The Pygmalion Effect: Performing better under high expectations

   E. TRADITIONAL PROPAGANDA TECHNIQUES:
      - Appeal to Fear: Creating anxiety to influence behavior
      - False Urgency: Creating artificial time pressure
      - Appeal to Authority: Using questionable expertise to establish credibility
      - Black-and-white Fallacy: Presenting complex issues as binary choices
      - Ad Hominem: Attacking character instead of arguments
      - Loaded Language: Using emotionally charged terms
      - Cherry-picking: Selecting favorable data while ignoring contradictions
      - Identity Manipulation: Using group identity to influence thinking
      - Scarcity Tactics: Creating artificial impression of limited resources

2. For each identified bias or technique:
   - Assign a confidence score (0.0-1.0)
   - Note whether it primarily targets System 1 (fast) or System 2 (deliberate) thinking

3. Calculate an overall manipulation score on a scale of 0.0 to 1.0, where:
   - 0.0-0.3: Minimal/no manipulation techniques
   - 0.3-0.6: Moderate use of manipulation techniques
   - 0.6-1.0: Heavy use of manipulation techniques

RETURN YOUR ANALYSIS AS JSON with this structure:
{
  "score": 0.XX,
  "techniques": {
    "technique_name_1": X,
    "technique_name_2": Y
  },
  "has_techniques": true/false,
  "system1_targeting": 0.XX
}

DO NOT include explanations or any text outside the JSON structure.
```
