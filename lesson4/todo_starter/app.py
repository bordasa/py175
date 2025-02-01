from uuid import uuid4

from flask import (
    flash,
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.exceptions import NotFound

from todos.utils import (
    delete_todo_by_id,
    error_for_list_title,
    error_for_todo, 
    find_list_by_id,
    find_todo_by_id,
    is_list_completed,
    is_todo_completed,
    mark_all_completed,
    sort_items,
    todos_remaining,
)

app = Flask(__name__)
app.secret_key='secret1'

@app.context_processor
def list_utilities_processor():
    return dict(
        is_list_completed = is_list_completed,
    )

@app.before_request
def initialize_session():
    if 'lists' not in session:
        session['lists'] = []

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
    lists = sort_items(session['lists'], is_list_completed)
    return render_template('lists.html', 
                           lists=lists,
                           todos_remaining=todos_remaining)

# Create a new todo list
@app.route("/lists", methods=["POST"])
def create_list():
    title = request.form["list_title"].strip()
    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, "error")
        return render_template('new_list.html', title=title)
    
    session['lists'].append({
            'id': str(uuid4()),
            'title': title,
            'todos': [],
            })

    flash("The list has been created.", "success")
    session.modified = True
    return redirect(url_for('get_lists'))

@app.route("/lists/<list_id>")
def show_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")
    
    lst['todos'] = sort_items(lst['todos'], is_todo_completed)
    return render_template('list.html', lst=lst)

@app.route("/lists/<list_id>/todos", methods=["POST"])
def create_todo(list_id):
    todo_title = request.form['todo'].strip()
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found")
    
    error = error_for_todo(todo_title)
    if error:
        flash(error, "error")
        return render_template('list.html', lst=lst)
    
    lst['todos'].append({
        'id': str(uuid4()),
        'title': todo_title,
        'completed': False,
    })
    
    flash("The todo was added.", "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<list_id>/todos/<todo_id>/toggle", methods=["POST"])
def update_todo_status(list_id, todo_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found.")

    todo = find_todo_by_id(todo_id, lst['todos'])
    if not todo:
        raise NotFound(description="Todo not found")
    
    todo['completed'] = (request.form['completed'] == 'True')

    flash('The todo has been updated.', "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<list_id>/todos/<todo_id>/delete", methods=["POST"])
def delete_todo(list_id, todo_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found.")
    
    todo = find_todo_by_id(todo_id, lst['todos'])
    if not todo:
        raise NotFound(description="Todo not found")
    
    delete_todo_by_id(todo_id, lst)

    flash('The todo has been deleted.', "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<list_id>/complete_all", methods=["POST"])
def mark_all_todos_completed(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found.")
    
    mark_all_completed(lst)

    flash('All todos are done!', "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))

@app.route("/lists/<list_id>/edit")
def edit_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found.")
    
    return render_template('edit_list.html', lst=lst)

@app.route("/lists/<list_id>/delete", methods=["POST"])
def delete_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found.")
    
    session['lists'] = [lst for lst in session['lists']
                        if lst['id'] != list_id]
    
    flash("The list has been deleted.", "success")
    session.modified = True
    return redirect(url_for('get_lists'))

@app.route("/lists/<list_id>", methods=["POST"])
def update_list(list_id):
    lst = find_list_by_id(list_id, session['lists'])
    if not lst:
        raise NotFound(description="List not found.")

    title = request.form["list_title"].strip()
    error = error_for_list_title(title, session['lists'])
    if error:
        flash(error, "error")
        return render_template('edit_list.html', lst=lst, title=title)
    
    lst['title'] = title
    
    flash("The list has been updated.", "success")
    session.modified = True
    return redirect(url_for('show_list', list_id=list_id))


if __name__ == "__main__":
    app.run(debug=True, port=5003)