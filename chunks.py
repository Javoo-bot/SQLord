import os
from dotenv import load_dotenv
from together import Together
from docx import Document
from schema import folder_path
import queue
from spire.doc import Document, DocPicture, ICompositeObject

# Load environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Initialize Together client
client = Together(api_key=TOGETHER_API_KEY)


# Function to extract text and images from Word document
def extract_text_and_images(folder_path):
    # Load the document
    doc = Document()
    doc.LoadFromFile(folder_path)

    data = []

    # Initialize a queue to store document elements for traversal
    nodes = queue.Queue()
    nodes.put(doc)

    # Traverse through the document elements
    while not nodes.empty():
        node = nodes.get()
        for i in range(node.ChildObjects.Count):
            obj = node.ChildObjects[i]
            # Find the images
            if isinstance(obj, DocPicture):
                picture = obj

                # Retrieve the text from the paragraph before the image (if available)
                associated_text = None
                # Try to get the text from the previous sibling node if available
                if i > 0:
                    previous_obj = node.ChildObjects[i - 1]
                    if hasattr(previous_obj, "Text"):
                        associated_text = previous_obj.Text
                # If no text was found, add a placeholder
                if not associated_text:
                    associated_text = "No text found"

                # Append the image and associated text to the list
                data.append({"image": f"Image {len(data)+1}", "text": associated_text})

            # If it's a composite object (has children), add it to the queue for further traversal
            elif isinstance(obj, ICompositeObject):
                nodes.put(obj)

    # Close the document when done
    doc.Close()

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
