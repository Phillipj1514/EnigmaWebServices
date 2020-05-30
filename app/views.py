import os, datetime
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash,abort, jsonify,g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from .forms  import *
from app.models import *



###
# Routing for your application.
###
# The Api fopr the system 
from app import api

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about')
def about():
    """Render profile creation page for the website"""
    return render_template('about.html')

@app.route('/registration', methods=['POST', 'GET'])
def registration():
    """Render registration creation for the website"""
    merchantRegForm = MerchantRegistration()
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
            merchant = Merchant.query.filter_by(email=email).first()
            if(not merchant is None):
                line = Line(merchant.id,"",0,merchant.estimatedWaitTime)
                db.session.add(line)
                db.session.commit()
            flash("Account created successfully", "success")
    # If the form fail to submit it returns an error messag
        flash_errors(merchantRegForm)
    return render_template('registration.html', form = merchantRegForm)

# Page to login user
@app.route('/login', methods=['POST', 'GET'])
def login():
    merchantLogin = MerchantLogin()
    submission_errors = []
    if request.method == 'POST' and merchantLogin.validate_on_submit():
        success = True
        email = merchantLogin.email.data
        password = merchantLogin.password.data
        merchant = Merchant.query.filter_by(email=email).first()
        if merchant is not None and check_password_hash(merchant.password, password):
            # On successfuly verification create the user payload with the user id 
            # and generate the user token
           login_user(merchant)
           flash("login successful", 'success')
           return redirect(url_for('dashboard'))
        else:
        # Add user validation error
            submission_errors.append("email or password invallid")
            flash(submission_errors, 'danger')
    flash_errors(merchantLogin)
    return render_template('login.html', form = merchantLogin)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    merchant_id = current_user.id
    merchant = Merchant.query.filter_by(id=merchant_id).first()
    line =  Line.query.filter_by(merchantID=merchant_id).first()
    lineDetails = {}
    mDetail = {}
    if(not line is None):
        customerInLine = []
        customers = line.queue.split(",")
        customers = [int(i) for i in customers if i.isdigit()] 
        for customerID in customers:
            customer = Customer.query.filter_by(id=int(customerID)).first()
            if(not customer is None):
                cDetails={
                    "id":customer.id,
                    "merchantID": customer.merchantID,
                    "queueID": customer.queueID,
                    "code": customer.code,
                    "position": customer.position,
                    "wait_time": customer.waitTime
                }
                customerInLine.append(cDetails)

        lineDetails = {
            "merchantID": line.merchantID,
            "id": line.id,
            "default_wait_time":line.waitTime,
            "count": line.count,
            "queue": customerInLine
        }
    if(not merchant is None ):
        logofile = "uploads/"+merchant.logo
        mDetail = {
            "id": merchant.id,
            "name": merchant.name,
            "address": merchant.address,
            "location": merchant.location,
            "logo_image":url_for('static', filename=logofile, _external=True),
            "email": merchant.email,
            "estimated-Wait-Time":merchant.estimatedWaitTime,
            "joined-on": merchant.joined_on.strftime("%m/%d/%Y, %H:%M:%S"),
            "line": lineDetails
        }

    return render_template('dashboard.html', details = mDetail)

@app.route('/checkTicket',  methods=['POST', 'GET'])
@login_required
def checkTicket():
    checkingForm = TicketCheck()
    if request.method == 'POST' and checkingForm.validate_on_submit():
        customer_code = ""
        if not checkingForm.qrcode.data  is None:
            qrcode = checkingForm.qrcode.data
            qrcode_name = secure_filename(qrcode.filename)

        if not checkingForm.customer_code.data is None:
            customer_code = checkingForm.customer_code.data
        # processing
        merchant_id = current_user.id
        merchant = Merchant.query.filter_by(id=merchant_id).first()
        line =  Line.query.filter_by(merchantID=merchant_id).first()
        customer = Customer.query.filter_by(code=customer_code).first()
        if(not customer is None):
            if(customer.merchantID == merchant_id):
                if customer.waitTime == 0:
                    if(not line is None):
                        customerInLine = []
                        customers = line.queue.split(",")
                        customers.remove(str(customer.id))
                        # update the system with new line count
                        line.queue = ",".join(customers)
                        line.count-=1
                        db.session.commit()
                        # Delete the current customer from the queue
                        db.session.delete(customer)
                        db.session.commit()
                        customers = [int(i) for i in customers if i.isdigit()] 
                        for customerID in customers:
                            customer = Customer.query.filter_by(id=int(customerID)).first()
                            customer.position-= 1
                            customer.waitTime-=line.waitTime
                            db.session.commit()
                        flash("Customer can be allowed on the inside", "success")
                else:
                    flash("The customer is too early", "danger")
            else:
                flash("Invalid Client / Wrong store","danger")
        else:
            flash("Invalid Client","danger")
    
    flash_errors(checkingForm)
    return render_template('checkTicket.html', form= checkingForm)

@app.route('/chat/<customer_id>',methods=['POST', 'GET'])
@login_required
def clientsupport(customer_id):
    messageForm = MessageForm()
    msgs = []
    customer = Customer.query.filter_by(id=customer_id).first()
    chat = Chats.query.filter_by(id=customer.chatID).first()
    if(not chat is None):
        msg = chat.messages.split(",")
        if request.method == 'POST' and messageForm.validate_on_submit():
            message = messageForm.message.data
            msgs.append(msg)
            chat.messages = ",".join(msgs)
            db.session.commit()
        flash_errors(messageForm)
    return render_template('clientsupport.html', form = messageForm, messages= msgs)

# @app.route('/profile', methods=['POST', 'GET'])
# def profile():
#     """Render profile creation page for the website"""
#     profileform = profileForm()
#     if request.method == 'POST' and profileform.validate_on_submit():
#         fname  = profileform.first_name.data
#         lname = profileform.last_name.data
#         gender = profileform.gender.data
#         email = profileform.email.data
#         location = profileform.location.data
#         biography = profileform.biography.data
#         profileImage = profileform.image.data
#         image_name = secure_filename(profileImage.filename)
#         profileImage.save(os.path.join(
#             app.config['UPLOAD_FOLDER'], image_name
#         ))
#         create_time = datetime.datetime.now()

#         newProfile = Profiles(fname,lname,gender, email, location, biography, image_name, create_time)
#         db.session.add(newProfile)
#         db.session.commit()  
#         flash("profile added successfully", "success")
#         return redirect(url_for("profiles"))
#     else:
#         flash_errors(profileform)
#     return render_template('profile.html', form = profileform)

# @app.route('/profiles')
# def profiles():
#     """Render page to show all profiles"""
#     uprofiles = db.session.query(Profiles).all()
#     return render_template('profiles.html', profiles = uprofiles)

# @app.route('/profile/<id>')
# def userProfile(id):
#     """Renders the profile for a specific user ID that is entered"""
#     uprofile = Profiles.query.get(id)
#     return render_template('userprofile.html', profile = uprofile)


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return Merchant.query.get(int(id))

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
