import base64
from functools import wraps
from copy import deepcopy

from flask import render_template, request, redirect, make_response, flash
from flask.views import MethodView

from controllers.AuthorizationController import AuthorizationController
from controllers.AuthenticationController import AuthenticationController
from controllers.DataBaseController import DataBaseController
from controllers.exceptions import LoginRequired
from utils.TokenHelper import TokenHelper
from database.mongo_db import get_all_movies, add_movie, drop_database

db_controller = DataBaseController()
authorization_controller = AuthorizationController(db_controller)
authentication_controller = AuthenticationController(db_controller)


class DefaultView(MethodView):
    def __init__(self):
        super(DefaultView, self).__init__()
        self.get = DefaultView.login_required(self.get)
        self.post = DefaultView.login_required(self.post)

    @staticmethod
    def login_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.cookies.get("token")
            if token and authentication_controller.validate_token(token):
                return func(*args, **kwargs)
            flash("Please log in first", "warning")
            return redirect('/login')

        return wrapper


class LoginPage(MethodView):

    def get(self):
        token = request.cookies.get("token")
        is_user_logged = bool(
            token) and authentication_controller.validate_token(token)
        return render_template("login.html",
                               is_user_logged=is_user_logged)

    def post(self):
        is_user_logged = authorization_controller.login(
            request.form['email'],
            request.form['password'])

        if is_user_logged:
            flash("You are successfully logged in", "success")
            resp = make_response(redirect("/"))
            resp.set_cookie("token",
                            TokenHelper.generate_token(request.form['email'],
                                                       request.form['password'])
                            )
            return resp
        flash("You are used wrong credentials", "")
        return redirect("/login")


class LogoutPage(MethodView):
    def get(self):
        flash("You are successfully logged out", "success")
        resp = make_response(redirect("/"))
        resp.set_cookie("token", "")
        return resp

    def post(self):
        return self.get()


class RegistrationPage(MethodView):

    @staticmethod
    def exception_handler(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                outcome = func(*args, **kwargs)
            except LoginRequired:
                flash("The user with such email exists. Please log"
                      " in or choose another email", "")
                return redirect('/registration')
            return outcome

        return wrapper

    def get(self):
        token = request.cookies.get("token")
        is_user_logged = bool(
            token) and authentication_controller.validate_token(token)
        return render_template("registration.html",
                               is_user_logged=is_user_logged)

    @exception_handler
    def post(self):
        authorization_controller.register(request.form['first_name'],
                                          request.form['last_name'],
                                          request.form['phone_number'],
                                          request.form['email'],
                                          request.form['password'])
        flash("You are successfully registered."
              " Please log in to your account", "success")
        return redirect("/")


class AllFilmsPage(MethodView):
    @staticmethod
    def login_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.cookies.get("token")
            if token and authentication_controller.validate_token(token):
                return func(*args, **kwargs)
            flash("Please log in first", "warning")
            return redirect('/login')

        return wrapper

    @login_required
    def get(self):
        token = request.cookies.get("token")
        is_user_logged = bool(
            token) and authentication_controller.validate_token(token)
        films = get_all_movies()
        films_copy = list(deepcopy(films))

        for film in films_copy:
            with open(film['path_to'], 'rb') as f:
                film['data'] = base64.b64encode(f.read()).decode('utf-8')

        return render_template('index.html',
                               films=films_copy,
                               is_user_logged=is_user_logged)


class UploadMovie(MethodView):
    @staticmethod
    def login_required(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.cookies.get("token")
            if token and authentication_controller.validate_token(token):
                return func(*args, **kwargs)
            flash("Please log in first", "warning")
            return redirect('/login')

        return wrapper

    @login_required
    def get(self):
        token = request.cookies.get("token")
        is_user_logged = bool(
            token) and authentication_controller.validate_token(token)
        return render_template('file_upload.html',
                               is_user_logged=is_user_logged)

    @login_required
    def post(self):
        f = request.files['file']
        path_to_movie = f"/app/movies/{f.filename}"
        f.save(path_to_movie)
        add_movie(f.filename, f.mimetype, path_to_movie)
        flash("Your movie successfully uploaded", "success")
        return redirect("/")


class DocsPage(MethodView):
    def get(self):
        token = request.cookies.get("token")
        is_user_logged = bool(
            token) and authentication_controller.validate_token(token)
        with open("/app/docs/use_case.jpg", "rb") as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')
        return render_template('docs.html',
                               is_user_logged=is_user_logged,
                               data=img_data)