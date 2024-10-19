import uuid
from flask import Flask, request, jsonify
from flask_uuid import FlaskUUID
from models.task import Task

app = Flask(__name__)
FlaskUUID(app)

tasks = []

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    new_task = Task(
        id=uuid.uuid4(),
        title=data.get("title"),
        description=data.get("description", "")
    )
    tasks.append(new_task)
    return jsonify({"message": "Nova tarefa criada com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True)