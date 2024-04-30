from flask import Flask, render_template, request, redirect, url_for, flash
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

DB_PATH = 'tasks.db'


def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, title TEXT, description TEXT, start_date DATE, end_date DATE, status TEXT)''')
    conn.commit()
    conn.close()

def add_task(title, description, start_date, end_date, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description, start_date, end_date, status) VALUES (?, ?, ?, ?, ?)",
              (title, description, start_date, end_date, status))
    conn.commit()
    conn.close()


def get_tasks(status=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if status:
        c.execute("SELECT * FROM tasks WHERE status=?", (status,))
    else:
        c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks


def update_task(task_id, title, description, start_date, end_date, status):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE tasks SET title=?, description=?, start_date=?, end_date=?, status=? WHERE id=?",
              (title, description, start_date, end_date, status, task_id))
    conn.commit()
    conn.close()


def get_task_by_id(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = c.fetchone()
    conn.close()
    return task


def get_task_statuses():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT DISTINCT status FROM tasks")
    statuses = [row[0] for row in c.fetchall()]
    conn.close()
    return statuses


def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()


@app.route('/')
def index():
    if not os.path.exists(DB_PATH):
        create_table()
    return render_template('index.html', tasks=get_tasks(), statuses=get_task_statuses(), edit_task=None)


@app.route('/filter', methods=['POST'])
def filter_tasks():
    status = request.form['status']
    if status == 'All':
        return redirect(url_for('index'))
    return render_template('index.html', tasks=get_tasks(status), statuses=get_task_statuses(), edit_task=None)


@app.route('/add_task', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    status = request.form['status']
    add_task(title, description, start_date, end_date, status)
    flash('Task added successfully', 'success')
    return redirect(url_for('index'))


@app.route('/edit_task_form/<int:task_id>', methods=['POST'])
def edit_task_form(task_id):
    task = get_task_by_id(task_id)
    return render_template('index.html', tasks=get_tasks(), statuses=get_task_statuses(), edit_task=task)


@app.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    title = request.form['title']
    description = request.form['description']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    status = request.form['status']
    update_task(task_id, title, description, start_date, end_date, status)
    flash('Task updated successfully', 'success')
    return redirect(url_for('index'))


@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task_view(task_id):
    delete_task(task_id)
    flash('Task deleted successfully', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
