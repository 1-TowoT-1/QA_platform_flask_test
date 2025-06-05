import wtforms
from wtforms.validators import Email,Length,EqualTo,InputRequired
from models import UserModel,EmailCaptchaModel
from exts import db
# 验证器：Email(邮箱验证),Length(长度验证),EqualTo(值是否相等)

# From：主要是验证前端提交数据是否符合要求
# 这里表单的命名要与前端页面的name属性一致才能检测的到
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=6,max=6,message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3,max=20,message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    # 自定义验证
    # 1. 邮箱是否已经被注册
    # validate_字段名(self, field) 就会自动绑定到对应的字段。
    # field 是一个 wtforms 内部传入的参数，代表 当前正在验证的字段对象。
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")
        
    # 2. 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        # EmailCaptchaModel.query.filter_by(email="18342771706@163.com",captcha="293754").first().__dict__可以看到字典内容
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first() # 返回查找ORM对象
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱验证码错误！")
        # else:
        #     db.session.delete(captcha_model)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误！")])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3,max=100,message="标题格式错误！")])
    content = wtforms.StringField(validators=[Length(min=3,message="内容格式错误！")])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3,message="内容格式错误！")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="必须要传入问题ID！")])