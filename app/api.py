import os
import datetime
from app import app
from flask import render_template, request, redirect, url_for, flash,abort, jsonify,g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from .forms  import *
from app.models import *

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/api/register', methods=['POST'])
def merchantRegister():
    merchantRegForm = MerchantRegistration(csrf_enabled=False)
    submission_errors = []
    if request.method == 'POST' and merchantRegForm.validate_on_submit():
        success = True
        name = merchantRegForm.name.data
        address = merchantRegForm.address.data
        location = merchantRegForm.location.data
        email = merchantRegForm.email.data
        estTime = merchantRegForm.estWaitTime.data
        logo  = merchantRegForm.logo.data
        logo_name = secure_filename(logo.filename)

        password = merchantRegForm.password.data
        confirmed_password  = merchantRegForm.confirmPassword.data 

        if(password != confirmed_password): 
            success = False
            submission_errors.append("password and confirm passowrd is different")
        if(not Merchant.query.filter_by(name=name).first() is None): 
            success = False
            submission_errors.append("Company name unavailable")
        if( not Merchant.query.filter_by(email=email).first() is None):
            success = False
            submission_errors.append("email already used")
        # Save the data if the information entered is valid and new 
        if(success):
            logo.save(os.path.join(
                app.config['UPLOAD_FOLDER'],logo_name
            ))
            merchant = Merchant(name, address, location, logo_name, email, password, estTime, datetime.datetime.now())
            db.session.add(merchant)
            db.session.commit()
            return successResponse({"message": "Merchant  successfully registered"}),201
    # If the form fail to submit it returns an error messag
    return errorResponse(form_errors(merchantRegForm)+submission_errors),400

@app.route('/api/login', methods=['POST'])
def merchantLogin():
    merchantLogin = MerchantLogin(csrf_enabled=False)
    submission_errors = []
    if request.method == 'POST' and merchantLogin.validate_on_submit():
        success = True
        email = merchantLogin.email.data
        password = merchantLogin.password.data
        merchant = Merchant.query.filter_by(email=email).first()
        if merchant is not None and check_password_hash(merchant.password, password):
            # On successfuly verification create the user payload with the user id 
            # and generate the user token
            # payload = {"userid":user.id,"time":datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
            # token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
            # return successResponse({'message':username+"Merchant successfully logged in.",
            #                             'token':token})
             return successResponse({'message':"Merchant successfully logged in."})
        # Add user validation error
        submission_errors.append("email or password invallid")
    return errorResponse(form_errors(merchantLogin)+submission_errors)

def successResponse(message):
    return jsonify(message )

def errorResponse(error):
    return jsonify(error=error)
