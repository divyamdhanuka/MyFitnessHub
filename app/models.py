from app import db, exercise_data
from datetime import datetime, timezone
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
    FloatField,
    SelectField,
    TimeField,
    HiddenField,
)
from wtforms.validators import (
    InputRequired,
    Length,
    ValidationError,
    Email,
    NumberRange,
    Optional,
    DataRequired,
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    profile_info = db.Column(db.String(256))
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    sex = db.Column(db.String, nullable=False)
    steps = db.Column(db.Integer, default=0)
    calories_burned = db.Column(db.Integer, default=0)
    calorie_intake = db.Column(db.Integer, default=0)
    workouts = db.relationship("Workout", backref="user", lazy="dynamic")
    meals = db.relationship("Meal", backref="user", lazy="dynamic")
    goals = db.relationship("Goal", backref="user", lazy="dynamic")


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    email = StringField(
        validators=[InputRequired(), Email(), Length(min=3, max=320)],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )
    age = IntegerField(
        validators=[InputRequired(), NumberRange(min=1, max=120)],
        render_kw={"placeholder": "Age"},
    )
    height = FloatField(
        validators=[
            InputRequired(),
            NumberRange(
                min=0.5, max=2.50, message="Height must be between 0.5 and 2.5 meters."
            ),
        ],
        render_kw={"placeholder": "Height (m)"},
    )
    weight = FloatField(
        validators=[
            InputRequired(),
            NumberRange(min=1, max=300, message="Weight must be between 1 and 300 kg."),
        ],
        render_kw={"placeholder": "Weight (kg)"},
    )
    sex = SelectField(
        choices=[("Male", "Male"), ("Female", "Female"), ("Neither", "Neither")],
        validators=[InputRequired()],
        render_kw={"placeholder": "Sex"},
    )
    submit = SubmitField("Register")


def validate_username(self, username):
    user_exist = User.query.filter_by(username=username.data).first()
    if user_exist:
        raise ValidationError(
            "This username already exists. Please choose a different one"
        )


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Login")


class EditProfileForm(FlaskForm):
    age = IntegerField(
        validators=[Optional(), NumberRange(min=1, max=120)],
        render_kw={"placeholder": "Age"},
    )
    height = FloatField(
        validators=[
            Optional(),
            NumberRange(
                min=0.5, max=2.5, message="Height must be between 0.5 and 2.5 meters"
            ),
        ],
        render_kw={"placeholder": "Height (m)"},
    )
    weight = FloatField(
        validators=[
            Optional(),
            NumberRange(min=1, max=300, message="Weight must be between 1 and 300 kg."),
        ],
        render_kw={"placeholder": "Weight (kg)"},
    )
    sex = SelectField(
        "Sex",
        choices=[
            ("", "Select"),
            ("Male", "Male"),
            ("Female", "Female"),
            ("Neither", "Neither"),
        ],
        validators=[Optional()],
        render_kw={"placeholder": "Sex"},
    )
    submit = SubmitField("Save Changes")


class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    start_time = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    exercise = db.Column(db.String(64))
    duration = db.Column(db.Integer)
    calories_burned = db.Column(db.Integer)


class WorkOutForm(FlaskForm):
    start_time = TimeField(
        "Start Time",
        validators=[InputRequired()],
        default=datetime.now().time(),
        render_kw={"placeholder": "Start Time"},
    )
    exercise = SelectField(
        choices=[
            exercise
            for exercise in exercise_data["Activity, Exercise or Sport (1 hour)"]
        ],
        validate_choice=[InputRequired()],
        render_kw={"placeholder": "Exercise"},
    )
    duration = IntegerField(
        validators=[InputRequired(), NumberRange(min=1, max=(24 * 60))],
        render_kw={"placeholder": "Duration (min)"},
    )
    timezone = HiddenField(validators=[InputRequired()])
    submit = SubmitField("Add Workout")


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    name = db.Column(db.String(64))
    calories = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    fats = db.Column(db.Integer)


class SearchMealForm(FlaskForm):
    food_item = StringField("Food Item", validators=[InputRequired()])
    submit = SubmitField("Add Food")


class AddMealForm(FlaskForm):
    quantity = IntegerField(
        "Quantity",
        validators=[InputRequired(), NumberRange(min=1)],
        render_kw={"placeholder": "Enter quantity consume"},
    )
    submit = SubmitField("Add Food")


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    type = db.Column(db.String(64))
    target = db.Column(db.Integer)
    current_progress = db.Column(db.Integer)
    deadline = db.Column(db.DateTime)
