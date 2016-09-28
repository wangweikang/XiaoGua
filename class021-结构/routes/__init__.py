from functools import wraps

from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for

# from models.board import Board
# from models.user import User

# 不加这一行会导致 mapper exception
#
# main = Blueprint('main', __name__)
#
#
# @main.route('/')
# def index_view():
#     return redirect(url_for('todo.index'))
