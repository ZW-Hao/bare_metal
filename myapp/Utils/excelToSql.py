import pandas as pd

# 替换为你的 Excel 文件路径
excel_file_path = 'daoru.xlsx'
# 替换为你的数据库表名
table_name = 'bare_metal'

# 读取 Excel 文件中的第一个工作簿
df = pd.read_excel(excel_file_path)

# 开始构建 SQL 插入语句
sql_insert_statements = []

for index, row in df.iterrows():
    sn = str(row['sn'])
    ip = str(row['ip'])
    bmcip = f"'{row['bmcip']}'" if pd.notnull(row['bmcip']) else 'NULL'
    address = str(row['address'])
    type_ = str(row['type'])
    restart = f"'{row['restart']}'" if pd.notnull(row['restart']) and row['restart'] != '' else 'NULL'

    # 构造插入语句
    sql = f"('{sn}', '{ip}', {bmcip}, '{address}', '{type_}', {restart})"
    sql_insert_statements.append(sql)

# 拼接所有的值语句来形成最终的 SQL 语句
sql_values = ',\n'.join(sql_insert_statements)
final_sql_statement = f"INSERT INTO {table_name} (sn, ip, bmcip, address, type, restart) VALUES\n{sql_values};"

print(final_sql_statement)
