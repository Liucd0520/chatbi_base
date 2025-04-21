#-*- coding : utf-8-*-
# coding:unicode_escape

import pymysql
from sqlalchemy import create_engine
import pandas as pd
import re

def contains_chinese(text: str) -> bool:
    """
    判断字符串是否包含中文字符

    Args:
        text: 需要检查的字符串

    Returns:
        bool: 是否包含中文字符
    """
    # 方法1：使用正则表达式匹配中文字符范围
    pattern = re.compile(r'[\u4e00-\u9fff]')
    return bool(pattern.search(text))

def excel2db(file_path: str, table_name: str, uri: str):
    if  contains_chinese(file_path):
        print('文件名包含中文字符，将文件名转换为utf-8编码')

    # 判断文件类型
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path,) 
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path, encoding='utf-8' ) 
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    engine = create_engine(uri)

    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)


if __name__ == '__main__':
    excel2db(file_path='fix_assert.xlsx', 
             table_name='huangpu_fayuan', 
             uri='mysql+pymysql://root:liucd123@localhost:3306/huangpu')

