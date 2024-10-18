"""
README
------
This app helps you manage to-do lists. Add, view, and complete tasks.

Usage
-----
1. Clone this repository and navigate to the project directory.
2. Create a virtual environment & install required libraries `pip install -r requirements.txt`.
3. Run the application using `python main.py`.
4. Open a web browser and navigate to the Todo list.

"""

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

BASE_URL = "http://localhost:5000"


class Todo(db.Model):
    """
    Todo Model
    ----------
    Represents a Todo item in the database.

    Attributes
    ----------
    id : int
        Unique identifier for the Todo item.
    title : str
        Title of the Todo item.
    description : str
        Description of the Todo item.
    completed : bool
        Whether the Todo item is completed or not.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Index Route
    -----------
    Handles GET and POST requests to the root URL.

    GET
    ---
    Retrieves all Todo items from the database and renders the index template.

    POST
    ----
    Creates a new Todo item based on the form data and adds it to the database.

    Returns
    -------
    render_template : str
        The rendered index template with the Todo items.
    """

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()

    todos = Todo.query.all()
    return render_template("index.html", todos=todos)


@app.route("/browser_session")
def browser_session():
    """
    Browser Session Route
    ---------------------
    Creates a new browser session using Selenium and navigates to the Todo list page.

    Returns
    -------
    render_template : str
        The rendered browser session template.
    """

    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    return render_template("browser_session.html")


@app.route("/add_button")
def add_button():
    """
    Add Button Route
    ----------------
    Adds a new button to the Todo list page.

    Returns
    -------
    render_template : str
        The rendered add button template.
    """

    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    button = driver.find_element_by_xpath("//button[@id='add-button']")
    button.click()
    return render_template("add_button.html")


@app.route("/add_switch")
def add_switch():
    """
    Add Switch Route
    ----------------
    Adds a new switch to the Todo list page.

    Returns
    -------
    render_template : str
        The rendered add switch template.
    """

    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    switch = driver.find_element_by_xpath("//input[@id='switch']")
    switch.click()
    return render_template("add_switch.html")


if __name__ == "__main__":
    db.create_all()
    app.run()
