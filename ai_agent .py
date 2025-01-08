#!/usr/bin/env python
# coding: utf-8

# # The AI agent evaluates Upwork project descriptions against Emerssive's past projects and technical expertise. It analyzes the relevance of the project's requirements by comparing them to Emerssive's tech stack and project portfolio. The agent provides:
# 
# #### * A relevance score (0-10) based on alignment with technical expertise and project similarities.
# #### * A concise analysis explaining why the project is or isn't a good fit.
# #### * A list of specific relevant past projects or an explanation if none are directly applicable.

# In[40]:


from docx import Document
import openai

# Load OpenAI API key
with open("api_key.txt", "r") as file:
    openai.api_key = file.read().strip()

# Default path to Emerssive's Word file
DEFAULT_WORD_FILE_PATH = r"C:\Emerssive\Proporsals\Notes for porporsals\AIAgent.docx"

# Read Word file content
def read_word_file(file_path=DEFAULT_WORD_FILE_PATH):
    """
    Read and extract the full text content from a Word file.
    """
    doc = Document(file_path)
    content = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
    return "\n".join(content)

# Generate GPT analysis
def generate_gpt_analysis(upwork_description, emerssive_data):
    """
    Use GPT to analyze the Upwork project description against Emerssive's project data.
    """
    prompt = f"""
    You are an AI project evaluator for a software development company called "Emerssive."
    Below is Emerssive's expertise and past project data:

    {emerssive_data}

    Evaluate the following Upwork project description:

    "{upwork_description}"

    Instructions:
    1. Prioritize the alignment between the project's technical requirements and Emerssive's technical expertise.
    2. Use the provided project data as a reference but also consider Emerssive's adaptability and capability to handle similar challenges.
    3. Provide the following:
        - A relevance score from 0 to 10, where:
            - 10 = Perfect alignment with expertise and past projects.
            - 7–9 = Strong alignment, even if minor gaps exist in project examples.
            - 4–6 = Partial alignment, requiring additional effort or learning.
            - 0–3 = Poor alignment or outside expertise.
        - A concise analysis explaining why the project is or isn't a good fit.
        - List relevant projects from the provided data, if any.
        - If no exact matches exist, explain how Emerssive's expertise still makes the project feasible.
        - Recommendations for approaching or adapting to the project.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant analyzing project relevance."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error generating GPT response: {e}"

# Main function
def evaluate_project(upwork_description):
    """
    Evaluate an Upwork project description against Emerssive's expertise using GPT.
    """
    # Read the entire Word file content
    emerssive_data = read_word_file()

    # Generate GPT analysis
    gpt_response = generate_gpt_analysis(upwork_description, emerssive_data)

    return gpt_response



# In[41]:


if __name__ == "__main__":
    print("Enter the Upwork project description:")
    upwork_description = input("> ")  # Get the Upwork project description from the user

    # Evaluate the project
    result = evaluate_project(upwork_description)
    print("\nDetailed Analysis:\n", result)


# In[ ]:




