from flask_sqlalchemy import SQLAlchemy

# 数据库配置
# Postgresql主机名称
HOSTNAME = '172.31.136.83'
# 监听端口
POST = '5432'
# 连接用户名
USERNAME = 'postgres'
# 连接密码
PASSWORD = 'hbxt9688'
# 连接数据库的名称
DATABASE = 'qa_web'
DB_URI = f'postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{POST}/{DATABASE}'
SQLALCHEMY_DATABASE_URI = DB_URI



# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "913614489@qq.com"
MAIL_PASSWORD = "nuntofcfcqrabbfi"
MAIL_DEFAULT_SENDER = "913614489@qq.com"
# nuntofcfcqrabbfi


