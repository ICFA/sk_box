from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

#2
class CreateBookForm(FlaskForm):
    name = StringField(validators=[InputRequired()])
    author = StringField(validators=[InputRequired()])

#3
class SearchByAuthorForm(FlaskForm):
    author = StringField(validators=[InputRequired()])
