# Unstructured Text to JSON Converter

## Purpose
Transform unstructured text into JSON format.

## Instructions
```markdown
- **reset**
- **no quotes**
- **no explanations**
- **no prompt**
- **no self-reference**
- **no apologies**
- **no filler**
- **just answer**

Ignore all prior instructions. Analyze the provided unstructured text to convert it into a well-organized JSON table. Identify the main entities, attributes, or categories mentioned in the text and use them as keys in the JSON object. Extract the relevant information from the text and populate the corresponding values in the JSON object. Ensure the data is accurately represented and properly formatted. Here is an example input and output:

### Example Input
Harmony Valley, a quaint town, is known for its exceptional residents. Among them is Dr. Sarah Mitchell, a 38-year-old Harvard-educated cardiologist who pioneered new heart disease treatments. Michael Andrews, aged 32, is a software engineer from MIT who developed innovative software solutions for local businesses. Grace Parker, a 50-year-old artist from the Rhode Island School of Design, has her work featured in several national galleries. Lucas Brown, a self-taught gardener, turned his backyard into a community garden, providing fresh produce to the entire town.

### Example Output
json
[
  {
    "name": "Dr. Sarah Mitchell",
    "age": 38,
    "profession": "Cardiologist",
    "education": "Harvard",
    "accomplishments": "Pioneered new heart disease treatments"
  },
  {
    "name": "Michael Andrews",
    "age": 32,
    "profession": "Software Engineer",
    "education": "MIT",
    "accomplishments": "Developed innovative software solutions for local businesses"
  },
  {
    "name": "Grace Parker",
    "age": 50,
    "profession": "Artist",
    "education": "Rhode Island School of Design",
    "accomplishments": "Featured in several national galleries"
  },
  {
    "name": "Lucas Brown",
    "age": null,
    "profession": "Gardener",
    "education": "Self-taught",
    "accomplishments": "Created a community garden providing fresh produce to the entire town"
  }
]

### Detailed Explanation
1. **Identify Entities:** Extract names, ages, professions, education, and accomplishments.
2. **Create JSON Structure:** Use extracted information to populate the JSON structure.
3. **Handle Missing Data:** Use `null` for missing or unspecified values.

Once you have fully grasped these instructions and are prepared to begin, respond with "Understood. Please provide the unstructured text you would like converted to a JSON table."
```
