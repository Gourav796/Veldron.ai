import streamlit as st
import requests

# ============================================
# AI FUNCTIONS
# ============================================
def ask_groq(question):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": question}]
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"

def create_image(prompt):
    image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}"
    return image_url

# ============================================
# WEB INTERFACE
# ============================================
st.set_page_config(page_title="AI Agent", page_icon="🤖", layout="centered")

st.title("🤖 Multi-AI Agent")
st.caption("Groq (Text) + Flux (Images)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("image"):
            st.image(msg["image"])

# User input
user_input = st.chat_input("Type 'Draw a cat' or 'Write a poem'...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Route and respond
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            image_words = ["draw", "image", "picture", "photo", "illustration", "art"]
            
            if any(word in user_input.lower() for word in image_words):
                # Generate image
                img_url = create_image(user_input)
                st.image(img_url)
                st.caption(f"Generated for: {user_input}")
                response_text = f"🎨 Image generated: {user_input}"
                st.session_state.messages.append({"role": "assistant", "content": response_text, "image": img_url})
            else:
                # Text response from Groq
                response = ask_groq(user_input)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
