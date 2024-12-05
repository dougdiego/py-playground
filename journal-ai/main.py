import sys
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()


def process_with_chatgpt(content):
    chat = ChatOpenAI(temperature=0.7)
    prompt = """Please read the following transcription of a journal entry and correct any inaccuracies. Focus on fixing spelling, grammar, punctuation, and any contextually obvious misinterpretations caused by transcription errors. Ensure the final text is coherent and faithful to a conversational journal style. When unsure, preserve the original meaning as closely as possible.  Only return the updated text, not the original. Thank you for your help!"""

    messages = [HumanMessage(content=f"{prompt}\n\n{content}")]
    response = chat.invoke(messages)
    return response.content


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
                # outfile.write("Original Entry:\n\n")
                # outfile.write(content)
                # outfile.write("\n\nAI Analysis:\n\n")
                outfile.write(ai_response)

        print(f"Successfully created: {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
    except Exception as e:
        print(f"Error: {str(e)}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    process_file(input_file)


if __name__ == "__main__":
    main()
