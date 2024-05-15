from langchain_community.llms import Ollama


def mistral_tell_joke():
    llm = Ollama(model="mistral")
    response = llm.invoke("Tell me a joke")
    print(response)


def llama3_tell_joke():
    llm = Ollama(model="llama3")
    response = llm.invoke("Tell me a joke")
    print(response)


def mistral_stream_example():
    from langchain.callbacks.manager import CallbackManager
    from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

    llm = Ollama(
        model="mistral",
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    # llm("The first man on the summit of Mount Everest, the highest peak on Earth, was ...")
    llm.invoke("The first man on the moon was ...")


if __name__ == "__main__":
    chromadb()
