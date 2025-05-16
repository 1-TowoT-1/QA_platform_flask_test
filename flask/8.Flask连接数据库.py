from flask import Flask, jsonify
import datetime
import json
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

app = Flask(__name__)

# ################################### 使用 psycopg 原生连接（小型项目） ###################################
# # 连接数据库（使用 psycopg v3 写法）
# import psycopg
# def get_db_connection():
#     conn = psycopg.connect(
#         dbname="postgres",
#         user="postgres",
#         password="123456",
#         host="XXX.XXX.XXX",  # localhost或远程IP
#         port="5432"
#     )
#     return conn


# @app.route('/')
# def users():
#     conn = get_db_connection()
#     cur = conn.cursor()
#     # 执行 SQL 查询
#     cur.execute('SELECT * FROM student_scores;')
#     columns = [desc[0] for desc in cur.description]
#     rows = cur.fetchall()
#     # 关闭连接
#     cur.close()
#     conn.close()

#     # 构造成 dict 列表，并手动处理中文和日期格式
#     result = []
#     for row in rows:
#         row_dict = {}
#         for key, value in zip(columns, row):
#             if isinstance(value, datetime.date):
#                 row_dict[key] = value.strftime('%Y-%m-%d')  # 自定义日期格式
#             else:
#                 row_dict[key] = value
#         result.append(row_dict)
#     # 使用 json.dumps 保留中文
#     json_str = json.dumps(result, ensure_ascii=False) # ensure_ascii默认是True
#     return app.response_class(
#         response=json_str,
#         status=200,
#         mimetype='application/json; charset=utf-8'
#     )


# if __name__ == '__main__':
#     app.run(debug=True)



#################################### 使用 SQLAlchemy + Flask-SQLAlchemy ###################################
from flask_sqlalchemy import SQLAlchemy

# Postgresql主机名称
HOSTNAME = 'XXX.XXX.XXX'
# 监听端口
POST = '5432'
# 连接用户名
USERNAME = 'postgres'
# 连接密码
PASSWORD = '123456'
# 连接数据库的名称
DATABASE = 'postgres'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{POST}/{DATABASE}'

# 在app.config中填写好需要连接的数据库信息
# 数据库必须是真实存在的，具体可以看postgresql的笔记

db = SQLAlchemy(app)

# ORM是一种可以将python对象导入关系型数据库的技术
# 一个ORM模型对应一张数据库的表
# 创建ORM映射表：
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # varchar, null
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# ORM的增删改查CURD，将其操作添加到远程数据库
@app.route('/add')
def add_user():
    # 1. 创建ORM对象
    user = User(username='张三', password='111')
    # 2. 将ORM对象添加到db.session中
    db.session.add(user)
    # 3. 将db.session中的改变同步到数据中
    db.session.commit()
    return '用户表格内容添加成功！'

@app.route('/query')
def query_user():
    # 1. get查找：根据主键查找
    user = User.query.get(1)
    print(f'{user.id}: {user.username}--{user.password}')
    
    # 2. filter_by查找
    # Query: 类数组
    users = User.query.filter_by(username='张三')
    for i in users:
        print(i.id,i.username,i.password)
    return '数据查询成功！'

@app.route('/update')
def update_user():
    user = User.query.filter_by(id=1)[0]
    user.password = '222'
    db.session.commit()
    return '数据修改成功！'

@app.route('/delete')
def del_user():
    user = User.query.filter_by(id=1)[0]
    # 从db.session中删除
    db.session.delete(user)
    # 同步数据库
    db.session.commit()
    return '数据删除成功！'

@app.route('/')
def hello_world():
    return '111'

if __name__ == '__main__':
    app.run(debug=True)


    # 映射数据库中原有的表格
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)
    StudentScore = Base.classes.student_scores  # 直接获取映射类
    session = Session(db.engine)
    data = session.query(StudentScore).all()
    result = [dict(row.__dict__) for row in data]
    print(result[1])