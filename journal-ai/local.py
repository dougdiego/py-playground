import sys
import os
from typing import Any, List, Optional
from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseMessage, ChatResult, ChatGeneration, HumanMessage
from dotenv import load_dotenv
import requests
import json

load_dotenv()

class LocalLLMChat(BaseChatModel):
    @property
    def _client(self) -> Any:
        return None

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        prompt = messages[0].content
        headers = {'Content-Type': 'application/json'}
        data = {
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.7,
            'stream': False
        }
        
        response = requests.post('http://localhost:1234/v1/chat/completions', 
                               headers=headers, 
                               data=json.dumps(data))
        
        if response.status_code == 200:
            text = response.json()['choices'][0]['message']['content']
            generation = ChatGeneration(message=HumanMessage(content=text))
            return ChatResult(generations=[generation])
        else:
            raise Exception(f"Error from LLM API: {response.text}")

    @property
    def _llm_type(self) -> str:
        return "local-llm"

def process_with_local_llm(content):
    chat = LocalLLMChat()
    #prompt = """Please read the following transcription of a journal entry that was transcribed from audio using the Whisper Model. Correct any inaccuracies in spelling, grammar, punctuation, and contextually obvious transcription errors, but maintain the original tone, style, and level of detail. Do not add any content or interpretations beyond what is explicitly stated. Preserve the conversational and informal journal style of the text. Return only the corrected version without additional commentary."""
    #prompt = """Please read the following transcription of a journal entry transcribed using the Whisper Model. Correct any spelling, grammar, punctuation, and contextually obvious transcription errors, ensuring the text is coherent and preserves its conversational journal style. Do not add or embellish content that was not explicitly stated in the original text, including interpretations or elaborations. If a section is unclear or ambiguous, make minimal corrections while maintaining the original meaning as closely as possible. Return only the corrected text without any additional commentary or formatting changes."""
    prompt = """As an AI assistant processing a Whisper-transcribed journal entry, your task is to:

1. Fix ONLY these specific items:
   - Basic spelling (e.g., "expresses" to "espressos")
   - Punctuation and capitalization
   - Common transcription errors (e.g., "yo" when context clearly indicates something else)
   - Basic formatting of times, dates, and numbers
   - Proper titles of media (TV shows, movies, books)
   - Brand names and proper nouns

2. Examples of proper title corrections:
   - "shits creek" → "Schitt's Creek"
   - "silo" → "Silo"
   - Maintain proper capitalization and apostrophes in titles

3. DO NOT:
   - Add any new information not explicitly stated
   - Make assumptions about how events ended
   - Fill in missing details
   - Add transitions between thoughts
   - Change incomplete sentences into complete ones
   - Add or remove any events or actions

4. PRESERVE EXACTLY:
   - All times mentioned
   - All names
   - All activities described
   - Incomplete thoughts or sentences
   - The casual, speech-like style
   - The original sequence of events

The final text should be one paragraph with no newlines or extra spaces.

Return only the corrected text without any additions or embellishments."""

    messages = [HumanMessage(content=f"{prompt}\n\n{content}")]
    response = chat.invoke(messages)
    return response.content

def process_file(input_file):
    try:
        # Split the file name and extension
        file_path, file_ext = os.path.splitext(input_file)
        # Create the output file name by adding .ai before the extension
        output_file = f"{file_path}.ai.llama3.2{file_ext}"

        # Read input file
        with open(input_file, "r") as infile:
            content = infile.read()

            # Process content with local LLM
            ai_response = process_with_local_llm(content)

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
