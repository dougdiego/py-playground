import sys
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

OBSIDIAN_JOURNAL_PATH = "/Users/doug/Vaults/Personal/Journal 2025.md"

load_dotenv()


def process_with_chatgpt(content):
    chat = ChatOpenAI(temperature=0.7)
    prompt = """Please read the following transcription of a journal entry and correct any inaccuracies. Focus on fixing spelling, grammar, punctuation, and any contextually obvious misinterpretations caused by transcription errors. Ensure the final text is coherent and faithful to a conversational journal style. When unsure, preserve the original meaning as closely as possible.  Only return the updated text, not the original. Thank you for your help!"""

    messages = [HumanMessage(content=f"{prompt}\n\n{content}")]
    response = chat.invoke(messages)
    # Clean up the response by replacing newlines with spaces and removing extra spaces
    cleaned_response = ' '.join(response.content.split())
    return cleaned_response


def process_file(input_file):
    try:
        # Split the file name and extension
        file_path, file_ext = os.path.splitext(input_file)
        # Create the output file name by adding .ai before the extension
        output_file = f"{file_path}.ai{file_ext}"

        # Read input file
        with open(input_file, "r") as infile:
            content = infile.read()

            # Process content with ChatGPT
            ai_response = process_with_chatgpt(content)

            # Write original content and AI response to output file
            with open(output_file, "w") as outfile:
                outfile.write(ai_response)

        print(f"Successfully created: {output_file}")
        return ai_response

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
        
def update_obsidian_file(input_file, cleaned_text, obsidian_file):
    try:
        # Extract date from input file name
        base_name = os.path.basename(input_file)
        # Get just the date portion (first 10 characters of YYYY-MM-DD)
        date = os.path.splitext(base_name)[0][:10]
        
        # Format the content with header
        formatted_content = f"\n## {date}\n{cleaned_text}\n"
        
        # Append to Obsidian file
        with open(obsidian_file, 'a') as f:
            f.write(formatted_content)
            
        print(f"Successfully appended to: {obsidian_file}")
        
    except Exception as e:
        print(f"Error updating Obsidian file: {str(e)}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    cleaned_text = process_file(input_file)
    if cleaned_text is None:
        sys.exit(1)
    update_obsidian_file(input_file, cleaned_text, OBSIDIAN_JOURNAL_PATH)

if __name__ == "__main__":
    main()
