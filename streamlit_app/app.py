
import streamlit as st
import requests

st.title("LLM-based RAG Search")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("enter your query...")
if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})
    flask_url = "http://localhost:5001/query"
    
    try:
        response = None # call the flask app and get response
        response = requests.post(flask_url, json={"query": query})
        if response.status_code == 200:
            answer = response.json().get('answer', "No answer received.")
            st.chat_message("assistant").markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.error(f"Error: {response.status_code}")
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {response.status_code}"})
    except Exception as e:
        st.error(f"Error: {e}")
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})
             
