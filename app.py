from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todolist(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, default=1)

    def __repr__(self):   # returns string when creating a task
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/', methods=['POST', 'GET'])   # adds item
def index():
    """Adds item by processing GET and POST requests
    
    If the request is POST, it adds a the inputted task and priority.
    If the request is GET, it retrieves all of the tasks in the database in the order of priority.

    Returns
    -------
        If the request method is POST and the task is added successfully, redirects to the index page.
        If the request method is GET, it renders the index template with the list of tasks.
    """

    if request.method == 'POST':
        taskname = request.form['taskname']
        taskpriority = request.form['taskpriority']
        catalog_task = Todolist(item=taskname, priority=taskpriority)
        
        db.session.add(catalog_task)
        db.session.commit()
        return redirect('/')

    else:
        items = Todolist.query.order_by(Todolist.priority).all()
        return render_template('index.html', items=items)
    
@app.route('/delete/<int:id>')   # deletes item
def delete(id):
    """Deletes items

    Parameters
    ----------
    id: integer
        The tag of each task in the database

    Deletes the selected task according to its id.

    Returns
    -------
        If the request method is POST and the task is added successfully, redirects to the index page.
        If the request method is GET, it renders the index template with the list of tasks.
    """
    deleting_item = Todolist.query.get_or_404(id)
    db.session.delete(deleting_item)
    db.session.commit()
    return redirect('/')

  
if __name__ == "__main__":
    app.run(debug=True)