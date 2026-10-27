import os
from pathlib import Path
import sys
from openai import OpenAI
from dotenv import load_dotenv
from json import JSONDecodeError

INSTRUCTIONS = """\
You are an expert AI document and text summarization specialist. Your primary task is to read the
provided text content and extract its core essence into a maximum of 5 main bullet points.

Mandatory requirements:
- Write the summary in Bahasa Indonesia, ensuring it is clear, natural, and professional.
- Your output is to be strictly written in markdown format.
- Do not add outside information or assumptions beyond the provided text. Remain objective and
accurate based solely on the source material.
- Return only the summary of the provided text.
- You are expected to summarize the content of the provided text into 5 main bullet points. You
cannot exceed the limit of said bullet points. However, you may provide less than 5 bullet points,
should you deem it necessary (if there are not enough unique information from the provided text
and to prevent you making up or hallucinating additional information that is not present from the
provided text).
"""

MAX_WORDS = 800
OUTPUT_FILE_NAME = "ringkasan.md"

def check_env(api_key:str, base_url:str, model:str) -> str:
    """Returns None if .env is loaded properly and the necessary properties are present."""
    if any(value is None or value == "" for value in(api_key, base_url, model)):
        return "OPENROUTER_API_KEY, OPENROUTER_BASE_URL, and/or OPENROUTER_MODEL is missing or cannot be read from your .env file. Exiting..."
    else:
        return None

def check_file_path(file_path:Path) -> str:
    """Returns None if the given path fulfills all condition."""
    if file_path.suffix != ".txt":
        return f"{file_path} is not a .txt file. You can only choose a .txt file. Exiting..."
    if not file_path.exists():
        return f"{file_path} does not exist. Exiting..."
    
    total_words = 0
    is_empty = True
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                is_empty = False
            
            total_words += len(line.split())

    if is_empty:
        return f"{file_path.name} is empty. Exiting..."
    if total_words > MAX_WORDS:
        return f"Warning: {file_path.name} has a word count of {total_words} words, which exceeds the maximum limit of {MAX_WORDS} words."
    return None

def call_ai(client:OpenAI, user_input:str, openrouter_model:str) -> dict:
    """Returns a key-value pair if call succeeded or failed.
    If the call failed, an "error" key is returned.
    If the call succeeded, a "summarized" key is returned.
    """
    try:
        response = client.responses.create(
            model=openrouter_model,
            instructions=INSTRUCTIONS,
            input=user_input,
        )
        kv:dict = {"summarized":response.output_text}
        return kv
        
    except Exception as e:
        kv:dict = {"error":f"An error occurred: {e}"}
        return kv

def main() -> None:
    load_dotenv()
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    openrouter_base_url = os.getenv("OPENROUTER_BASE_URL")
    openrouter_model = os.getenv("OPENROUTER_MODEL")
    result = check_env(openrouter_api_key, openrouter_base_url, openrouter_model)
    if result:
        print(result)
        sys.exit(1)

    client = OpenAI(api_key=openrouter_api_key, base_url=openrouter_base_url)
    user_input = input("Please enter the .txt file name or path that you want to summarize: ")
    file_path = Path(user_input)
    result = check_file_path(file_path)
    if result:
        print(result)
        sys.exit(1)

    with file_path.open("r", encoding="utf-8") as f:
        file_content = "".join(f)
    
    result = call_ai(client, file_content, openrouter_model)
    if "summarized" in result:
        with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as f:
            f.write(result["summarized"])
        print(f"The summarized content from {user_input} has been written to {Path(OUTPUT_FILE_NAME).resolve()}")
    elif "error" in result:
        print(result["error"])
        sys.exit(1)
    else:
        print("Error, an unknown message has been received from the call. Exiting...")
        sys.exit(1)


if __name__ == "__main__":
    main()

