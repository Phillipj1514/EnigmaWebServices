import os
import datetime
from app import app
from flask import render_template, request, redirect, url_for, flash,abort, jsonify,g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
#from .forms  import profileForm
from app.models import *

@app.route('/api/register', methods=['POST'])
def merchantRegister():
    return successResponse({"successs":"hurray"})

def successResponse(message):
    return jsonify(message )

def errorResponse(error):
    return jsonify(error=error)
