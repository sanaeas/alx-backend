#!/usr/bin/env python3
""" Create Flask App """
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    """ Configure available languages in the app """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """ Retrieve user information based on the provided user id """
    return users.get(user_id)


@app.before_request
def before_request():
    """ Execute before all other functions """
    user_id = request.args.get('login_as')
    if user_id:
        user = get_user(int(user_id))
        g.user = user
    else:
        g.user = None


@babel.localeselector
def get_locale():
    """ Determine the best match with our supported languages """
    locale_param = request.args.get('locale')

    if locale_param and locale_param in app.config['LANGUAGES']:
        return locale_param

    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """ Home page """
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run()
