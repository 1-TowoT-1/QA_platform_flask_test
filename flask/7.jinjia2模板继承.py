# 在一个网站里面大部分网页得模板都是重复的，所以为了避免臃肿，通常通过模板继承，把一些重复的代码写在父模板中，子模版继承父模板。


# 基础模板（base.html）
# 在 base.html 中，使用 {% block %} 定义可被子模板覆盖的区域，{% block title %}内容{% endblock %}
# 基模板可以包含多个 block，子模板可以选择是否覆盖：
# {% block sidebar %}默认侧边栏{% endblock %}
# {% block sidebar %}
#     <p>自定义侧边栏</p>
# {% endblock %}

################################################################################################################
# 子模板（child.html）
# child.html 继承 base.html，并填充 block 区域：
# {% extends "base.html" %}
# {% block title %}主页 - 我的网站{% endblock %}
# {% block content %}
#     <h2>欢迎来到我的主页</h2>
#     <p>这里是主页内容。</p>
# {% endblock %}


# super() 关键字
# 如果子模板希望在 block 内部保留 base.html 的部分内容，可以使用 {{ super() }}：
# {% block content %}
#     {{ super() }}
#     <p>这里是额外的内容。</p>
# {% endblock %}


################################################################################################################
# 静态加载文件
# 在 base.html 中：
# <head>
#     <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
#     {% block extra_head %}{% endblock %}
# </head>
# 在 child.html 中：
# {% block extra_head %}
#     <script src="{{ url_for('static', filename='script.js') }}"></script>
# {% endblock %}


from flask import Flask,render_template

app = Flask(__name__)

class User():
    def __init__(self, username, email):
        self.username = username
        self.email = email

# 字典访问，类访问
@app.route('/')
def hello_world():
    user = User(username='陈平安', email="测试@111.com")
    person = {
        "username" : "张三",
        "email" : "zhangsan@qq.com",
    }
    return render_template("index.html",user=user,person=person) 


@app.route('/child1')
def child():
    return render_template("child1.html")

@app.route('/child2')
def child2():
    return render_template("child2.html")

if __name__ == "__main__":
    app.run(debug=True)