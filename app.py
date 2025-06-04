from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# sets config variable. Using sqlite database for now.
# path to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# Need to set to false to avoid warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# creating the actual database
db = SQLAlchemy(app)

# Define a Todo model that represents a table in the database


class Todo(db.Model):
    # Unique ID for each task (Primary Key)
    id = db.Column(db.Integer, primary_key=True)
    # Task title, up to 100 characters
    title = db.Column(db.String(100))
    # Boolean indicating if the task is completed
    complete = db.Column(db.Boolean)


# Route for the homepage ("/")
@app.route('/')
def index():
    # show all todos
    todo_list = Todo.query.all()
    print(todo_list)
    # Render and return template
    return render_template('base.html', todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    # add new item
    # get title from the form. Import request for this
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    # import redirect and url_for. Redirects user to index page.
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        # Initialize database tables from SQLAlchemy models
        db.create_all()

    # Start the Flask server with debug mode enabled
    app.run(debug=True)
