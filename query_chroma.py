from langchain.vectorstores import Chroma
import chromadb
import os
from dotenv import load_dotenv
import chromadb
load_dotenv()
from langchain.embeddings import OpenAIEmbeddings

# TODO: get scores from closest
# TODO: allow search in one doc only
# TODO: compare across multiple docs and choose top scores only
# LATER: get treshold from mean of scores?

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

embeddings = OpenAIEmbeddings()
# Initialize Chroma with the persistent client
def query_chroma(query, filter=None, sources=['Quintiere - Fundamentals of Fire Phenomena', 'BS 9999-2017'], n=5):
    total_results = []
    for source in sources:
        client = chromadb.PersistentClient(path=f"knowledge_db\{source}")
        vectordb = Chroma(client=client, embedding_function=embeddings)

        sub_results = vectordb.similarity_search_with_score(query, include=["documents", "scores", "metadata"], k=n)
        total_results += sub_results
    # get scores from closest
    pass
    sorted_results = sorted(total_results, key=lambda x: x[1])
    top_n = sorted_results[:min(5, len(sorted_results))]
    # remove scores?
    return top_n


if __name__ == "__main__":
    query_chroma("Fire Mains")
    # query_llm("External fire spread", "What is the external fire spread?")