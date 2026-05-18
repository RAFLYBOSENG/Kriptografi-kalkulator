from flask import Blueprint, render_template
from ..services import history_service

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/history")
def history():
    hist = history_service.load_history()
    return render_template("history.html", history=hist)
