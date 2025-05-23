from flask import Blueprint,render_template,request,jsonify,redirect,url_for,session # redirect重定向
from exts import mail,db
from flask_mail import Message
import random
from models import EmailCaptchaModel,UserModel
from blueprints.forms import RegisterForm,LoginForm # 或者使用同级目录相对路径导入：from .forms import RegisterForm
# password不能直接保存password，因为这里是明文密码，如果数据库被盗取了，那么就会造成用户信息流失。
from werkzeug.security import generate_password_hash,check_password_hash

# /auth
bp = Blueprint("auth", __name__, url_prefix="/auth")

# /auth/login
@bp.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在！")
                return redirect(url_for("auth.login"))
            if check_password_hash(pwhash=user.password, password=password):
                # cookie：cookie中不适合存储大量数据，一般用来存放登录授权内容
                # flask中的session是经过加密处理存储在cookie当中的
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("密码错误！")
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))
        

@bp.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("regist.html")
    else:
        # 验证用户邮箱和验证码是否对应和正确
        # 表单验证：flask-wtf：wtforms
        form = RegisterForm(request.form)
        form.validate() # 该类继承的wtforms.Form内部方法自己可以调用所需检查的验证器。
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # 创建账户后重定向到登录界面
            return redirect(url_for("auth.login")) #这里的login是视图函数的名字，也可以写成redirecet("/auth/login")
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))

# 发送验证码
# 如果没有指定，bp.route默认的是get请求
@bp.route("/captcha/email")
def get_email_captcha():
    # /captcha/email/<email>
    # /captcha/email?email=xxx@qq.com
    email = request.args.get("email")
    code = random.randint(100000,999999)
    message = Message(subject="测试验证码", recipients=[email], body=f"您的验证码是：{code}")
    mail.send(message)

    # 记录验证码，核验邮箱和验证码是否正确，后期可以用redis或者其他方式进行管理。
    email_captcha = EmailCaptchaModel(email=email, captcha=code)
    db.session.add(email_captcha)
    db.session.commit()

    return jsonify({"code":200, "message":"", "data":None})