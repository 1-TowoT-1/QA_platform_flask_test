from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html") # 渲染html模板，会在templates文件夹中寻找的html文件。
# render_template这个函数底层就是调用的jinjia2模板

# 传参
@app.route('/blog_id/<blog_id>_<username>')
def blog_detail(blog_id, username):
    return render_template("blog.html", blog_id2=blog_id, username2=username)


if __name__ == "__main__":
    app.run(debug=True)

