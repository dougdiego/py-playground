

- [Run LLMs locally | 🦜️🔗 LangChain](https://python.langchain.com/v0.1/docs/guides/development/local_llms/)
- [Ollama and LangChain: Run LLMs locally | by Abonia Sojasingarayar | Medium](https://medium.com/@abonia/ollama-and-langchain-run-llms-locally-900931914a46)

```
brew install ollama  
brew services start ollama
```

```
ollama pull mistral
ollama pull llama3
ollama pull nomic-embed-text
```

```
curl http://localhost:11434/api/generate -d '{  
"model": "mistral",  
"prompt":"Why is the sky blue?"  
}'
```


```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

```
brew services stop ollama
```


https://github.com/ollama/ollama/blob/main/docs/tutorials/langchainpy.md
https://docs.trychroma.com/integrations/ollama
https://ollama.com/blog/embedding-models
