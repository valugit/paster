from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, validators
from wtforms.validators import DataRequired, ValidationError
from app.models import Post


class PostForm(FlaskForm):
    title = StringField(
        "Title :",
        [validators.Length(max=128), validators.DataRequired()],
        render_kw={"placeholder": "Your Title Goes Here..."},
    )
    content = TextAreaField(
        "Content :",
        [validators.Length(max=1024), validators.DataRequired()],
        render_kw={"placeholder": "Your Content Goes Here..."},
    )
    path = StringField(
        "Path :",
        [validators.Regexp(r"[A-Za-z0-9]{4}"), validators.Optional()],
        render_kw={"placeholder": "Choose Your Path Here..."},
    )
    submit = SubmitField("Post")

    def validate_path(self, path):
        post = Post.query.filter_by(path=path.data).first()
        if post is not None:
            raise ValidationError("Please use a different path.")
