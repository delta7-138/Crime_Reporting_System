from flask import Flask , render_template , url_for

app = Flask(__name__)
@app.route('/')
def index():
    return render_template("home.html")
@app.route('/link1')
def link_1():
    return render_template("link1.html")
if __name__=='__main__':
    app.run(debug = True)
