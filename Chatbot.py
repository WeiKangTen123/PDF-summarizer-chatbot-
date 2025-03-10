import streamlit as st
import base64
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
import os
os.environ["OPENAI_API_KEY"] = "YOUR-API"
EMBEDDING_MODEL = "text-embedding-ada-002"
import tempfile


st.set_page_config(
    page_title="Multipage App",
    page_icon="🤖"
)

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey! 👋"]

def conversation_chat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]

def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'

    # Displaying File
    st.sidebar.markdown(pdf_display, unsafe_allow_html=True)

def display_chat_history(chain):
    reply_container = st.container()
    script = """<div id = 'chat_outer'></div>"""
    container = st.container()
    script1 = """<div id = 'chat_outer'></div>"""

    with reply_container:
        script = """<div id = 'chat_inner'></div>"""
        st.markdown(script, unsafe_allow_html=True)

    with container:
        script1 = """<div id = 'chat_inner'></div>"""
        st.markdown(script1, unsafe_allow_html=True)
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask about your PDF", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            with st.spinner('Generating response...'):
                output = conversation_chat(user_input, chain, st.session_state['history'])

            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="thumbs")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

def create_conversational_chain(vector_store):
    # Create llm
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                 retriever=vector_store.as_retriever(),
                                                 memory=memory
)
    return chain

def get_vector_stores(text_chunks):
        # Create embeddings
        embeddings = OpenAIEmbeddings()

        # Create vector store
        vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)
        return vector_store

def main():
    # Initialize session state
    initialize_session_state()
    st.title("|🐱‍🏍 Our Multi-PDF ChatBot using GPT 3.5")

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://images.unsplash.com/photo-1702816789113-bbc54df5f1aa?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: 100%;
        background-position: top left;
        background-repeat: no-repeat;
        background-attachment: fixed;
        }}

    [data-testid="stSidebar"] > div:first-child {{
    background-image: url("https://images.unsplash.com/photo-1702635429447-06e9ee0c617c?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: 45%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}
        
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}

    [data-testid="stToolbar"] {{
        right: 2rem;
        }}
    </style>
    """
    reply_container = """<style>
    div[data-testid='stVerticalBlock']:has(div#chat_inner):not(:has(div#chat_outer)) {background-color: #E4F2EC};
    </style>
    """
    container = """<style>
    div[data-testid='stVerticalBlock']:has(div#chat_inner):not(:has(div#chat_outer)) {background-color: #E4F2EC};
    </style>
    """
    st.markdown(container, unsafe_allow_html=True)
    st.markdown(reply_container, unsafe_allow_html=True) 
    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Initialize Streamlit
    st.sidebar.title('🤯🤡 LLM ChatBot')
    st.sidebar.subheader('To understand this chatbot application functions and details, click on [documentation](https://docs.google.com/document/d/1y2sjwp6OM_EDuIpxoTdZy_bb0Lae6klvAY-OFCnTiEU/edit#heading=h.2et92p0)')
    st.sidebar.title("Document Processing")
    uploaded_files = st.sidebar.file_uploader("Upload files", type=["pdf"], accept_multiple_files=True)
    st.sidebar.title("Read PDF information")

    if uploaded_files:
        text = []
        for file in uploaded_files:
            file_extension = os.path.splitext(file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name

            st.sidebar.markdown("<h4 style color:black;'>File details</h4>", unsafe_allow_html=True)
            st.sidebar.info(file.name)
            st.sidebar.markdown("<h4 style color:black;'>File preview</h4>", unsafe_allow_html=True)
            pdf_view = displayPDF(temp_file_path)
              
            loader = None
            if file_extension == ".pdf":
                loader = PyPDFLoader(temp_file_path)

            if loader:
                text.extend(loader.load())
                os.remove(temp_file_path)


        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=20)
        text_chunks = text_splitter.split_documents(text)

        vector_store = get_vector_stores(text_chunks)

        # Create the chain object
        chain = create_conversational_chain(vector_store)

        
        display_chat_history(chain)

if __name__ == "__main__":
    main()