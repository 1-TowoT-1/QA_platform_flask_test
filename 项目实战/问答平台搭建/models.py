from exts import db
from datetime import datetime # 调用datetime包中的datetime类

def now_without_microseconds():
    return datetime.now().replace(microsecond=0)
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=now_without_microseconds)


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)



class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.String(100),nullable=False)
    author_name = db.Column(db.String(20),nullable=False)
    create_time = db.Column(db.DateTime, default=now_without_microseconds)
    # 设置外键，并且设置级联删除： ondelete='CASCADE'，relationship需要开启passive_deletes=True
    author_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))
    author = db.relationship(UserModel, backref="questions", passive_deletes=True)


class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(100),nullable=False)
    create_time = db.Column(db.DateTime, default=now_without_microseconds)

    # 增加外键，答案是回复哪个问题，问题的ID
    question_id = db.Column(db.Integer, db.ForeignKey("question.id",ondelete='CASCADE'))
    # 增加外键，答案是谁回复的，user用户ID
    author_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'))

    # 关系
    question = db.relationship(QuestionModel, backref=db.backref("answer", order_by=create_time.desc()), passive_deletes=True)
    author = db.relationship(UserModel, backref="answer", passive_deletes=True)