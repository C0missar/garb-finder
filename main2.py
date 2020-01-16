from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://garb-finder:garb-finder@localhost:8889/garb-finder'
app.config['SQLALCHEMY_ECHO'] = True 
app.config['SECRET_KEY'] = "Your_secret_string"
db = SQLAlchemy(app)

class User (db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
#   saved_item = db.relationship("Item", backref = "owner")


    def __init__(self, username, password):
        self.username = username
        self.password = password


class Item (db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    # description = db.Column(db.String(2000))
    # culture = db.Column(db.String(120))
    # climate = db.Column(db.String(120))
    # gender = db.Column(db.String(120))
    # item_type = db.Column(db.String(120)) 
    # time_period_start = db.Column(db.Integer)
    # time_period_end = db.Column(db.Integer)
   
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, name, owner):
    # , description, culture, climate, gender, item_type, time_period_start, time_period_end
        self.name = name
        self.owner = owner
        # self.description = description
        # self.culture = culture
        # self.climate = climate
        # self.gender = gender
        # self.item_type = item_type
        # self.time_period_end = time_period_start
        # self.time_period_end = time_period_end
       

 
class Climate (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name


@app.route("/login", methods=['GET', 'POST'])
def login():
    incorrect_info=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        incorrect_info=""
        q_user = User.query.filter_by(username=username).first()
        print("==== /login q_user = ",q_user)
        error_bool=False
        if q_user:
            if password != q_user.password:
                incorrect_info = "Incorrect username or password"
                error_bool=True
        else:
            incorrect_info = "Incorrect username or password"
            error_bool=True    
        if error_bool == False:
            session['user'] = username
            print("==== /login redirect to /saved_items")
            return redirect('/saved_items')
        else:
            return render_template("login.html", incorrect_info=incorrect_info)    
    return render_template("login.html")
    
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    mismatch=""
    bad_password=""
    bad_username=""
    other_username=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        taken_username=User.query.filter_by(username=username).count()
        error_bool=False
        if verify != password:
            mismatch="These passwords do not match."
            error_bool=True
        if len(password) <3:
            bad_password="Please enter a password that is at least 3 characters long"
            error_bool=True
        if len(username) <3:
            bad_username="Please enter a username that is at least 3 characters long"    
            error_bool=True
        if taken_username > 0:
            other_username="This username has already been taken.  Please pick another one."
            error_bool=True
        if error_bool == False:  
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            session["user"] = username
            return redirect('/home')
        else:
            return render_template("signup.html", mismatch=mismatch, bad_password=bad_password, bad_username=bad_username, other_username=other_username)
    else: 
        return render_template("signup.html")

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'home', 'index']
    if request.endpoint not in allowed_routes and 'user' not in session:
    # restricted_routes = ['saved_items']
    # if request.endpoint in restricted_routes and 'user' not in session:
        print("==== / redirect to /login")
        return redirect('/login')

@app.route('/logout')
def logout():
    if "user" in session:
        del session['user']
    print("==== /logout redirect to /home")
    return redirect('/home')

@app.route('/home')
def avocado():
    print("==== /home")
    return render_template("home.html")

@app.route('/index', methods=['POST', 'GET'])
def index():
    print("==== /index")
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/saved_items', methods=['POST', 'GET'])
def my_stuff():
    print("==== /saved_items",request.method)
    if request.method == 'POST':
        item_name = request.form['item']
        print("==== saved_items before User.query, item_name=",item_name)
        user = User.query.filter_by(username=session['user']).first()
        owner=user.id
        print("==== user")
        print(user)
        print("==== owner")
        print(owner)
        print("==== saved_items after User query, owner=",owner)
        new_item = Item(item_name, owner)
        db.session.add(new_item)
        print("==== saved_items after add",item_name,owner)
        db.session.commit()
        print("==== saved_items after commit",item_name,owner)

    print("==== /saved_items before Item.query")
    items = Item.query.filter_by(owner=session['user']).all()
    print("==== /saved_items after Item.query")
    return render_template("saved_items.html", items=items)

# @app.route("/welcome")
# def welcome_in():
#     username = request.args.get("username")  
#     return render_template("welcome.html", username=username)

@app.route("/")
def default():
    return redirect("/home")
 
if __name__ == "__main__":
    app.run()