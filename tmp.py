import re 

sql = "SELECT DISTINCT `上报地址` FROM `HongKouDemo` WHERE `发现时间` >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND `案件描述/内容描述` LIKE '%设备维修%' LIMIT 10;"
pattern = r"(?i)(SELECT\s+)(.*?)(\s+FROM)"
modified_sql = re.sub(pattern, lambda match: f"{match.group(1)}*{match.group(3)}", sql, flags=re.IGNORECASE)
print(modified_sql)       