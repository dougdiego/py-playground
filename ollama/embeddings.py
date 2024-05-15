from langchain_community.llms import Ollama
ollama = Ollama(
    base_url='http://localhost:11434',
    model="llama3"
)
#print(ollama.invoke("why is the sky blue"))


#from langchain.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://www.gutenberg.org/files/1727/1727-h/1727-h.htm")
data = loader.load()

from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

#from langchain.embeddings import OllamaEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
#from langchain.vectorstores import Chroma
from langchain_community.vectorstores import Chroma
oembed = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")
vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)

question="Who is Neleus and who is in Neleus' family?"
docs = vectorstore.similarity_search(question)
print(len(docs))

from langchain.chains import RetrievalQA
qachain=RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
response = qachain.invoke({"query": question})
print(response)