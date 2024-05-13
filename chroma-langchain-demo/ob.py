import os
from chromadb import ChromaDB

# https://github.com/langchain-ai/langchain/discussions/16158

# Specify the directory path
directory_path = '/Users/dougdiego/Vaults-Test/Prosper'

# Initialize ChromaDB
db = ChromaDB()

# Iterate over the files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.md'):
        # Read the markdown file
        with open(os.path.join(directory_path, filename), 'r') as file:
            markdown_content = file.read()

        # Import the markdown content into ChromaDB
        db.import_markdown(markdown_content)

# Close the ChromaDB connection
db.close()


