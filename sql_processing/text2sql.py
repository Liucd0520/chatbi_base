
from pathlib import Path
import sys 
import os 
# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)


import pymysql
# from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain_community.utilities import SQLDatabase
from langchain.prompts import PromptTemplate
import time 
from langchain_openai import  ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from prompts.prompt import *
from utils.util import *
import json 
import copy 
from langchain.schema.runnable import Runnable
from models.langchain_models import llm_qwen_14B
import json 
import os 



def schema_linking(query: str, 
                   schema: str, 
                   related_columns: list = [], 
                   values_dict: dict = {},
                   examples: list = [], 
                   chain: Runnable = None):
    
    output = chain.invoke({"schema": schema, "query": query, "samples": examples})
    
    old_output = copy.deepcopy(output)
    cond_columns = copy.deepcopy(output['condition_columns'])

    print(f"cond_columns: {cond_columns}")

    for condition_field, condition_value in cond_columns.items():
        if condition_field not in related_columns: # 条件字段要与字典库里的匹配
            continue
       
        renew_dict = {}
        for k, v in values_dict.items():  
            if condition_value in v:  
                renew_dict.update({k: condition_value})
        
        if len(renew_dict) > 0: # 意味着有匹配上的
            output['condition_columns'].pop(condition_field) 
            output['condition_columns'].update(renew_dict)
        else:   
            unstructured_field = related_columns[-1]
            # 意味着四级分类里的值没有与之对应的，那就扔给非结构化字段
            output['condition_columns'].pop(condition_field)
            output['condition_columns'].update({unstructured_field: condition_value})

    return  old_output, output


def sql_gen(query: str, columns: dict, schema: str, chain: Runnable):
    # 利用上一步schema补全的结果    
            
    output = chain.invoke({"schema": schema, "query": query, "columns": columns})
    
    return output

