import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

def init_chroma():
    print("Initializing ChromaDB...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    policies = [
        Document(
            page_content="Return Policy: You can return items within 30 days of purchase for a full refund. Items must be in original condition.",
            metadata={"source": "return_policy"}
        ),
        Document(
            page_content="Shipping Policy: Free standard shipping on orders over $50. Expedited shipping is available for an additional fee.",
            metadata={"source": "shipping_policy"}
        ),
        Document(
            page_content="How to wash this shirt: Machine wash cold with like colors. Tumble dry low. Do not bleach.",
            metadata={"source": "care_guide"}
        ),
        Document(
            page_content="International Shipping: We currently ship to the US, Canada, UK, and Australia. Customs fees may apply.",
            metadata={"source": "shipping_policy"}
        ),
        Document(
            page_content="Damaged Items: If you receive a damaged item, please contact support within 48 hours with a photo of the damage.",
            metadata={"source": "return_policy"}
        )
    ]
    
    # Create Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=policies, 
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    print("ChromaDB populated successfully.")

if __name__ == "__main__":
    init_chroma()
