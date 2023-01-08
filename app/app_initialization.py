from flask import Flask

from configs.Config import Config
from views.views import LoginPage, RegistrationPage, \
    AllFilmsPage, LogoutPage, UploadMovie, DocsPage

app = Flask(__name__)
config = Config()
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.add_url_rule("/login",
                 view_func=LoginPage.as_view("login"))
app.add_url_rule("/registration",
                 view_func=RegistrationPage.as_view("registration"))
app.add_url_rule("/",
                 view_func=AllFilmsPage.as_view("all_movies"))
app.add_url_rule("/logout",
                 view_func=LogoutPage.as_view("logout"))
app.add_url_rule("/upload",
                 view_func=UploadMovie.as_view("upload"))
app.add_url_rule("/docs",
                 view_func=DocsPage.as_view("docs"))
