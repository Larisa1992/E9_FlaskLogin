from flask_login import login_required, current_user, login_user, logout_user, LoginManager
from flask import jsonify, render_template, request, redirect, flash, url_for, abort
from datetime import datetime, timedelta
from is_safe_url import is_safe_url

from app import app, db, bcrypt, login_manager
from app.models import Event, User
from app.forms import EventsForm, CreateUserForm, LoginForm


@app.route('/')
def index():
    mes = "Hi, it is project about user's events!"
    return render_template('index.html', mes=mes)

# возвращает объект пользователя по его email
@login_manager.user_loader
def user_loader(user_id):
    print(f'user_id {user_id}')
    return User.query.get(user_id)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect('/')
        # return redirect(url_for('index'))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.get(form.email.data)
            # user = db.session.query(User).filter(User.email == form.email.data).first()
            print(user.email)
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()

                    login_user(user, remember=True, duration = timedelta(minutes=25))

                    print('current_user.email = ', current_user.email)
                    print('current_user.is_authenticated = ', current_user.is_authenticated())
                    return redirect("/events_list")
                    # next = request.args.get('next')

                    # print(f'next {next}')
                    # if not is_safe_url(next):
                    #     return abort(400)

                    # return redirect(next or url_for('index'))
                    # return redirect("/")
                    # return render_template(url_for('index'), user = user)
                else:
                    flash('Email or password is not correct')
            else: flash('Please, fill email and password fields!')

    return render_template("login.html", form=form)

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    message = ''
    form = CreateUserForm()
    
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User(email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        flash('User created successfully')
        return redirect('/login')
    return render_template("create_user.html", form=form)

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect('/login')

# @csrf.exempt
# для залогиненного пользователя доступна форма, которая позволяет добавить событие.
# У события должны быть следующие параметры: автор, время начала, время конца, тема и описание
@app.route('/add_event', methods=['POST', 'GET'])
# @login_required
def add_event():
    events_form = EventsForm()
    print(f'add_event request.method {request.method} ')
    if request.method == 'POST':
        print(f'events_form.validate_on_submit { events_form.validate_on_submit() } ')
        print(f'events_form.errors {events_form.errors} ')
        print(f'events_form.from_date.data {events_form.from_date.data} ')
        print(f'request to_date  {request.form.get("to_date")} ')
        # не работает валидация формы, уточнить
        # if events_form.validate_on_submit():

        author = request.form.get('author')
        # date_format = datetime.strptime(date, '%d-%m-%y')
        from_date = request.form.get('from_date')
        to_date = request.form.get('to_date')
        theme = request.form.get('theme')
        description = request.form.get('description')
        ev = Event(author=author, from_date=from_date, to_date=to_date, theme=theme, description=description)
        
        # print(f'add_event current_user.email {current_user.email}')

        db.session.add(ev)
        db.session.commit()
        return redirect('/events_list')
        # flash("Form was not validated")
    
    return render_template('events.html', form=events_form)

# список всех событий для залогиненного пользователя
@app.route('/events_list')
# @login_required
def events_list():
    events = Event.query.order_by(Event.from_date).all()
    print('events_list current_user.is_authenticated = ', current_user.is_authenticated)
    return render_template('events_list.html', object_list=events)

@app.route('/events_edit')
def events_edit():
    # events = Event.query.all(current_user.email)
    events = db.session.query(Event).filter(author == current_user.email)
    return render_template('events_edit.html', object_list=events)