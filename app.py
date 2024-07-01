from flask import  Flask,render_template, request, redirect
from models import db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'
db.init_app(app)


@app.before_request
def create_tables():
    db.create_all()



@app.route('/')
def index():
    user = User.query.all()
    return render_template('index.html', datas = user)
 

@app.route('/add_user', methods = ['GET', 'POST'])
def add_user():
    
    if request.method == "POST":
        name = request.form['uname']
        email = request.form['uemail']
        password = request.form['upwd']
        new_user = User(name = name, email = email, password = password)
        db.session.add(new_user)
        db.session.commit()
        user = User.query.all()
        return render_template('index.html', datas = user)
    
   
    return render_template('add_user.html')


@app.route('/edit_user/<int:user_id>', methods = ['GET', 'POST'])
def edit_user(user_id):
    user = User.query.all()
    member = User.query.get_or_404(user_id)
    if request.method == "POST":
        member.name = request.form['uname']
        member.email = request.form['uemail']
        db.session.commit()
        return render_template('index.html', datas = user)

    return render_template('edit_user.html', user = member )


@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user = User.query.all()
    member = User.query.get_or_404(user_id)
    db.session.delete(member)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)