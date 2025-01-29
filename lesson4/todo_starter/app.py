from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return redirect(url_for('get_lists'))

# Render new todo list page
@app.route("/lists/new")
def add_todo_list():
    return render_template('new_list.html')

# Render the list of todo lists
@app.route("/lists")
def get_lists():
    lists = [
        {"title": "Lunch Groceries", "todos":[]},
        {"title": "Dinner Groceries", "todos": []},
    ]
    return render_template('lists.html', lists=lists)

if __name__ == "__main__":
    app.run(debug=True, port=5003)
