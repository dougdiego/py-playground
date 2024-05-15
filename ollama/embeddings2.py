from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings

ollama = Ollama(
    base_url='http://localhost:11434',
    model="llama3"
)
#print(ollama.invoke("why is the sky blue"))


#from langchain.document_loaders import WebBaseLoader
# from langchain_community.document_loaders import WebBaseLoader
# loader = WebBaseLoader("https://www.gutenberg.org/files/1727/1727-h/1727-h.htm")
# data = loader.load()


# Load a PDF document and split it into sections
loader = PyPDFLoader("data/ECM_Synchronika_Manual_20171108.pdf")
docs = loader.load_and_split()


embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
#embeddings = SentenceTransformerEmbeddings(model_name="nomic-embed-text")

# Load the Chroma database from disk
chroma_db = Chroma(
    persist_directory="data",
    embedding_function=embeddings,
    collection_name="rag-chroma",
)

# Get the collection from the Chroma database
collection = chroma_db.get()

print("1.Collection:")
print(collection)

# If the collection is empty, create a new one
if len(collection["ids"]) == 0:
    print("Creating a new collection")
    chroma_db = Chroma.from_documents(
        documents=docs,
        collection_name="rag-chroma",
        embedding=embeddings,
    )
    # Save the Chroma database to disk
    chroma_db.persist()
    collection = chroma_db.get()

print("2.Collection:")
print(collection)
    
# retriever = chroma_db.as_retriever()

# question = "What are the approaches to Task Decomposition?"
# docs = chroma_db.similarity_search(question)
# len(docs)

# print(docs[0])


## COPIED

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

print("Document with custom metadata tag:")
print(docs[0])

# Prompt the model
chain = RetrievalQA.from_chain_type(
    llm=ollama, chain_type="stuff", retriever=chroma_db.as_retriever()
)

# Execute the chain
response = chain(query)

# Print the response
print(response["result"])

# Delete the collection
chroma_db.delete_collection()