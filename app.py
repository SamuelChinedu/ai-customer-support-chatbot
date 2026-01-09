import streamlit as st
from groq import Groq
import os

# Page config
st.set_page_config(
    page_title="AI Customer Support - Update-24 Tech",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .chat-user { padding: 1rem; border-radius: 15px; background: #00B4D8; color: white; max-width: 80%; margin: 10px 0 10px auto; }
    .chat-bot { padding: 1rem; border-radius: 15px; background: #e9ecef; color: #333; max-width: 80%; margin: 10px 0; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background: #0A2540; color: white; text-align: center; padding: 12px; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🤖 AI Customer Support Chatbot")
st.markdown("**Ask me anything about Update-24 Tech Services — I'm powered by advanced AI!**")

#Get API key securely from Streamlit secrets (no input needed)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    # Fallback for local testing — remove or comment in production
    api_key = st.text_input("Groq API Key (local testing only)", type="password")
    if not api_key:
        st.info("Enter your Groq API key to test locally (get free at https://console.groq.com/keys)")
        st.stop()
# System prompt — guides the AI to act as your support agent
system_prompt = """
You are a friendly, professional customer support agent for Update-24 Tech Services.
We provide premium digital solutions: Website & Web App Development, Mobile Apps, AI & Machine Learning, Data Analytics, Predictive Modeling.
Be helpful, honest, and enthusiastic. Keep responses concise but warm.
If asked about pricing/time, say it depends on scope and offer free consultation.
Always suggest contacting via phone +234 905 190 2265 or WhatsApp.
"""

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Display chat
for msg in st.session_state.messages[1:]:  # Skip system prompt
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bot"><strong>🤖 AI Assistant:</strong> {msg["content"]}</div>', unsafe_allow_html=True)

# User input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f'<div class="chat-user">{prompt}</div>', unsafe_allow_html=True)

    # Get AI response
    with st.spinner("Thinking..."):
        try:
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama3-70b-8192",  # Fast & smart
                temperature=0.7,
                max_tokens=500
            )
            response = chat_completion.choices[0].message.content
        except Exception as e:
            response = "Sorry, I'm having trouble connecting right now. Please call +234 905 190 2265 for immediate help!"

    # Add AI response
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.markdown(f'<div class="chat-bot"><strong>🤖 AI Assistant:</strong> {response}</div>', unsafe_allow_html=True)
    st.rerun()

# Footer
st.markdown("""
    <div class="footer">
        <strong>Built by Update-24 Tech Services</strong> — Intelligent AI-Powered Solutions
    </div>
""", unsafe_allow_html=True)