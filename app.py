from myproject import app,db
from flask import render_template,redirect,request,url_for,flash,abort, g , Flask
from flask_login import login_user,login_required,logout_user, UserMixin
import flask_login
from myproject.models import User, Missing, Crime, Complaint
from myproject.forms import LoginForm,RegistrationForm,Adminlogin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug import secure_filename
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import shutil
#from myproject.databases import Missing
#from myproject.forms import MissingReportsForm


admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Missing,  db.session))
admin.add_view(ModelView(Crime, db.session))
admin.add_view(ModelView(Complaint, db.session))



@app.route('/')
def home():
    global user_id
    if(flask_login.current_user.is_authenticated==True):
        user_id = flask_login.current_user.id

    return render_template('home.html')

@app.route('/welcome' , methods = ['POST', 'GET'])  #decorator
@login_required
def welcome_user():
        return render_template('welcome_user.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('home'))

@app.route('/login',methods = ['GET','POST'])
def login():
     form = LoginForm()
     if form.validate_on_submit():
         user = User.query.filter_by(email = form.email.data).first()

         if user.check_password(form.password.data) and user is not None:
             login_user(user)
             flash('Logged in successfully')
             next = request.args.get('next')   #if user is trying to go to page which required login we can use next
# checking if next exist otherwise we go to welcone user page
             if next == None or not next[0] == '/':
                 next = url_for('welcome_user')

             return redirect(next)

     return render_template('login.html',form=form)


@app.route('/register',methods = ['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)

        db.session.add(user)   #adding user to our database
        db.session.commit()   #saving the changes made in database
        flash("Thanks for registration!")
        return redirect(url_for('login'))
    return render_template('register.html',form=form)

@app.route('/reports',methods = ['GET','POST'])
def reports():
    if flask_login.current_user.is_authenticated:
        return render_template('oc.html')
    return 'not logged in '

@app.route('/crime')
def crime_rep():
    if flask_login.current_user.is_authenticated:
        return render_template('crime.html')
    return 'not logged in'

@app.route('/complaint')
def complaint():
    if flask_login.current_user.is_authenticated:
        return render_template('compl.html')
    return 'not logged in '

@app.route('/missing')
def missing():
    if flask_login.current_user.is_authenticated:
        return render_template('mis.html')
    return 'not logged in'

@app.route('/uploaded_compl' , methods = ['GET' , 'POST'])
def index_compl():
    if request.method=='POST':
        if(request.form['name'] and request.form['date'] and request.form['descr']):
            obj = Complaint(request.form['name'] , request.form['date'] , request.form['descr'],  "pending", flask_login.current_user.id)
            db.session.add(obj)
            db.session.commit()
            return render_template("success.html")

@app.route('/uploaded_crime' , methods = ['GET' , 'POST'])
def index_crime():
    if request.method=='POST':
        if(request.form['name'] and request.form['date'] and request.form['descr']):
            obj = Crime(request.form['name'] , request.form['date'] , request.form['descr'],  "pending", flask_login.current_user.id)
            db.session.add(obj)
            db.session.commit()
            return render_template("success.html")

@app.route('/uploaded' , methods = ['GET' , 'POST'])
def index_missing():
    if request.method=='POST':
        if(request.form['name'] and request.form['date'] and request.form['descr'] and request.form['PIN'] and request.files['file']):

            f = request.files['file']
            f.save(secure_filename(f.filename))
            shutil.move("/home/delta7/Desktop/Py_Project/" + f.filename , "/home/delta7/Desktop/Py_Project/myproject/static/images/" + f.filename)
            obj = Missing(request.form['name'] , request.form['date'] , request.form['descr'] ,request.form['PIN'] , f.filename , "pending", flask_login.current_user.id)
            db.session.add(obj)
            db.session.commit()
            return render_template("success.html")
        #alert('Please fill all fields')
        return redirect('/')
@app.route('/missing_rep')
def display_miss():
    if flask_login.current_user.is_authenticated:
        return render_template('dash_miss.html', input = Missing.query.filter_by(user_id = flask_login.current_user.id).all())
    return redirect(url_for('login'))

@app.route('/compls')
def display_compl():
    if flask_login.current_user.is_authenticated:
        return render_template('dash_compl.html', input = Complaint.query.filter_by(user_id = flask_login.current_user.id).all())
    return redirect(url_for('login'))

@app.route('/crimes')
def display_crime():
    if flask_login.current_user.is_authenticated:
        return render_template('dash_crimes.html', input = Crime.query.filter_by(user_id = flask_login.current_user.id).all())
    return redirect(url_for('login'))

@app.route('/post' ,  methods = ['GET' , 'POST'])
def display():
    if request.method=='POST':
        return render_template('missing_dis.html' , input = Missing.query.filter_by(PIN = request.form['sub_pin']).all())
    return render_template('missing_dis.html' , input = Missing.query.all())


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect("http://127.0.0.1:5000/admin/")
    return render_template('adminlogin.html', error=error)

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
