from flask import Blueprint,request,render_template,g,redirect,url_for
from .forms import QuestionForm,AnswerForm
from models import QuestionModel,AnswerModel
from exts import db
from decorator import login_required

# /
bp = Blueprint("qa", __name__, url_prefix="/")

# 首页
@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template("index.html", questions=questions)

@bp.route("/qa/public", methods=['GET','POST'])
@login_required
def public_qa():
    if request.method == 'GET':
        return render_template("question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            author_name = g.user.username
            question = QuestionModel(title=title,content=content,author_name=author_name,author=g.user)

            db.session.add(question)
            db.session.commit()

            # todo：跳转到这篇问答的详情页
            return redirect("/")
        else:
            print(form.errors)
            return redirect("qa.public_qa")
        

@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    comments = question.answer # 利用 backref 获取该问题下的所有回答（按时间倒序）
    return render_template("detail.html", question=question, comments=comments)


# @bp.route("/answer/public", methods=['POST'])
@bp.post("/answer/public")
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))


@bp.route("/search")
def search():
    # /search?q=flask
    # /search/<q>
    # post, request.form
    q = request.args.get("q")
    search_contents = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("index.html", questions=search_contents)