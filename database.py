import os
import json
from together import Together
from schema import extract_text_from_word
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Initialize Together client
client = Together(api_key=TOGETHER_API_KEY)

# Load the schema from the saved JSON file
schema_file = "./manual_schema.json"  
with open(schema_file, "r") as f:
    schema_data = json.load(f)["schema"]

# Specify the new Word document to extract data from
folder_path = "./Docu"
word_files = [f for f in os.listdir(folder_path) if f.endswith(".docx")]

# Extract text from each Word file and process them
for word_file in word_files:
    full_path = os.path.join(folder_path, word_file)
    text = extract_text_from_word(full_path)

# Send the new text and schema to the LLM to extract data
response = client.chat.completions.create(
    model="meta-llama/Llama-Vision-Free",
    messages=[
        {
            "role": "user",
            "content": f"Usando el siguiente esquema de tablas: {schema_data}, extrae los datos del documento y genera sentencias SQL INSERT INTO con los valores correspondientes: {text}",
        }
    ],
    max_tokens=1000,
)

# Extract the data from the response
extracted_data = response.choices[0].message.content

# Print the extracted data
print(f"Extracted data based on the schema: {extracted_data}")
