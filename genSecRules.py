import os
import sys
from dotenv import load_dotenv
import openai
import PyPDF2
from datetime import datetime

# Check if PDF file path is provided as first argument
if len(sys.argv) < 2:
    print("Error: Please provide a PDF file path as the first argument")
    print("Usage: python genSecRules.py <path_to_pdf>")
    sys.exit(1)

pdf_file = sys.argv[1]

# Check if PDF file exists
if not os.path.exists(pdf_file):
    print(f"Error: PDF file '{pdf_file}' not found")
    sys.exit(1)

# Read PDF content
pdf_content = ""
try:
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            pdf_content += page.extract_text() + "\n"
except Exception as e:
    print(f"Error reading PDF: {e}")
    sys.exit(1)

# Read the function template from file and store as a string
with open('function_template.yaml', 'r') as f:
    function_template = f.read()

# Load .env into environment
load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("NAVIGATOR_TOOLKIT_API_KEY"),
    base_url="https://api.ai.it.ufl.edu"
)

# Create comprehensive prompt
instruction_prompt = """You are a security expert. Analyze the provided documentation and generate security rules in the specified YAML function template format. 
The security rules should be:
- Comprehensive and cover all important security aspects from the documentation
- Properly structured according to the function template
- Include appropriate constraints, preconditions, and validations
- Focus on critical security parameters and edge cases"""

prompt_content = f"""DOCUMENTATION:
{pdf_content}

FUNCTION TEMPLATE FORMAT (use this structure for your response):
{function_template}

INSTRUCTION:
{instruction_prompt}

Please generate detailed security rules based on the documentation provided."""

response = client.chat.completions.create(
    model="gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": prompt_content
        }
    ]
)

# Get response content
response_text = response.choices[0].message.content

# Print response
print(response_text)

# Save response to text file with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"results/security_rules_{timestamp}.txt"

# Create results directory if it doesn't exist
os.makedirs('results', exist_ok=True)

try:
    with open(output_filename, 'w') as f:
        f.write("PDF Documentation File: " + pdf_file + "\n")
        f.write("Generated at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        f.write("="*80 + "\n\n")
        f.write(response_text)
    print(f"\nResponse saved to: {output_filename}")
except Exception as e:
    print(f"Error saving response: {e}")
