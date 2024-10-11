# pip install python-dotenv
# pip install together==1.2.6 e2b-code-interpreter==0.0.10 dotenv==1.0.0

import os
from dotenv import load_dotenv
from together import Together
from docx import Document
import json

# Load environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Initialize Together client
client = Together(api_key=TOGETHER_API_KEY)

# Function to extract text from Word document
def extract_text_from_word(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

# Specify the folder containing the Word documents
folder_path = "./Docu"

# List all files in the folder and filter for .docx files
word_files = [f for f in os.listdir(folder_path) if f.endswith(".docx")]

# Count how many .docx files are in the folder
num_files = len(word_files)
print(f"Number of Word files found: {num_files}")

# Extract text from each Word file and process them
for word_file in word_files:
    full_path = os.path.join(folder_path, word_file)
    text = extract_text_from_word(full_path)
    # print(f"Extracted text from {word_file}:\n{text[:200]}...")

# Send extracted text to the LLM to analyze and generate SQL schema
response = client.chat.completions.create(
    model="meta-llama/Llama-Vision-Free",
    messages=[{"role": "user", "content": f"Analyze this text and generate a SQL table schema: {text}"}],
    max_tokens=1000,
)

# Print the LLM's response (SQL table schema)
#print(response.choices[0].message.content)

# Save schema to a file (JSON format)
#schema = response.choices[0].message.content
#schema_filename = f"{word_file}_schema.json"
#with open(schema_filename, "w") as f:
#    json.dump({"schema": schema}, f)

#print(f"Schema saved to {schema_filename}")
