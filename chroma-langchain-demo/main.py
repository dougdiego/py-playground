# https://www.gettingstarted.ai
# email: jeff@gettingstarted.ai
# written by jeff

# Don't forget to set your OPEN_AI_KEY
# In your terminal execute this command: export OPENAI_API_KEY="YOUR_KEY_HERE"

# Import required modules from the LangChain package
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Load a PDF document and split it into sections
loader = PyPDFLoader("data/ECM_Synchronika_Manual_20171108.pdf")
docs = loader.load_and_split()

# Initialize the OpenAI chat model
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)

# Initialize the OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Load the Chroma database from disk
chroma_db = Chroma(
    persist_directory="data",
    embedding_function=embeddings,
    collection_name="lc_chroma_demo",
)

# Get the collection from the Chroma database
collection = chroma_db.get()

# If the collection is empty, create a new one
if len(collection["ids"]) == 0:
    print("Creating a new collection")
    # Create a new Chroma database from the documents
    chroma_db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="data",
        collection_name="lc_chroma_demo",
    )

    # Save the Chroma database to disk
    chroma_db.persist()

print("Collection:")
print(collection)

# Prepare query
query = "What is this document about?"

print("Similarity search:")
print(chroma_db.similarity_search(query))

print("Similarity search with score:")
print(chroma_db.similarity_search_with_score(query))

# Add a custom metadata tag to the first document
docs[0].metadata = {
    "tag": "demo",
}

# Update the document in the collection
chroma_db.update_document(document=docs[0], document_id=collection["ids"][0])

# Find the document with the custom metadata tag
collection = chroma_db.get(where={"tag": "demo"})

# Prompt the model
chain = RetrievalQA.from_chain_type(
    llm=llm, chain_type="stuff", retriever=chroma_db.as_retriever()
)

# Execute the chain
response = chain(query)

# Print the response
print(response["result"])

# Delete the collection
chroma_db.delete_collection()
