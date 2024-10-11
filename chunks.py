import os
from dotenv import load_dotenv
from together import Together
from spire.doc import Document, DocPicture, ICompositeObject
import queue
from schema import file

# Load environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Initialize Together client
client = Together(api_key=TOGETHER_API_KEY)


# Function to extract images from Word document
def extract_images(file_path):
    # Load the Word document
    doc = Document()
    doc.LoadFromFile(file_path)

    images = []
    nodes = queue.Queue()
    nodes.put(doc)

    # Traverse through the document elements to find images
    while not nodes.empty():
        node = nodes.get()
        for i in range(node.ChildObjects.Count):
            obj = node.ChildObjects[i]

            if isinstance(obj, DocPicture):
                # Extract the image binary data
                image_data = obj.ImageBytes

                if image_data:
                    # Append the image data directly to the list (no saving to disk)
                    images.append(image_data)

            # If the object has child nodes, add it to the queue for further traversal
            elif isinstance(obj, ICompositeObject):
                nodes.put(obj)

    # Close the document
    doc.Close()

    return images


# Function to generate prompt for LLM using the image
def generate_prompt_for_image(image_name):
    prompt = f"""
    Based on the analysis of the image "{image_name}", extract the instructions and categorize them into the following format:
    - Correct: The exact step-by-step process that is correct.
    - Result OK: The expected successful outcome.
    - Incorrect: Common mistakes or incorrect steps.
    - Result Error: Possible failure or error messages.
    - Recs: Recommendations for avoiding or fixing mistakes.
    - Fix: Specific steps to correct errors.
    - Impact: What will happen if things go wrong.

    Format your response like:

    [Task Name] - [Correct steps] - [Expected result] - [Common mistakes] - [Error messages] - [Recommendations]
    """
    return prompt


# Function to pass image data to LLM and generate structured output
def analyze_image_with_llm(image_data, image_name):
    prompt = generate_prompt_for_image(image_name)

    # Send image binary data and prompt to Together AI's LLM
    # Assuming that Together AI's LLM can handle image data (this depends on the LLM's capabilities)
    response = client.chat.completions.create(
        model="black-forest-labs/FLUX.1-schnell",  # Example model for images
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
    )

    # Return the structured response from the LLM
    return response.choices[0].message.content


# Save LLM responses to a text file
def save_to_text_file(responses, output_file):
    with open(output_file, "w") as f:
        for idx, response in enumerate(responses):
            f.write(f"Image {idx + 1}:\n")
            f.write(response + "\n\n")


# Example usage
file_path = "Template.docx"
output_file = "llm_analysis_output.txt"
