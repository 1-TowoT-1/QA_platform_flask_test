from flask import Flask,request

### url和视图
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello adasd'

# 定义路由路径。可以在ip后面加/zidong来查看该路由下的内容
@app.route('/zidong')
def zhuzhu():
    return '空间！'

# 带参数的url，参数定义类型
@app.route('/blog/<int:blog_id>')
def blog(blog_id):
    return "博客空间ID：%s"%blog_id

# 查询字符串方式传参，在url中传参默认是'?'，例如要访问页面www.baidu.com?page=2
@app.route('/book_list')
def book_list():
    page = request.args.get("page", default=1, type=int)
    return f'书库页码：{page}'


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5001)