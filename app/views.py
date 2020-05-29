import os, datetime
from app import app
from flask import render_template, request, redirect, url_for, flash,abort, jsonify,g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
#from .forms  import profileForm
from app.models import *



###
# Routing for your application.
###

from app import api

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about')
def about():
    """Render profile creation page for the website"""
    return render_template('about.html')



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
