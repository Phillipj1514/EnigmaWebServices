import os
import datetime
from app import app
from flask import render_template, request, redirect, url_for, flash,abort, jsonify,g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from .forms  import *
from app.models import *

@app.route('/api/register', methods=['POST'])
def merchantRegister():
    merchantRegForm = merchantRegister(csrf_enabled=False)
    submission_errors = []
    if request.method == 'POST' and merchantRegForm.validate_on_submit():
        success = True
        name = merchantRegForm.name.data
        address = merchantRegForm.address.data
        location = merchantRegForm.location.data
        email = merchantRegForm.email.data
        estTime = merchantRegForm.estWaitTime
        logo  = merchantRegForm.logo.data
        logo_name = secure_filename(logo.filename)

        password = merchantRegForm.password.data
        confirmed_password  = merchantRegForm.confirm_password.data 

        if(password != confirmed_password): 
            success = False
            submission_errors.append("password and confirm passowrd is different")
        if(not Merchant.query.filter_by(name=name).first() is None): 
            success = False
            submission_errors.append("Company name unavailable")
        if( not Users.query.filter_by(email=email).first() is None):
            success = False
            submission_errors.append("email already used")
        # Save the data if the information entered is valid and new 
        if(success):
            profile_photo.save(os.path.join(
                app.config['UPLOAD_FOLDER'],logo_name
            ))
            merchant  = Merchant(name,address,location,logo_name, email,password,estTime, datetime.datetime.now())
            db.session.add(merchant)
            db.session.commit()
            return successResponse({"message": "Merchant  successfully registered"}),201
    # If the form fail to submit it returns an error message
    return errorResponse(form_errors(merchantRegForm)+submission_errors),400

def successResponse(message):
    return jsonify(message )

def errorResponse(error):
    return jsonify(error=error)
