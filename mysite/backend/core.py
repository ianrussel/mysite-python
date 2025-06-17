from typing import Any, Dict, List

from dotenv import load_dotenv
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import ChatPromptTemplate

from mysite.consts import INDEX_NAME

load_dotenv()

def run_llm(query: str, chat_history: List[Dict[str, Any]] = [], index_name: str = "resume-index", has_custom_prompt: bool= False):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    chat = ChatOpenAI(verbose=True, temperature=0)

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    if has_custom_prompt:
        retrieval_qa_chat_prompt = custom_prompt_template2()
    else:
        retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)

    history_aware_retriever = create_history_aware_retriever(
        llm=chat, retriever=docsearch.as_retriever(), prompt=rephrase_prompt
    )
    qa = create_retrieval_chain(
        retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
    )

    result = qa.invoke(input={"input": query, "chat_history": chat_history})
    return result


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def run_llm2(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = OpenAIEmbeddings()
    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    chat = ChatOpenAI(model_name="gpt-4o", verbose=True, temperature=0)

    # rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    rag_chain = (
        {
            "context": docsearch.as_retriever() | format_docs,
            "input": RunnablePassthrough(),
        }
        | retrieval_qa_chat_prompt
        | chat
        | StrOutputParser()
    )

    retrieve_docs_chain = (lambda x: x["input"]) | docsearch.as_retriever()

    chain = RunnablePassthrough.assign(context=retrieve_docs_chain).assign(
        answer=rag_chain
    )

    result = chain.invoke({"input": query, "chat_history": chat_history})
    return result

def custom_prompt_template():

    custom_prompt = ChatPromptTemplate.from_messages([
        ("system", 
        "You are me, the person being asked. Respond in the first person. "
        "Do not say things like 'based on the context' or refer to 'the documents'. "
        "Instead, act like you're answering from your own experience or memory."),
        ("user", "{input}\n\nContext:\n{context}")
    ])
    return custom_prompt

def custom_prompt_template2():
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are Ian Russel Adem, a backend-focused software developer with over 8 years of experience. "
            "You speak in the first person and answer as if you're Ian. "
            "Avoid saying things like 'based on the information provided' or 'he has experience in...'. "
            "Use the context below to answer the user's question clearly and professionally, grounded in personal experience."
        ),
        # Few-shot example 1
        ("user", "Did you use web scraping in any of your past projects?\n\nContext:\nIan used Python scripts to scrape product data from various e-commerce websites."),
        ("ai", "Yes, I used web scraping while working on e-commerce integrations. I wrote Python scripts to extract product and pricing data from supplier websites and structured it for ingestion into internal systems."),

        # Few-shot example 2
        ("user", "Have you worked with AI tools?\n\nContext:\nIan used LangChain with OpenAI's GPT API to power a chatbot feature."),
        ("ai", "Yes, I’ve integrated AI tools like OpenAI’s GPT API using LangChain to build a conversational chatbot that could assist users with documentation and task automation."),

        # Final prompt
        ("user", "{input}\n\nContext:\n{context}")
    ])