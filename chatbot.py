import streamlit as st
import requests
import json
from typing import Optional

# Configure page
st.set_page_config(
    page_title="Mistral AI Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful background and responsive styling
st.markdown("""
<style>
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Custom container styling - responsive */
    .main-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1rem;
        margin: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        max-height: 70vh;
        overflow-y: auto;
    }
    
    /* Title styling - responsive */
    .title {
        color: white;
        text-align: center;
        font-size: clamp(1.8rem, 5vw, 3rem);
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        padding: 0 1rem;
    }
    
    /* Chat messages styling - responsive */
    .user-message {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 0.8rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-left: clamp(0.5rem, 3vw, 2rem);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        word-wrap: break-word;
        max-width: 85%;
        font-size: clamp(0.9rem, 2.5vw, 1rem);
        line-height: 1.4;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #4834d4, #686de0);
        color: white;
        padding: 0.8rem 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        margin-right: clamp(0.5rem, 3vw, 2rem);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        word-wrap: break-word;
        max-width: 85%;
        font-size: clamp(0.9rem, 2.5vw, 1rem);
        line-height: 1.4;
    }
    
    /* Sidebar styling - responsive */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Input styling - responsive */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        color: white;
        font-size: clamp(0.9rem, 2.5vw, 1rem);
        padding: 0.75rem;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }
    
    /* Chat input styling - responsive */
    .stChatInput > div > div > textarea {
        background: rgba(255, 255, 255, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        color: white;
        font-size: clamp(0.9rem, 2.5vw, 1rem);
        padding: 0.75rem;
    }
    
    .stChatInput > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.7);
    }
    
    /* Button styling - responsive */
    .stButton > button {
        background: linear-gradient(135deg, #00d4aa, #00a085);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
        font-size: clamp(0.8rem, 2.5vw, 1rem);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .main-container {
            margin: 0.25rem;
            padding: 0.75rem;
            border-radius: 15px;
            max-height: 65vh;
        }
        
        .user-message, .bot-message {
            margin-left: 0.5rem;
            margin-right: 0.5rem;
            padding: 0.7rem;
            max-width: 90%;
            font-size: 0.9rem;
        }
        
        .title {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
        }
        
        /* Hide sidebar on mobile for more space */
        .css-1d391kg {
            display: none;
        }
        
        /* Full width on mobile */
        .stApp > div {
            padding: 0.5rem;
        }
    }
    
    /* Tablet optimizations */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main-container {
            margin: 0.75rem;
            padding: 1.25rem;
            max-height: 68vh;
        }
        
        .user-message, .bot-message {
            padding: 0.9rem;
            max-width: 80%;
        }
        
        .title {
            font-size: 2.5rem;
        }
    }
    
    /* Desktop optimizations */
    @media (min-width: 1025px) {
        .main-container {
            margin: 1rem;
            padding: 2rem;
            max-height: 70vh;
        }
        
        .user-message, .bot-message {
            padding: 1rem;
            max-width: 75%;
        }
        
        .title {
            font-size: 3rem;
        }
    }
    
    /* Scrollbar styling */
    .main-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .main-container::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
    }
    
    .main-container::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 3px;
    }
    
    .main-container::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.5);
    }
    
    /* Loading spinner customization */
    .stSpinner > div {
        border-top-color: white !important;
    }
    
    /* Footer responsive */
    .footer {
        color: white;
        opacity: 0.7;
        text-align: center;
        font-size: clamp(0.8rem, 2vw, 1rem);
        padding: 1rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

class MistralClient:
    def __init__(self, api_key: str = None, model: str = "mistral-small"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
    
    def generate_response(self, message: str) -> str:
        """Generate response from Mistral API"""
        if not self.api_key or self.api_key == "your-mistral-api-key-here":
            return "⚠️ Please add your Mistral API key to use the real AI model. Get one from https://console.mistral.ai/"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": message}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            if "401" in str(e):
                return "❌ Invalid API key. Please check your Mistral API key."
            elif "429" in str(e):
                return "⏳ Rate limit exceeded. Please wait a moment and try again."
            elif "500" in str(e):
                return "🔧 Mistral API is temporarily unavailable. Please try again later."
            else:
                return f"⚠️ API Error: {str(e)}"
        except KeyError:
            return "❌ Error: Invalid response format from API"
        except Exception as e:
            return f"⚠️ Unexpected error: {str(e)}"

def main():
    # Title
    st.markdown('<h1 class="title">🤖 Mistral AI Chat Assistant</h1>', unsafe_allow_html=True)
    
    # Sidebar with only clear chat button
    with st.sidebar:
        st.markdown("### 🗑️ Chat Controls")
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">👤 You: {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">🤖 Mistral: {message["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area - must be outside containers
    user_input = st.chat_input("Type your message here...")
    
    # Process user input
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Initialize Mistral client with API key from secrets
        try:
            api_key = st.secrets["MISTRAL_API_KEY"]
        except KeyError:
            api_key = None
            st.error("🔑 MISTRAL_API_KEY not found in secrets. Please add it in Streamlit Cloud settings.")
        
        client = MistralClient(api_key, "mistral-small")
        
        # Show loading spinner
        with st.spinner("🤔 Thinking..."):
            response = client.generate_response(user_input)
        
        # Add bot response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Rerun to update chat
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p class="footer">Made with ❤️ using Streamlit and Mistral AI</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
