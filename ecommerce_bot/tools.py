import os
from langchain_core.tools import tool
from sqlalchemy import create_engine, text
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Initialize DB connection
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///ecommerce.db")
engine = create_engine(DATABASE_URL)

# Initialize Chroma connection
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# ensure ChromaDB is created before using it
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

@tool
def check_inventory(query: str) -> str:
    """Use this tool to check inventory, stock, price, or order status. 
    Provide a natural language query describing what you need from the structured database.
    Example: "Show me black running shoes under $100" or "Check order ORD-123"
    """
    # For a real system, we'd use SQLDatabaseChain or create an agent that translates text to SQL.
    # To keep it beginner-friendly but robust, we'll implement a basic SQL chain using LangChain.
    from langchain_community.utilities import SQLDatabase
    from langchain_community.agent_toolkits import create_sql_agent
    from langchain_groq import ChatGroq
    
    try:
        db = SQLDatabase(engine)
        llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
        agent = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=False)
        result = agent.invoke({"input": query})
        return result["output"]
    except Exception as e:
        return f"Error querying database: {str(e)}"

@tool
def check_policies(query: str) -> str:
    """Use this tool to find information about return policies, shipping policies, care guides, or FAQs.
    Example: "What is the return policy?" or "How do I wash this?"
    """
    try:
        docs = retriever.invoke(query)
        if not docs:
            return "I couldn't find any relevant policy information."
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Error searching policies: {str(e)}"

# Expose tools for the graph
ecommerce_tools = [check_inventory, check_policies]
