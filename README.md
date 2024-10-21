# Fitness Tracker Web Application

This repository contains the source code for a Flask-based web application that helps users track their fitness activities, meals, and personal health goals. The app allows users to log their workouts, meals, and track progress towards their fitness goals. It also integrates with the Nutritionix API to search for food items and fetch their nutritional information.

## Features

- **User Registration and Login**: Users can create accounts and log in securely using hashed passwords.
- **Profile Management**: Users can view and edit their personal details such as age, height, weight, and gender.
- **Workout Tracking**: Users can log their workouts, specifying the type of exercise, start time, and duration. The app calculates calories burned based on the user's weight and the selected exercise.
- **Meal Tracking**: Integration with the Nutritionix API allows users to search for food items, log their meals, and track their daily calorie intake.
- **Goals**: Users can set fitness goals such as weight loss or calorie intake and track their progress.
- **Calorie Calculations**: The app provides daily summaries of calories burned from workouts and calorie intake from meals.
- **Timezone Support**: Users can set their timezone for accurate workout and meal tracking across different regions.

## Technologies Used

- **Flask**: Web framework used for building the app.
- **Flask-Login**: Manages user session handling and authentication.
- **Flask-WTF**: Provides form handling and validation.
- **SQLAlchemy**: ORM used for database management.
- **SQLite**: Database used for storing user data, workouts, meals, and goals.
- **Nutritionix API**: Used to fetch nutritional information for meals.
- **WTForms**: For form validation and handling in the app.
- **Jinja2**: Templating engine for rendering HTML pages.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/fitness-tracker.git
   cd fitness-tracker
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the environment variables**:
   Create a `.env` file in the project root directory and add the following keys:

   ```
   FLASK_APP=app
   FLASK_ENV=development
   NUTRITIONIX_APP_ID=your_nutritionix_app_id
   NUTRITIONIX_API_KEY=your_nutritionix_api_key
   ```

5. **Initialize the database**:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Run the application**:

   ```bash
   flask run
   ```

7. Visit `http://127.0.0.1:5000` in your browser to access the app.

## Usage

- **Register**: Create a new account by providing your username, email, password, age, height, weight, and gender.
- **Log in**: Use your registered username and password to log in.
- **Profile**: Edit your profile to update your age, height, weight, and gender.
- **Add Workouts**: Log your workouts by selecting the exercise type, start time, and duration. Calories burned will be calculated based on your weight and exercise type.
- **Search Meals**: Use the Nutritionix API to search for food items, then log them into your daily meals to track calorie intake.
- **View Workouts**: See a list of your logged workouts, along with the calories burned.

## File Structure

```
├── app/
│   ├── __init__.py           # Application initialization
│   ├── models.py             # Database models and forms
│   ├── routes.py             # Application routes and logic
│   └── templates/            # HTML templates for rendering pages
│       ├── base.html         # Base template
│       ├── index.html        # Home page template
│       ├── login.html        # Login page template
│       ├── register.html     # Registration page template
│       ├── profile.html      # Profile page template
│       ├── workouts.html     # Workouts page template
│       ├── search_meal.html  # Search meal page template
│       └── add_workout.html  # Add workout page template
├── migrations/               # Database migration files
├── venv/                     # Virtual environment files
├── .env                      # Environment variables
├── requirements.txt          # Required dependencies
└── README.md                 # Project documentation
```

## API Integration

This app integrates with the **Nutritionix API** to search for food items and log meals. To enable this feature, sign up for a free API key on [Nutritionix](https://www.nutritionix.com/business/api) and add your credentials to the `.env` file.

## Contributing

Feel free to fork this repository and submit pull requests. Any contributions to improve the app, fix bugs, or add new features are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
