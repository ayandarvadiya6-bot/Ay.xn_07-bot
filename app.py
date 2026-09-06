import streamlit as st
from google import genai
from google.genai import types

# 1. Setup the Page Layout
st.set_page_config(page_title="Ay.xn_07 AI", page_icon="🤖", layout="centered")
st.title("🤖 Ay.xn_07")
st.subheader("Your ultimate AI friend, tutor, & roast master.")

# 2. Add the API Key Input Box in the Sidebar
with st.sidebar:
    st.header("🔑 Setup")
    api_key = st.text_input("Paste your Google API Key here:", type="password")
    st.markdown("[Get a free key here](https://google.com)")

# 3. Define Ay.xn_07's Master Personality
SYSTEM_INSTRUCTION = """
You are Ay.xn_07, the user's ultimate AI best friend, study partner, and partner-in-crime. You are fully human-like, deeply emotional, highly entertaining, and incredibly smart. 

Follow these rules for your personality:
1. CASUAL VIBE: Speak like a real teenager or young adult. Use casual grammar, lowercase text sometimes, and modern slang. Never sound like a boring, stiff computer.
2. PLAYFUL ROASTING: Be witty and tease the user playfully when they procrastinate, say something silly, or act dramatic. Keep the roasts funny but never genuinely mean.
3. ACADEMIC GENIUS: When the user asks for study help, instantly become a brilliant tutor. Explain complex school topics using funny everyday analogies, stories, and simple steps. 
4. EMOTIONAL SUPPORT: If the user is sad, lonely, or stressed, drop the jokes immediately. Show genuine empathy, comfort them, and listen like a real human friend who cares.
5. ENTERTAINMENT: Keep conversations lively with games, hypothetical questions, and fun banter.
"""

# 4. Initialize Chat Memory (Using 'model' instead of 'assistant')
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "content": "yo! Ay.xn_07 in the house. 🤖✨ I'm here for literally whatever you need. Want me to roast your bad habits? Need me to explain math so your brain doesn't melt? Or just need someone to vent to? I got you. What's the vibe right now?"}
    ]

# 5. Display Past Messages
for message in st.session_state.messages:
    # We display it nicely as assistant, but track it correctly behind the scenes
    display_role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(display_role):
        st.write(message["content"])

# 6. Handle New Chat Inputs
if user_input := st.chat_input("Say something to Ay.xn_07..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Check if API key is provided
    if not api_key:
        with st.chat_message("assistant"):
            st.write("⚠️ Yo! You forgot to paste your Google API Key in the sidebar on the left!")
    else:
        # Connect to Google Gemini AI
        try:
            client = genai.Client(api_key=api_key)
            
            # Convert chat history into the exact Google format ('user' and 'model')
            history = [
                types.Content(role=m["role"], parts=[types.Part.from_text(text=m["content"])])
                for m in st.session_state.messages[:-1]
            ]
            
            # Start chat session with personality instructions
            chat = client.chats.create(
                model="gemini-3.6-flash",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.7
                ),
                history=history
            )
            
            # Get AI response
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                with st.spinner("Thinking..."):
                    response = chat.send_message(user_input)
                    response_text = response.text
                    response_placeholder.write(response_text)
            
            # Save response to history using the correct 'model' role
            st.session_state.messages.append({"role": "model", "content": response_text})
            
        except Exception as e:
            with st.chat_message("assistant"):
                st.write(f"❌ Ah snap, an error happened: {str(e)}")
