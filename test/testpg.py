import psycopg2
from psycopg2 import sql
conn=None
try:
    # 连接到PostgreSQL数据库
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )

    # 创建游标对象
    cur = conn.cursor()

    # 准备SQL语句
    insert_query = sql.SQL("""
        INSERT INTO strategy_backtest (code, strategy_name, type, price, trigger_time)
        VALUES (%s, %s, %s, %s, %s)
    """)
    code='123'
    strategy_name='测试'
    type='买入'
    price='123'
    trigger_time='2024'

    # 执行SQL语句
    cur.execute(insert_query, (code, strategy_name, type, price, trigger_time,))

    # 提交事务
    conn.commit()


except (Exception, psycopg2.Error) as error:
    print(f"写入数据库时发生错误: {error}")

finally:
    # 关闭游标和连接
    if conn:
        cur.close()
        conn.close()