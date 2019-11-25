from flask import Flask , render_template , request
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
import shutil

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///persons.sqlite3"
app.config['SECRET_KEY'] = 'random string'
app.config['UPLOAD_FOLDER'] = "/static"

db = SQLAlchemy(app)
class Person(db.Model):
    complaint_id = db.Column('comp_id' , db.Integer , primary_key = True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    height = db.Column(db.String)
    last_add = db.Column(db.String)
    last_PIN = db.Column(db.String)
    img = db.Column(db.String)

    def __init__(self , name , age , height , last_add , last_PIN , img):
        self.name = name
        self.age = age
        self.height = height
        self.last_add = last_add;
        self.last_PIN = last_PIN;
        self.img = img

    def __repr__(self):
        return f"Missing ({self.name} , {self.age} , {self.height} , {self.last_add} , {self.last_PIN} , {self.img})"

@app.route('/')
def upload():
    return render_template('missing.html')

@app.route('/uploaded' , methods = ['GET' , 'POST'])
def index():
    if request.method=='POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        shutil.move("/home/delta7/Desktop/Py_Project/" + f.filename , "/home/delta7/Desktop/Py_Project/static/images/")
        obj = Person(request.form['name'] , request.form['age'] , request.form['height'] , request.form['last_add'] ,request.form['PIN'] , f.filename)
        db.session.add(obj)
        db.session.commit()
        return 'success'
@app.route('/post' ,  methods = ['GET' , 'POST'])
def display():
    if request.method=='POST':
        return render_template('missing_dis.html' , input = Person.query.filter_by(last_PIN = request.form['sub_pin']).all())
    return render_template('missing_dis.html' , input = Person.query.all())

@app.route('/enter_pin')
def display_page():
    return render_template("check_pin.html")
if __name__=='__main__':
    db.create_all()
    app.run(debug = True)
