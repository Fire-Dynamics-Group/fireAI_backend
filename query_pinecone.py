from langchain.vectorstores import Pinecone
from pinecone import Pinecone, ServerlessSpec
import pinecone
import os
from dotenv import load_dotenv
load_dotenv()
from langchain.embeddings import OpenAIEmbeddings

import json
# TODO: setup for pinecone
# search filtering for metadata of source -> perhaps chapter etc later

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV')


embeddings = OpenAIEmbeddings()
# TODO: remove duplicates from index -> or don't add duplicates in the first place


def query_pinecone(query, filter=None, sources=['BS 9999-2017'], n=5):
    pc = Pinecone(
        PINECONE_API_KEY,
        # environment=PINECONE_ENV
    )
    # pinecone.init(
    #     api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    #     environment=PINECONE_ENV  # next to api key in console
    # )
    # 
    index_name = "fire-docs"
    total_results = []
    # for source in sources: # later filter by source
    vectordb = pc.Index(index_name)
    query_embedding = embeddings.embed_query(query)

    query_response = vectordb.query(
                                    vector=query_embedding, 
                                    top_k=n,
                                    include_metadata=True
                                    )
    if query_response:
        query_response = query_response.to_dict()
        query_response = query_response['matches']
        # sub_results = vectordb.similarity_search(query)
        print(query_response[0]['metadata']['text'])
        # total_results += sub_results
        # get scores from closest
        # pass
        # sorted_results = sorted(total_results, key=lambda x: x[1])
        # top_n = sorted_results[:min(5, len(sorted_results))]
        # remove scores?
        return query_response
    print("No results found")
    return []


if __name__ == "__main__":
    # query_pinecone("office escape distances")
    user_input = "office escape distances"
    context = query_pinecone(user_input)
    context_text = [result.metadata['text'].replace("\n", " ") for result in context]
    context_text = ';;;'.join(context_text)
    print("context_text:", context_text)
    content = f"context:'''{context_text}'''user input:'''{user_input}'''"
    print(content)
