from flask import Flask,session,g #g flask中的全局
import config
from exts import db,mail
from models import UserModel
from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp
from flask_migrate import Migrate

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

# 将db导入app中
migrate = Migrate(app, db)

# blueprint是用来模块化的
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

# 钩子函数：before_request / before_first_request / after_request
@app.before_request
def my_before_request():
    # session 是 Flask 提供的用户会话对象，底层通过 cookie 储存数据。
    user_id = session.get('user_id')
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}


if __name__ == '__main__':
    app.run(debug=True)