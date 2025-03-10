from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain import OpenAI
import streamlit as st
import os
import tempfile

# Set up OpenAI API
os.environ["OPENAI_API_KEY"] = "YOUR-API"
llm = OpenAI(temperature=0)


def summarize_pdfs_from_folder(pdfs_folder):
    summaries = []
    for pdf_file in pdfs_folder:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_path = temp_file.name
            temp_file.write(pdf_file.read())
        
        loader = PyPDFLoader(temp_path)
        docs = loader.load_and_split()
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(docs)
        summaries.append(summary)

        # Delete the temporary file
        os.remove(temp_path)
    
    return summaries

def main():
# Streamlit App
    st.title(" 🌈 Multiple PDF Summarizer ")

    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://images.unsplash.com/photo-1702816789113-bbc54df5f1aa?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: 260%;
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
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Allow user to upload PDF files
    pdf_files = st.sidebar.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    st.sidebar.title('🤯🤩 Upload your PDF here')
    st.sidebar.title("You will Receive your PDF summaries 🐟")

    if pdf_files:
    # Generate summaries when the "Generate Summary" button is clicked
      if st.sidebar.button("Generate Summary"):
        st.write("Summaries:")
        summaries = summarize_pdfs_from_folder(pdf_files)
        for i, summary in enumerate(summaries):
            st.write(f"Summary for PDF {i+1}:")
            st.write(summary)

if __name__ == "__main__":
    main()