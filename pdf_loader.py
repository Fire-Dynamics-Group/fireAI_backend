from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA
from langchain.document_loaders import TextLoader

from langchain.document_loaders import PyPDFLoader
import os
from dotenv import load_dotenv
import chromadb
load_dotenv()
# required_version = version.parse("1.1.1")
# current_version = version.parse(openai.__version__)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# TODO: persist db
# TODO: allow backend to call db
# TODO: add title and page metadata
# LATER: open pdf at correct page on frontend

def load_pdf(file_path: str):
    for pdf in os.listdir(file_path):
        all_texts = []
        client = chromadb.PersistentClient(path=f"knowledge_db/{pdf[:-4]}")
        collection = client.get_or_create_collection("Fire_Docs")
        pdf_path = f'{file_path}\\{pdf}'
        try:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            for doc in documents:
                # final part of path without .pdf
                doc.metadata['title'] = pdf_path.split('\\')[-1][:-4]
                # doc.metadata['title'] = 'Quintiere - Fundamentals of Fire Phenomena'
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
                texts = text_splitter.split_documents(documents)
                all_texts.append(texts)
        except:
            pass

        embeddings = OpenAIEmbeddings()
        collection = Chroma.from_documents(texts, embeddings, client=client)

        query = "External fire spread"
        collection.similarity_search(query)


load_pdf('knowledge_docs')

'''
# filter collection for updated source
example_db.get(where={"source": "some_other_source"})
'''