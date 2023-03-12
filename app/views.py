"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""

import os

from app import app, db
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask.helpers import send_from_directory

from app.forms import PropertyForm
from app.models import Property



###
# Routing for your application.
###
def get_uploaded_images():
    upload_dir = app.config.get('UPLOAD_FOLDER')
    return sorted(os.listdir(upload_dir))

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/properties/create/', methods=['GET', 'POST'])
def add_property():
    """Form for adding properties"""
    form = PropertyForm()

    if request.method == 'POST':
        if form.validate_on_submit():
           
            title = form.title.data
            description = form.description.data
            num_bedrooms = form.num_bedrooms.data
            num_bathrooms = form.num_bathrooms.data
            price = form.price.data
            location = form.location.data
            property_type = form.property_type.data
            photo = form.photo.data
            photo_upload = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_upload))

            
            property_model = Property(
                title=title,
                description=description,
                num_bedrooms=num_bedrooms,
                num_bathrooms=num_bathrooms,
                price=price,
                location=location,
                property_type=property_type,
                photo = photo_upload)

            db.session.add(property_model)
            db.session.commit()

        
            flash('Property successfully saved', 'success')
            return redirect(url_for('get_properties'))
        flash_errors(form)
    return render_template('property.html', form=form)


@app.route('/properties')
def get_properties():
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)

@app.route('/uploads/<filename>')
def get_image(filename):
    print(filename)
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

@app.route("/property/<property_id>")
def view_property(property_id):
    # Retrieve the property with the matching id
    prop = Property.query.filter_by(id=property_id).first()

    # Construct the URL for the property's photo
    if prop.photo is not None:
        photo_url = url_for('get_image', filename=prop.photo) 
    else:
        photo_url = None
    
    # Pass the property and photo URL to the template
    return render_template("view_property.html", prop=prop, photo_url=photo_url)



###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
