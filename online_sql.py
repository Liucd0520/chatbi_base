from sql_processing.text2sql import  sql_gen
from langchain.schema.runnable import Runnable
from sql_processing.view_manager import create_temp_view, sql_replace_view, drop_view
from utils.util import sql_semantic_rewrite, sql_execute
from configs import config as config
from utils.util import *

async def sql_path(query: str, linking_columns: dict, schema: str, view_values: str, unstructured_column: str,
             sql_gen_chain: Runnable, ner_clf_chain: Runnable, sql_feedback_chain: Runnable, 
             app_retrieve: Runnable, milvus_opt):
     
    sql_command = sql_gen(query, linking_columns, schema, sql_gen_chain)
    sql_command_std = sql_command
    logger.info(f"stad sql: {sql_command}")

    params = {}  # 初始化参数，仅当处理非结构化字段时使用
    if config.is_semantic_analysis:
        # 可能会有语义分析 
        unstr_dict = unstructure_value_extract(sql_command, unstructured_column)  
        logger.info(f'非结构化信息为: {unstr_dict}')
        # 字典格式（可能存在多个kv对）：{"`案件描述/内容描述` LIKE '%支付宝平台%';": '支付宝平台'}
        # 如果unstr_dict 为空，语义分析依然能够正常处理
        sql_command, params = await sql_semantic_rewrite(sql_command, milvus_opt, unstr_dict, unstructured_column,  ner_clf_chain, app_retrieve)
        sql_command_semantic = sql_command
        
    # 基于视图的查询
    view_table_names = []
    for table_name in config.table_names:
        view_table_name = create_temp_view(config.mysql_uri, table_name, 
                                            config.view_index,  view_values)
        if view_table_name:
            sql_command = sql_replace_view(sql_command, table_name, view_table_name)
            view_table_names.append(view_table_name)
            logger.info(f'视图为： {view_table_name}')
    
    if len(view_table_names) == 0:
        logger.info(f"没有找到< {view_values} >对应的视图")
    sql_command_view = sql_command
    

    # 执行sql查询
    execute_result = sql_execute(config.mysql_uri, sql_command, schema, params, sql_feedback_chain)
    obtain_data = eval(execute_result)

    # 执行完sql之后删除视图
    drop_view(config.mysql_uri, view_table_names)

    sql_result = {"sql_std": sql_command_std, "sql_semantic": sql_command_semantic, "sql_view": sql_command_view}
    return obtain_data, sql_result, params
