from flask import Blueprint

# /
bp = Blueprint("qa", __name__, url_prefix="/")

# 首页
@bp.route("/")
def index():
    pass