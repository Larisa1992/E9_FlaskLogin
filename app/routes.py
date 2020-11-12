from flask_login import login_required, current_user, login_user, logout_user, LoginManager
from flask import jsonify, render_template, request, redirect, flash, url_for, abort
from datetime import datetime, timedelta
from is_safe_url import is_safe_url

from app import app, db, bcrypt, login_manager
from app.models import Event, User
from app.forms import EventsForm, CreateUserForm, LoginForm


@login_manager.user_loader
def user_loader(email):
    print(f'email from rout')
    print(f'email from rout {email}')
    return User.query.filter_by(email=email).first()

@login_manager.request_loader
def request_loader(request):
    print(request)
    email = request.form.get('email')
    print(f'request.form from request_loader {request.form}')
    print(f'email from request_loader {email}')
    user = User.query.filter_by(email=email).first()
    if not user:
        return
    user.authenticated = True
    db.session.add(user)
    db.session.commit()
    return user

@app.route('/')
def index():
    mes = "Hi, it is project about user's events!"
    return render_template('index.html', mes=mes)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        curr_user = User.query.filter_by(email=form.email.data).first()
        if curr_user:
            if bcrypt.check_password_hash(curr_user.password, form.password.data):
                curr_user.authenticated = True
                db.session.add(curr_user)
                db.session.commit()

                login_user(curr_user, remember=True)

                print('current_user.email login = ', current_user.email)        
                return redirect("/")
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
        new_user = User(email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(new_user)
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

# для залогиненного пользователя доступна форма, которая позволяет добавить событие.
# У события должны быть следующие параметры: автор, время начала, время конца, тема и описание
@app.route('/add_event', methods=['POST', 'GET'])
@login_required
def add_event():
    events_form = EventsForm()
    if request.method == 'POST':

        if events_form.validate_on_submit():

            author = request.form.get('author')
            from_date = request.form.get('from_date')
            to_date = request.form.get('to_date')
            theme = request.form.get('theme')
            description = request.form.get('description')
            author = current_user.email
            ev = Event(author=author, from_date=from_date, to_date=to_date, theme=theme, description=description)
            db.session.add(ev)
            db.session.commit()
            return redirect('/events_list')
        flash(f'Form was not validated {events_form.errors}')
    
    return render_template('events.html', form=events_form)

# список всех событий для залогиненного пользователя
@app.route('/events_list')
@login_required
def events_list():
    events = Event.query.order_by(Event.from_date).all()
    return render_template('events_list.html', object_list=events)

# Детальнее
@app.route('/events/<int:_id>')
@login_required
def view_event(_id):
    this_event = Event.query.get(_id)
    return render_template('view_event.html', event = this_event)

# Обновить - редактировать
@app.route('/events/<int:_id>/edit',  methods=['POST', 'GET'])
@login_required
def edit_event(_id):
    this_event = Event.query.get(_id)
    if request.method == 'POST':
        this_event.from_date = request.form['from_date']
        this_event.to_date = request.form['to_date']
        this_event.theme = request.form['theme']
        this_event.description = request.form['description']
        try:
            db.session.add(this_event)
            db.session.commit()
            return redirect('/events_list')
        except:
            return 'При обновлении записи произошла ошибка'
    return render_template('edit_event.html', event = this_event)

# Удалить
@app.route('/events/<int:_id>/del')
@login_required
def delete_event(_id):
    del_event = Event.query.get_or_404(_id)
    print(del_event.theme)
    try:
        db.session.delete(del_event)
        db.session.commit()
        return redirect('/events_list')
    except:
        return 'При удалении события произошла ошибка'