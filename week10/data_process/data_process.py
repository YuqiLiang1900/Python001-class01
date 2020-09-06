"""
数据预处理与语义情感分析
"""
import pandas as pd
from snownlp import SnowNLP
from sqlalchemy import create_engine

import config

engine = create_engine(config.MYSQL_URL)

sql = 'SELECT * FROM product_comment'

df = pd.read_sql(sql, engine)

# 数据预处理
df.dropna(inplace=True)  # 删除缺失值
df.drop(df[df['comment'] == ''].index, inplace=True)  # 删除空值
df.drop_duplicates('comment', inplace=True)  # 去重
df.drop(['id'], axis=1, inplace=True)  # 删除 id 列


# 语义情感分析
def _sentiment(text):
    s = SnowNLP(text)
    return s.sentiments


df['sentiment'] = df.comment.apply(_sentiment)

# 分析结果入库
# 保存到 MySQL
df.to_sql('product_comment_sentiment', engine, index=False, if_exists='append')
