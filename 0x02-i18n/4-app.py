#!/usr/bin/env python3
""" Create Flask App """
from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """ Configure available languages in the app """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """ Determine the best match with our supported languages """
    locale_param = request.args.get('locale')

    if locale_param and locale_param in app.config['LANGUAGES']:
        return locale_param
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """ Home page """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run()
