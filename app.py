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
    ## trecho abaixo criado para verificar último id criado
    #print(output['tasks'][len(task_list) - 1]['id'])
    return jsonify(output),200

@app.route("/tasks/<uuid:id>", methods=["GET"])
def get_one_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict())
    return jsonify({"message": "Não foi possível encontrar a task"}), 404

@app.route("/tasks/<uuid:id>", methods=["PUT"])
def update_task(id):
    for t in tasks:
        if t.id == id:
            data =  request.get_json()
            t.title = data.get("title")
            t.description = data.get("description")
            t.completed = data.get("completed")
            return jsonify({"message": "Tarefa atualizada com suscesso."})
    return jsonify({"message": "Não foi possível encontrar a task"}), 404

@app.route("/tasks/<uuid:id>", methods=["DELETE"])
def delete_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
            break
    if not task:
        return jsonify({"message": "Não foi possível encontrar a task"}), 404
    tasks.remove(task)
    return jsonify({"message": "Task apagada com sucesso."})

if __name__ == "__main__":
    app.run(debug=True)