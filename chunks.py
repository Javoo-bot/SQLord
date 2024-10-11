import os
from dotenv import load_dotenv
from together import Together
from docx import Document

# Load environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Initialize Together client
client = Together(api_key=TOGETHER_API_KEY)


# Function to extract text and images from Word document
def extract_text_and_images(file_path):
    doc = Document(file_path)
    data = []
    for i, paragraph in enumerate(doc.paragraphs):
        # Check if the paragraph contains an image (using run in paragraph)
        if paragraph.runs and any(run.element.xpath(".//w:drawing") for run in paragraph.runs):
            # Save text and associate it with an image
            associated_text = doc.paragraphs[i - 1].text if i > 0 else "No text found"
            data.append({"image": f"Image {len(data)+1}", "text": associated_text})
    return data


# Function to generate prompt for the LLM
def generate_prompt(text):
    prompt = f"""
    Based on the following text, extract the instructions and categorize them into the following format:
    - Correct: The exact step-by-step process that is correct.
    - Result OK: The expected successful outcome.
    - Incorrect: Common mistakes or incorrect steps.
    - Result Error: Possible failure or error messages.
    - Recs: Recommendations for avoiding or fixing mistakes.
    - Fix: Specific steps to correct errors.
    - Impact: What will happen if things go wrong.

    Text: {text}

    Format your response like:
    
    [Task Name] - [Correct steps] - [Expected result] - [Common mistakes] - [Error messages] - [Recommendations]
    
    Format your response as a single string with the above structure.
    """
    return prompt


# Specify the folder containing the Word documents
folder_path = "./Docu"

# List all files in the folder and filter for .docx files
word_files = [f for f in os.listdir(folder_path) if f.endswith(".docx")]

# Process each Word file
for word_file in word_files:
    full_path = os.path.join(folder_path, word_file)

    # Extract text and images from the document
    data = extract_text_and_images(full_path)

    for idx, entry in enumerate(data):
        # Generate prompt for LLM
        prompt = generate_prompt(entry["text"])

        # Send prompt to LLM and retrieve response
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
        )

        # Get the response content (formatted string)
        structured_string = response.choices[0].message.content.strip()

        # Save the structured string to a file
        output_filename = f"{word_file}_image_{idx+1}_instructions.txt"
        with open(output_filename, "w") as f:
            f.write(structured_string)

        print(f"Structured instruction string for image {idx+1} saved to {output_filename}")
