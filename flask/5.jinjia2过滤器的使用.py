from flask import Flask,render_template
from datetime import datetime

app = Flask(__name__)

class User():
    def __init__(self, username, email):
        self.username = username
        self.email = email

### 自定义过滤器：
def datetime_format(value, format="%Y年%m月%d日\t时间:(%H:%M)"):
    return value.strftime(format)  
# 添加自定义过滤器：
app.add_template_filter(datetime_format,"dformat") ## 其中dformat是在模板中调用该过滤器的名字


# 字典访问，类访问
@app.route('/')
def hello_world():
    user = User(username='陈平安', email="测试@111.com")
    person = {
        "username" : "张三",
        "email" : "zhangsan@qq.com",
    }
    return render_template("index.html",user=user,person=person) # 渲染html模板，会在templates文件夹中寻找的html文件。
# render_template这个函数底层就是调用的jinjia2模板

@app.route('/filter')
def filter():
    user = User(username='陈平安', email="测试@111.com")
    mytime = datetime.now()
    return render_template("filter.html", user=user, mytime=mytime)


if __name__ == "__main__":
    app.run(debug=True)