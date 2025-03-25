from flask import Flask

# 使用flask类创建一个app对象
# __name__：代表当前app.py这个模块
# 1. 以后出现bug，它可以帮助我们快速定位
# 2. 对于寻找模块文件，有一个相对路径
app = Flask(__name__)

# 创建一个路由和视图函数的映射。'/'表示根路由（可以类比linux中的根目录'~'）。
@app.route('/')
def hello_world():
    return 'Hello adasd'

# 1. debug模式
# 这里的debug模式调用的是flask内部的debug而非vscode本身的debug模式。所以app加上debug=True，直接运行即可。 

# 2. 修改host模式
# 局域网内部访问，vscode在run里面加入host=0.0.0.0或者自己的IP地址

# 3. 修改port模式
# 改变端口号，如果端口号被别人占用，可以进行更改。

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5001)