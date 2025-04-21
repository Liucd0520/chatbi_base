
# mysql_uri = 'mysql+mysqlconnector://root:liucd123@localhost:3306/pdga'
# mysql_uri = 'mysql+mysqlconnector://root:liucd123@localhost:3306/12345'
# table_names = ['hongkou', ]
mysql_uri = 'mysql+pymysql://root:liucd123@localhost:3306/12345'
table_names = ['shanghai', ]

log_dir = './logs'
data_save_dir = 'data_shanghai'

# related_columns = ['事项大类', '事项小类',  '事项名称', '事项标签', '案件描述/内容描述']
# related_columns = ['资产名称', '资产分类', '备注名称']
related_columns = ['一级分类', '二级分类', '三级分类', '四级分类', '内容描述']

# 视图索引 控制不同的查询权限
view_index = '工号'