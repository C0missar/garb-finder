from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://garb-finder:garb-finder@localhost:8889/garb-finder'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = "Your_secret_string"
db = SQLAlchemy(app)

class User (db.Model):

    # id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), primary_key=True)
    password = db.Column(db.String(120))
    #saved_item = db.relationship("Item", backref = "owner")

    def __init__(self, username, password):
        self.username = username
        self.password = password  
        

class Item (db.Model):

 #   saved_item = db.relationship("Item", backref = "user")
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
<<<<<<< HEAD
    # description = db.Column(db.String(2000))
    # culture = db.Column(db.String(120))
    # climate = db.Column(db.String(120))
    # gender = db.Column(db.String(120))
    # item_type = db.Column(db.String(120)) 
    # time_period_start = db.Column(db.Integer)
    # time_period_end = db.Column(db.Integer)
    owner = db.Column(db.String(120), db.ForeignKey(User.username))
    
    def __init__(self, name,  owner):
    # description, culture, climate, gender, item_type, time_period_start, time_period_end,

        self.name = name
        # self.description = description
        # self.culture = culture
        # self.climate = climate
        # self.gender = gender
        # self.item_type = item_type
        # self.time_period_end = time_period_start
        # self.time_period_end = time_period_end
        self.owner = owner


class Kit (db.Model):
    
    kit_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey(Item.id))
    username = db.Column(db.String(120), db.ForeignKey(User.username))

    def __init__(self, kit_id, item_id, username):

        self.kit_id = kit_id
        self.item_id = item_id
        self.username = username


class Culture (db.Model):

    name = db.Column(db.String(120), primary_key=True)

    def __init__(self, name):
            self.name = name

        
class Climate (db.Model):

    name = db.Column(db.String(120), primary_key=True)
=======
    culture = db.Column(db.String(120))
    climate = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    item_type = db.Column(db.String(120))
    time_period_start = db.Column(db.Integer)
    time_period_end = db.Column(db.Integer)
    description = db.Column(db.String(2000))
    user_id = db.Column(db.Integer)

 #   user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, name, culture, climate, gender, item_type, time_period_start, time_period_end, description, user):
        self.name = name
        self.culture = culture
        self.climate = climate
        self.gender = gender
        self.item_type = item_type
        self.time_period_start = time_period_start
        self.time_period_end = time_period_end
        self.description = description
        self.user = user

class Climate (db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2000))
>>>>>>> 1c187eae33780a801c8f2af3cb7cce57d51c4698

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

<<<<<<< HEAD
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'home', 'index']
    if request.endpoint not in allowed_routes and 'user' not in session:
    # restricted_routes = ['saved_items']
    # if request.endpoint in restricted_routes and 'user' not in session:
        return redirect('/login')

@app.route('/logout')
def logout():
    if "user" in session:
        del session['user']
    return redirect('/home')

=======
>>>>>>> 1c187eae33780a801c8f2af3cb7cce57d51c4698
@app.route('/home')
def avocado():
  return render_template("home.html")

@app.route('/index', methods=['POST', 'GET'])
def index():
<<<<<<< HEAD
    if request.method == 'POST':
        item_id = request.form['name']
        user = User.query.filter_by(username=session['user']).first()
        print ("====")
        print (user)
        print ("====")
        new_kit = Kit(item_id, user.username)
        print ("=====")
        print (user.username)
        print ("=====")
        db.session.add(new_kit)
        db.session.commit()
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/saved_items', methods=['POST', 'GET'])
def my_stuff():
    if request.method == 'POST':
        item_name = request.form['item']
        owner = User.query.filter_by(username=session['user']).first()
        new_item = Item(item_name, owner.username)
        db.session.add(new_item)
        db.session.commit()
    owner = User.query.filter_by(username=session['user']).first()
    print ("=====")
    print (owner.username)
    print ("=====")
    items = Item.query.filter_by(owner=owner.username).all()
    return render_template("saved_items.html", items = items)

# @app.route("/welcome")
# def welcome_in():
#     username = request.args.get("username")  
#     return render_template("welcome.html", username=username)
=======
    for item in Item.query.all():
        print(item.name, item.description)
    items = Item.query.all()
    print(items)
    return render_template("index.html",items=items)

@app.route("/welcome")
def welcome_in():
    username = request.args.get("username")  
    return render_template("welcome.html", username=username)
>>>>>>> 1c187eae33780a801c8f2af3cb7cce57d51c4698

@app.route("/")
def default():
    return redirect("/home")
 
if __name__ == "__main__":
    app.run()
