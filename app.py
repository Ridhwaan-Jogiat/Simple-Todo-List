from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())


def __repr__(self):
    return "<task %r" % self.id


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a issue adding your task"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>", methods=['DELETE', 'GET'])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return "There was a issue deleting your task"


@app.route("/update/<int:id>", methods=[ 'GET','POST',])
def update(id):
    task=Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Issue updating"

    else:
        return render_template("update.html",task=task)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
