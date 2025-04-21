
from langchain_openai import  ChatOpenAI
from openai import OpenAI
import numpy as np 

llm_qwen_14B = ChatOpenAI(model="Qwen2.5-14B",  
                    # base_url='http://192.168.0.11:8011/v1', 
                    base_url='http://172.31.24.23:8001/v1', 
                    api_key='EMPTY',
                    temperature=0,
                    )



def embedding_bge(query_list):
    openai_api_key = "EMPTY"
    openai_api_base = 'http://172.31.24.23:8002/v1'

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

    responses = client.embeddings.create(
        input=query_list,
        model='bge-large-embedding',
    )
    embedding_list = [output_data.embedding for output_data in  responses.data]
    
    return np.array(embedding_list)


embedding_bge(['你好'])
llm_qwen_14B.invoke('你好')