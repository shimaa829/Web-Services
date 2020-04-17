import sqlite3
from sqlite3 import Error
from flask import Flask
# from flask import g
from flask import request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/employees', methods=['GET','POST'])
def getAllEmployees():
	if request.method == 'POST':
		name = request.form['name']
		salary = request.form['salary']
		conn = sqlite3.connect('employee.db')
		conn.execute("INSERT into Employees (name, salary) values (?,?)", (name,salary,))
		conn.commit()
		return "inserted successfully"
	elif request.method == 'GET':
		conn = sqlite3.connect('employee.db')
		cur = conn.cursor()
		cur.execute("SELECT * FROM employees")
		all_emp = cur.fetchall()
		return jsonify(all_emp)


@app.route('/employees/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def Employee(id):
	if request.method == 'GET':
		conn = sqlite3.connect('employee.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM employees WHERE id=?', (id,))
		emp = cur.fetchone()
		return jsonify(emp)
	elif request.method == 'PUT':
		return updateEmployee(id)
	elif request.method == 'DELETE':
		return deleteEmployee(id)

def updateEmployee(id):
	name = request.form['name']
	salary = request.form['salary']
	conn = sqlite3.connect('employee.db')
	cur = conn.cursor()
	cur.execute('''UPDATE employees SET name = ?,salary = ? WHERE id = ?''', (name, salary, id))
	conn.commit()
	return "updated successfully"


def deleteEmployee(id):
	conn = sqlite3.connect('employee.db')
	cur = conn.cursor()
	cur.execute("delete from Employees where id = ?", (id,))
	conn.commit()
	return "record successfully deleted"

app.run()