from flask import render_template, flash, redirect, url_for, request, session
from app import app, db, bcrypt, login_manager, exercise_data
from app.models import (
    User,
    RegisterForm,
    LoginForm,
    EditProfileForm,
    Workout,
    Meal,
    Goal,
    WorkOutForm,
    datetime,
    timezone,
    SearchMealForm,
    AddMealForm,
)
from flask_login import current_user, login_user, logout_user, login_required
import pytz
from datetime import time
import requests


NUTRITIONIX_APP_ID = XXXXXXXX
NUTRITIONIX_API_KEY = XXXXXXX


def calculate_calories_burned(exercise, duration):
    exercise_row = exercise_data[
        exercise_data["Activity, Exercise or Sport (1 hour)"] == exercise
    ]
    return (
        current_user.weight
        * int(exercise_row["Calories per lbs per hour"].values[0])
        * (duration / 60)
    )


def workouts_in_a_day(user_id, tz_str):
    tz = pytz.timezone(tz_str)
    now = datetime.now(tz=tz)
    midnight = datetime.combine(now.date(), time.min, tz)
    time_difference = now - midnight
    today = datetime.now(tz=timezone.utc)
    yesterday = datetime.now(tz=timezone.utc) - time_difference

    workouts = Workout.query.filter(
        Workout.user_id == user_id,
        Workout.start_time >= yesterday,
        Workout.start_time <= today,
    ).all()

    return workouts


def calories_burned_in_a_day(user_id, tz_str):
    workouts = workouts_in_a_day(user_id, tz_str)

    return sum(workout.calories_burned for workout in workouts)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/set_timezone", methods=["POST"])
def set_timezone():
    data = request.json
    if "timezone" in data:
        session["timezone"] = data["timezone"]
        return "Timezone set", 200
    return "Timezone not provided", 400


@app.route("/")
@app.route("/index")
def index():
    user_timezone = session.get("timezone", "UTC")
    if current_user.is_authenticated:
        total_calories = calories_burned_in_a_day(current_user.id, user_timezone)
    else:
        total_calories = 0
    return render_template("index.html", total_calories=total_calories, title="home")


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if request.method == "POST":

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(
                user.password_hash, form.password.data
            ):
                login_user(user)
                flash("You have successfully logged in", "sucess")
                return redirect(url_for("index"))
        else:
            flash("Invalid username or password, please try again.", "danger")

    return render_template("login.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegisterForm()

    if request.method == "POST":

        if form.validate_on_submit():
            password_hash = bcrypt.generate_password_hash(form.password.data)
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=password_hash,
                age=form.age.data,
                height=form.height.data,
                weight=form.weight.data,
                sex=form.sex.data,
            )
            db.session.add(new_user)
            db.session.commit()
            flash("You are a registered user now!", "success")
            return redirect(url_for("login"))

        else:
            flash("Invalid username or password, please try again", "danger")

    return render_template("register.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile", methods=["POST", "GET"])
def profile():
    form = EditProfileForm()

    # The profile section should have all the stats about the user.
    # So that would inclue, for now, the steps, the calories burnt, active time, calories intake.
    # It can also take into account the sleep tracking feature from the watch.
    # Can also take into account the amount of water drank in the entire day.

    return render_template("profile.html", form=form)


@app.route("/edit_profile", methods=["POST", "GET"])
def edit_profile():
    form = EditProfileForm()

    if request.method == "POST":
        if form.validate_on_submit():
            if form.age.data is not None:
                current_user.age = form.age.data
            if form.height.data is not None:
                current_user.height = form.height.data
            if form.weight.data is not None:
                current_user.weight = form.weight.data
            if form.sex.data:
                current_user.sex = form.sex.data
            db.session.commit()
            flash("Your profile has been updated.")
            return redirect(url_for("profile"))

    return render_template("profile.html", form=form)


@app.route("/add_workout", methods=["POST", "GET"])
def add_workout():
    form = WorkOutForm()

    if request.method == "POST":
        if form.validate_on_submit():
            start_time_local = pytz.timezone(form.timezone.data).localize(
                datetime.combine(datetime.now().date(), form.start_time.data)
            )
            start_time = start_time_local.astimezone(pytz.utc)
            exercise = form.exercise.data
            duration = form.duration.data
            calories_burned = calculate_calories_burned(exercise, duration)

            new_workout = Workout(
                user_id=current_user.id,
                start_time=start_time,
                exercise=str(exercise),
                duration=duration,
                calories_burned=calories_burned,
            )

            db.session.add(new_workout)
            db.session.commit()
            flash("You have added a new workout!", "success")
            return redirect(url_for("add_workout"))
        else:
            flash("The form had some invalid entries!", "danger")

    return render_template("add_workout.html", form=form)


@app.route("/workouts", methods=["GET"])
def workouts():
    user_timezone = session.get("timezone", "UTC")
    workouts = workouts_in_a_day(current_user.id, user_timezone)

    for workout in workouts:
        utc_localized = pytz.timezone("UTC").localize(workout.start_time)
        workout.start_time = utc_localized.astimezone(pytz.timezone(user_timezone))
        print(workout.start_time)

    return render_template("workouts.html", workouts=workouts)


@app.route("/search_meal", methods=["POST", "GET"])
def search_meal():
    form = SearchMealForm()
    results = None
    if form.validate_on_submit():
        food_item = form.food_item.data
        response = requests.get(
            "https://trackapi.nutritionix.com/v2/search/instant",
            headers={
                "Content-Type": "application/json",
                "x-app-id": NUTRITIONIX_APP_ID,
                "x-app-key": NUTRITIONIX_API_KEY,
            },
            params={"query": food_item},
        )

        if response.status_code == 200:
            data = response.json()
            results = data.get("common", []) + data.get("branded", [])
        else:
            flash("Food entry was not successful!", "danger")

    return render_template("search_meal.html", form=form, results=results)


@app.route("/add_meal", methods=["POST", "GET"])
def add_meal():
    form = AddMealForm()
    if request.method == "GET":
        session["food_name"] = request.args.get("food_name")
        response = requests.get(
            "https://trackapi.nutritionix.com/v2/natural/nutrients",
            headers={
                "Content-Type": "application/json",
                "x-app-id": NUTRITIONIX_APP_ID,
                "x-app_key": NUTRITIONIX_API_KEY,
            },
            params={"query": session.get("food_name")},
        )

        if response.status_code == 200:
            data = response.json()
            session["serving_qty"] = data["foods"][0]["serving_qty"]
            session["serving_unit"] = data["foods"][0]["serving_unit"]
            session["nf_calories"] = data["foods"][0]["nf_calories"]

    if form.validate_on_submit():
        food_name = session.get("food_name")
        nf_calories = float(session.get("nf_calories"))
        serving_qty = int(session.get("serving_qty"))
        serving_unit = session.get("serving_unit")
        quantity = form.quantity.data

        total_calories = nf_calories * (quantity / serving_qty)

        print(total_calories)

        return redirect(url_for("index"))

    return render_template("add_meal.html", form=form)


@app.route("/add_goal", methods=["POST", "GET"])
def add_goal():
    # Goals that the user wants to achieve each day for calories burned, steps achieved and active time.
    # Could also be for sleep time and water intake and calorie intake.
    pass
