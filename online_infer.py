
from prompts.prompt import *
from models.langchain_models import llm_qwen_14B
from utils.util import *
from langchain.prompts import PromptTemplate
from sql_processing.text2sql import schema_linking, sql_gen
from sql_processing.view_manager import create_temp_view, sql_replace_view, drop_view
from configs import config as config
from offline_initial import init
from langchain_community.utilities import SQLDatabase


def infer_pipeline(query, view_values):
    
    prompt_schema_linking = PromptTemplate(template=schema_link_prompt, input_variables=["schema", "query", 'samples'])
    linking_chain = create_json_chain(llm_qwen_14B, prompt_schema_linking)

    
    old_linking_columns, new_linking_columns = schema_linking(query, schema, config.related_columns, 
                                                              distinct_values, schema_linking_samples, 
                                                              linking_chain)
    print(f"old_linking_result: {old_linking_columns}")
    print(f"new_linking_result: {new_linking_columns}")

    prompt_sql_gen = PromptTemplate(template=sql_gen_prompt, input_variables=["schema", "query", 'columns'])
    sql_gen_chain = create_json_chain(llm_qwen_14B, prompt_sql_gen)
    sql_gen_result = sql_gen(query, new_linking_columns, schema, sql_gen_chain)
    sql_command = sql_gen_result['SQL']
    
    view_table_names = []
    for table_name in config.table_names:
        if table_name in columns_dict.keys():
            view_table_name = create_temp_view(config.mysql_uri, table_name, 
                                               config.view_index,  view_values)
            if view_table_name:
                sql_command = sql_replace_view(sql_command, table_name, view_table_name)
                view_table_names.append(view_table_name)

    if len(view_table_names) == 0:
        print(f"没有找到< {view_values} >对应的视图")
    
    # 执行sql查询
    mysql_db = SQLDatabase.from_uri(config.mysql_uri)
    result = mysql_db.run(sql_command)
    obtain_data = eval(result)

    # 执行完sql之后删除视图
    drop_view(config.mysql_uri, view_table_names)
    
    print(f"sql_command: {sql_command}")
    print(f"result: {result}")

    return obtain_data, sql_command
