import streamlit as st
import os
from langchain_core.messages import HumanMessage, AIMessage

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "ecommerce.db")
chroma_path = os.path.join(BASE_DIR, "chroma_db")

# Initialize databases if they don't exist
if not os.path.exists(db_path):
    from init_postgres import init_db
    init_db()

if not os.path.exists(chroma_path):
    from init_chroma import init_chroma
    init_chroma()

from graph import graph

st.set_page_config(page_title="E-Commerce AI Assistant", page_icon="🛍️")

# Custom CSS for UI styling
st.markdown("""
<style>
    .stApp {
        background-color: #1E1E2E;
        color: #Cdd6F4;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #313244;
        border-left: 4px solid #89b4fa;
    }
    .chat-message.bot {
        background-color: #45475a;
        border-left: 4px solid #a6e3a1;
    }
    .stTextInput input {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #585b70;
    }
    h1 {
        color: #89b4fa;
        text-align: center;
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛍️ E-Commerce AI Assistant")
st.markdown("Ask me about our products, check your order status, or inquire about our policies!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# React to user input
if prompt := st.chat_input("What are you looking for today?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to state
    st.session_state.messages.append(HumanMessage(content=prompt))
    
    # Prepare input for graph
    inputs = {"messages": st.session_state.messages}
    
    with st.spinner("Thinking..."):
        try:
            # Invoke the graph
            result = graph.invoke(inputs)
            
            # The final state will have all messages, we just want the last one (AI response)
            final_message = result["messages"][-1]
            
            # Add assistant response to state
            st.session_state.messages.append(final_message)
            
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(final_message.content)
        except Exception as e:
            st.error(f"Error processing your request: {str(e)}")
