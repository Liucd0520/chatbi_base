
from models.langchain_models import llm_qwen_14B
from utils.util import *
from langchain.prompts import PromptTemplate
from sql_processing.text2sql import schema_linking, sql_gen
from sql_processing.view_manager import create_temp_view, sql_replace_view, drop_view
from configs import config as config
from offline_initial import init
from langchain_community.utilities import SQLDatabase

from fastapi import APIRouter
from typing import List, Optional
import os

router = APIRouter()
@router.post('/', summary='生成SQL查询获取数据')
def sql_gen(query: str):
    pass 
