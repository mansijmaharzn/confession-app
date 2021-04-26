from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET', 'POST'])
def home():
    allTodo = Todo.query.all()
    allTodo = allTodo.reverse()
    return render_template('index.html', allTodo=allTodo)


@app.route('/createpost', methods=['GET', 'POST'])
def createpost():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('createpost.html')


@ app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('moderation'))


@ app.route('/moderation')
def moderation():
    allTodo = Todo.query.all()
    return render_template('moderation.html', allTodo=allTodo)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
