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


# Function to extract images from Word document
def extract_images(file_path, output_path):
    # Load the Word document
    doc = Document()
    doc.LoadFromFile(file_path)

    # List to hold the image file paths
    images = []

    # Queue to traverse the document elements
    nodes = queue.Queue()
    nodes.put(doc)

    # Traverse through the document elements to find images
    while not nodes.empty():
        node = nodes.get()
        for i in range(node.ChildObjects.Count):
            obj = node.ChildObjects[i]

            if isinstance(obj, DocPicture):
                # Extract the image data (binary format)
                image_data = obj.ImageBytes  # Get the image data as binary bytes

                if image_data:
                    # Define the image file name and path
                    image_path = os.path.join(output_path, f"image_{len(images) + 1}.png")

                    # Save the binary data as an image file
                    with open(image_path, "wb") as image_file:
                        image_file.write(image_data)  # Write binary data to file

                    images.append(image_path)

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
    
    Image: {image_name}
    
    Please format the response according to this structure.
    """
    return prompt


# Function to analyze an image using the FLUX.1-schnell model
def analyze_image_with_flux(image_path, prompt):
    # Send the image analysis request to Together AI model
    response = client.chat.completions.create(
        model="black-forest-labs/FLUX.1-schnell",  # The image model
        messages=[{"role": "user", "content": prompt}],  # Use the custom prompt
        max_tokens=1000,
    )
    return response.choices[0].message.content


# Specify the folder containing the Word documents
folder_path = r"C:\Users\jlmenendez\Desktop\db\Docu"

# Process each Word file
word_files = [f for f in os.listdir(folder_path) if f.endswith(".docx")]

# Output file for storing analysis results
output_filename = "flux_image_analysis_output.txt"
with open(output_filename, "w") as f_out:
    for word_file in word_files:
        full_path = os.path.join(folder_path, word_file)
        images = extract_images(full_path)

        for image_path in images:
            # Generate the structured prompt for the image
            prompt = generate_prompt_for_image(image_path)

            # Analyze the image using the FLUX model
            analysis_result = analyze_image_with_flux(image_path, prompt)

            # Save the structured output
            f_out.write(f"Image: {image_path}\n")
            f_out.write(f"Analysis:\n{analysis_result}\n\n")

    print(f"Structured output saved to {output_filename}")
