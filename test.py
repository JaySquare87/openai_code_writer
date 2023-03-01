import openai
import os
import sys
from datetime import datetime

openai.api_key = "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"

def ask_question(question, model_engine="text-davinci-002", prompt=""):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=f"{prompt} Q: {question}\nA:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()
    return answer

# Parse command-line arguments
if len(sys.argv) != 2:
    print("Usage: python chatgpt.py <session_name>")
    sys.exit(1)

session_name = sys.argv[1]
folder_name = datetime.today().strftime("%Y-%m-%d") + " ChatSessions"
filename = f"{folder_name}/{session_name}.md"

# Create folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Load previous questions from session file
previous_questions = []
if os.path.exists(filename):
    with open(filename, "r") as file:
        for line in file:
            if line.startswith("## Q:"):
                question = line.strip()[6:]
                previous_questions.append(question)

# Main loop
with open(filename, "a") as file:
    while True:
        # Ask user for question
        question = input("Ask a question (or enter 'quit' to exit): ")

        # Check if user wants to quit
        if question.lower() == "quit":
            break

        # Check if question is a follow-up to a previous question
        prompt = ""
        for previous_question in previous_questions:
            if previous_question.lower() in question.lower():
                prompt = f"{prompt} Q: {previous_question}\nA: {ask_question(previous_question)}"

        # Get answer and print to console
        answer = ask_question(question, prompt=prompt)
        print(f"A: {answer}")

        # Save question and answer to session file
        file.write(f"## Q: {question}\n\n")
        file.write(f"{answer}\n\n")
        print(f"Answer saved to {filename}\n")

        # Add question to previous questions list
        previous_questions.append(question)

