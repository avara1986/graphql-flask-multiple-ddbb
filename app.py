# encoding: utf-8
from __future__ import absolute_import, print_function, unicode_literals

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_graphql import GraphQLView

from models import db_session
from schema import schema

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'SECRET'

toolbar = DebugToolbarExtension(app)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # for having the GraphiQL interface
    )
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()
