from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import os
import pymysql

app = Flask(__name__)
api = Api(app)

# Get MySQL Configuration from Environment Variables
db_host = os.environ.get('DB_HOST', 'localhost')
db_user = os.environ.get('DB_USER', 'username')
db_password = os.environ.get('DB_PASSWORD', 'password')
db_name = os.environ.get('DB_NAME', 'todo_app_db')

def get_db_connection():
    try:
        connection = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name, cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


class TaskList(Resource):
    def get(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        connection.close()
        return jsonify(tasks)

    def post(self):
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO tasks (title, description, completed) VALUES (%s, %s, %s)', (data['title'], data.get('description', ''), data.get('completed', False)))
        connection.commit()
        task_id = cursor.lastrowid
        connection.close()
        return jsonify({'id': task_id, 'title': data['title'], 'description': data.get('description', ''), 'completed': data.get('completed', False)}), 201

class Task(Resource):
    def put(self, task_id):
        data = request.json
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('UPDATE tasks SET title = %s, description = %s, completed = %s WHERE id = %s', (data.get('title', ''), data.get('description', ''), data.get('completed', False), task_id))
        connection.commit()
        connection.close()
        return jsonify({'id': task_id, 'title': data.get('title', ''), 'description': data.get('description', ''), 'completed': data.get('completed', False)})

    def delete(self, task_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
        connection.commit()
        connection.close()
        return '', 204

api.add_resource(TaskList, '/tasks')
api.add_resource(Task, '/tasks/<int:task_id>')

if __name__ == '__main__':
    app.run(debug=True)
