import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from pyecharts.charts import Bar

plt.rcParams['font.sans-serif'] = 'SimHei'
engine = create_engine('mysql+pymysql://root:123456@localhost:3306/beike_spider')
sql = ''' select * from wh_loupan; '''
# 将查到的数据 load到pd
df = pd.read_sql_query(sql, engine)

# 过滤掉其他的类型 只拿住宅做分析 同时只保留了4个列
houses = df.loc[df["lp_type"] == "住宅", ['id', 'name', 'ava_price', 'block']]

# 通过区来做分组 这里返回的是一个series类型 索引为区，值为区下楼盘的数量 因此需要将对应的值取出来
group_num = houses.groupby("block").size()
index = []
val = []
for i in group_num.items():
    index.append(i[0])
    val.append(i[1])

bar = Bar()
bar.add_xaxis(index)
bar.add_yaxis("楼盘数", val)
# render 会生成本地 HTML 文件，默认会在当前目录生成 render.html 文件
# 也可以传入路径参数，如 bar.render("mycharts.html")
bar.render("./figures/楼盘分布.html")
