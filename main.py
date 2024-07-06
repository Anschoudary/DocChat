
import PyPDF2 
import streamlit as st
from io import StringIO
import google.generativeai as genai

def get_model():
    genai.configure(api_key="AIzaSyDahZhLwTabewAMPZnBvKh-FMn_uA-yg9k")
    # getting the model
    model = genai.GenerativeModel(model_name = "gemini-1.5-flash")

    # starting a chat_session with model
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Understand this: {text}",
                ],
            },
        ]
    )
    return chat_session

def get_document():
    # Get file path from user
    path = st.file_uploader(" ", type=[".pdf", ".txt"])

    if path:
        # Handle text files
        if path.type == "text/plain":
            string_data = StringIO(path.getvalue().decode("utf-8"))
            text = string_data.getvalue()
            return text
        
        # Handle PDF files
        elif path.type == "application/pdf":
            reader = PyPDF2.PdfReader(path)
            pdf_text = ""
            for page in reader.pages:
                pdf_text += page.extract_text()

            return pdf_text
        # Handle other file types
        else:
            st.error("Unsupported file type!")

def docChat(chat_session):
    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        try:
            response = chat_session.send_message(prompt)
        except Exception as e:
            st.error("Request timed out, plz check your connection!")
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response.text)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.text})


# main function
if __name__ == '__main__':

    # title of app
    st.title("DocChat")
    text = get_document()
    chat_session = get_model()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        
    docChat(chat_session)
