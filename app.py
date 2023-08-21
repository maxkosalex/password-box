from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user,login_required, LoginManager, logout_user

app = Flask(__name__)
app.secret_key = "247557"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30),  nullable=True)
    email = db.Column(db.String(60), nullable=True)
    password = db.Column(db.String(30), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Article %r>' % self.id


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id



@login_manager.user_loader
def load_user(user_id):
    return  Users.query.get(user_id)


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        name = request.form['input_name']
        email = request.form['input_email']
        password = request.form['input_password']
        article = Article(name=name, email=email, password=password)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')

        except Exception as ex:
            print(ex)
            return str(ex)

    else:
        articles = Article.query.all()
        return render_template('main.html', articles=articles)


@app.route('/<int:id>/delete')
@login_required
def data_delete(id):
    global login_key
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/password-box/'+str(login_key))
    except:
        return "Произошла ошибка"




@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        check_password = request.form['check-password']
        if password == check_password:
            hash = generate_password_hash(password)
            users = Users(name=name, password=hash)
            try:
                db.session.add(users)
                db.session.commit()

                return redirect('login')

            except Exception as ex:
                print(ex)
                return str(ex)
        else:
            flash('Пароли не сходятся')

    return render_template('registration.html')


login_key = None


@app.route('/login',methods=["POST", "GET"])
def login():
    global login_key
    if request.method == 'POST':
        name = request.form['name']
        check_user = Users.query.filter_by(name=name).first()
        password = request.form['password']
        if check_user != None:
            if check_password_hash(check_user.password, password) == True:
                login_user(check_user)
                login_key = check_user.id
                return redirect('/password-box/'+str(check_user.id))
            else:
                flash('Не верный пароль')
                return  redirect('/login')
        else:
            flash('Такого пользователя нет')
            return redirect('/login')
    else:
        return render_template('login.html')


@app.route('/logout',methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/password-box/<int:id>', methods=["POST", "GET"])
@login_required
def profile(id):
    global login_key
    if request.method == 'POST' and id == login_key:
        user = Users.query.get_or_404(id)
        name = request.form['input_name']
        email = request.form['input_email']
        password = request.form['input_password']
        user_id = login_key
        article = Article(name=name, email=email, password=password, user_id=user_id)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/password-box/'+str(login_key))

        except Exception as ex:
            print(ex)
            return str(ex)
    else:
        user_id = login_key
        if id != user_id:
            return "Страница не найдена"
        else:
            articles = Article.query.filter_by(user_id=login_key).all()
            user = Users.query.filter_by(id=login_key).first()
            return render_template('psw_profile.html', articles=articles, users=user)


@app.after_request
def redirect_to_signin(response):
    global login_key
    if response.status_code == 401:
        return redirect(url_for("login") + "?next=" + request.url)
    return response


if __name__ == "__main__":
    app.run(debug=True)