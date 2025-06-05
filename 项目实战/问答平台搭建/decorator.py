
from functools import wraps
from flask import g,redirect,url_for

def login_required(func):
    # 保留传递进来的func信息
    @wraps(func)
    def inner(*args,**kwargs): # *args接收位置参数，**kwargs接收关键字参数。func(1,2,c=3)，其中1，2是位置参数，c=3是关键字参数。
        if g.user:
            return func(*args,**kwargs)
        else:
            return redirect(url_for("auth.login"))
    return inner

        

