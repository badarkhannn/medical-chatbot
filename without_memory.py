import os
import chainlit as cl
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from pinecone import Pinecone

# Load environment variables
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Index name
index_name = "medical-bot"

# Load the local embedding model correctly
embedding_model = HuggingFaceEmbeddings(model_name="./local_model")

# Load the existing Pinecone index
vector_store = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embedding_model
)

# Set up the retriever
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Initialize OpenAI LLM
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.5, max_tokens=200)

# Prompt template
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the answer concise.\n\n{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("human", "{input}")]
)

# Create RAG chain
qa_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever=retriever, combine_docs_chain=qa_chain)

# Chainlit message handler
@cl.on_message
async def main(message: cl.Message):
    print(f"[User] {message.content}")
    response = rag_chain.invoke({"input": message.content})
    print(f"[Bot] {response.get('answer')}")
    await cl.Message(content=response.get("answer", "No answer found.")).send()
