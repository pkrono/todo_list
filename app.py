from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) #initialize the database

class Todo(db.Model): #initialize model
    task_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id
        
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception:
            return 'error adding task'
        
    else:
        tasks = Todo.query.order_by(Todo.create_date).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task_to_delete = Todo.query.get_or_404(task_id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception:
        return 'error deleting task'
    
@app.route('/update/<int:task_id>', methods=['GET','POST'])
def update_task(task_id):
    task_to_update = Todo.query.get_or_404(task_id)
    try:
        db.session.update(task_to_update)
    except Exception:
        return 'error updating task'


if __name__ == "__main__":
    app.run(debug=True)