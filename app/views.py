from app import app
from flask import render_template, request, redirect, url_for, flash
from .forms import ContactForm
from app import mail
from flask_mail import Message 

###
# Routing for your application.
###

@app.route('/',methods=['GET', 'POST'])
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/contact')
def contact():
    """Render the website's contact page."""
    contactForm = ContactForm()
    print("Class created")

    if request.method == 'POST':
        print("Is a Post request")
        if contactForm.validate_on_submit():
            print("Form validated")
            # Note the difference when retrieving form data using Flask-WTF
            # Here we use myform.firstname.data instead of request.form['firstname']
            name = contactForm.name.data
            email = contactForm.email.data
            subject = contactForm.subject.data
            message = contactForm.message.data

            msg = Message(subject,
            sender=(name, email),
            recipients=["akelebenjamin.ab@gmail.com"])
            msg.body = message
            print("Msg composed")
            mail.send(msg) 
            print("Mail Sent")
            flash('Email sent successfully')
            print("Mail Flashed")
            return render_template('home.html')

        flash_errors(contactForm)
    return render_template('contact.html', form=contactForm)
    

###
# The functions below should be applicable to all Flask apps.
###


# Flash errors from the form if validation fails
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
