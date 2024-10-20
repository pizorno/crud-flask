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
    return jsonify({"message": "Nova tarefa criada com sucesso!"}),201

@app.route("/tasks", methods=["GET"])
def get_all_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {"tasks": task_list, "total_tasks": len(task_list)}
    return jsonify(output),200

@app.route("/tasks/<uuid:id>", methods=["GET"])
def get_one_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    return jsonify({"message": "Não foi possível encontrar a task"}), 404

if __name__ == "__main__":
    app.run(debug=True)