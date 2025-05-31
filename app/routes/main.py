from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('main/index.html')

@main.route('/rooms')
@login_required
def rooms():
    return render_template('main/rooms.html')

@main.route('/samples')
@login_required
def samples():
    return render_template('main/samples.html')
