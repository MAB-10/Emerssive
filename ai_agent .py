#!/usr/bin/env python
# coding: utf-8

# In[3]:


from docx import Document
import openai

# Load OpenAI API key
with open("api_key.txt", "r") as file:
    openai.api_key = file.read().strip()

# Default path to Emerssive's Word file
DEFAULT_WORD_FILE_PATH = r"C:\Emerssive\Proporsals\Notes for porporsals\AI Agent.docx"

# Read Word file and parse projects
def read_word_file(file_path=DEFAULT_WORD_FILE_PATH):
    """
    Read and extract text content from a Word file.
    """
    doc = Document(file_path)
    content = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
    return "\n".join(content)

def extract_projects(raw_text):
    """
    Extract individual projects from the raw text data.
    """
    # Assuming projects are separated by a header or delimiter like "Project:"
    projects = []
    for line in raw_text.split("\n"):
        if "Project:" in line:
            projects.append(line.strip())
    return projects

# Generate GPT-4 analysis
def generate_gpt_analysis(upwork_description, emerssive_data, relevant_projects):
    """
    Use GPT-4 to analyze the Upwork project description against Emerssive's project data.
    """
    relevant_projects_text = "\n".join(relevant_projects) if relevant_projects else "No directly relevant projects found."
    prompt = f"""
    You are an expert project evaluator for a software development team named "Emerssive."
    Below is Emerssive's past project data and technical expertise:

    {emerssive_data}

    Relevant projects based on the provided data:
    {relevant_projects_text}

    Evaluate the following Upwork project description:

    "{upwork_description}"

    Instructions:
    - Prioritize the match between the project's technical requirements and Emerssive's technical expertise.
    - If the project aligns strongly with the tech stack but doesn't perfectly match past projects, still consider it a good fit.
    - If the project somewhat matches past projects but uses a new tech stack Emerssive can handle, note that it is still suitable.
    - Provide the following in your response:
        1. A relevance score from 0 to 10, where 10 means the project strongly aligns with Emerssive's expertise.
        2. A concise analysis explaining why the project is or isn't a good fit.
        3. Highlight any specific past projects that are similar to the Upwork project description.
       
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using GPT-4 took a long time to get a repsone 
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
    Evaluate an Upwork project description against Emerssive's data using GPT-4.
    """
    # Read Emerssive data from the Word file
    raw_data = read_word_file()
    emerssive_data = raw_data
    
    # Extract individual projects
    projects = extract_projects(raw_data)
    
    # Find relevant projects (naive match on project description for now)
    relevant_projects = [project for project in projects if any(keyword in upwork_description.lower() for keyword in project.lower().split())]

    # Generate GPT analysis
    gpt_response = generate_gpt_analysis(upwork_description, emerssive_data, relevant_projects)
    
    return gpt_response



# In[4]:


if __name__ == "__main__":
    print("Enter the Upwork project description:")
    upwork_description = input("> ")  # Get project description from the user
    
    # Evaluate the project
    result = evaluate_project(upwork_description)
    print("\nDetailed Analysis:\n", result)


# In[ ]:




