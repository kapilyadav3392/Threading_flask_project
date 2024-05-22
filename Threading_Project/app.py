from flask import Flask, request, jsonify
from flask_restful import Api, Resource
import threading
import time
import uuid

app = Flask(__name__)
api = Api(app)

# Dictionary to store task status
tasks = {}

def long_running_task(task_id):
    # Simulate a long-running task
    time.sleep(20)  # Replace with the actual long task
    tasks[task_id]['status'] = 'completed'

class LongTask(Resource):
    def post(self):
        # Create a unique task ID
        task_id = str(uuid.uuid4())
        
        # Add task to the tasks dictionary with status 'pending'
        tasks[task_id] = {'status': 'pending'}
        
        # Start the background task
        thread = threading.Thread(target=long_running_task, args=(task_id,))
        thread.start()
        
        return {'task_id': task_id, 'status': 'pending'}, 202

class TaskStatus(Resource):
    def get(self, task_id):
        if task_id in tasks:
            return tasks[task_id]
        else:
            return {'message': 'Task not found'}, 404

api.add_resource(LongTask, '/longtask')
api.add_resource(TaskStatus, '/taskstatus/<string:task_id>')

if __name__ == '__main__':
    app.run(debug=True)
