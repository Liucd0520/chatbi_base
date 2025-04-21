from fastapi import FastAPI, APIRouter
from typing import List, Optional
import tempfile
from pydantic import BaseModel
from enum import Enum
from fastapi import File, UploadFile
import os
from offline_initial import init
router = APIRouter()

@router.post('/', summary='初始化项目')
async def knowledge_gen(mysql_uri: str = 'mysql+pymysql://root:liucd123@localhost:3306/db_TEMP',
                        table_names: str = 't_temp',
                        data_save_dir: str = 'data__',
                        log_dir: str = 'logs__',
                        gen_query_list: List = [],
                        related_columns: List = [],
                        ):
    if not os.path.exists(data_save_dir):
        os.makedirs(data_save_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    

    setup_flag = True
    schema_list, schema_linking_samples, distinct_values = \
        init(query_list=gen_query_list, 
             is_meta_data=setup_flag, 
             is_schema_linking_gen=setup_flag, 
             is_distinct_values_gen=setup_flag)
    
    