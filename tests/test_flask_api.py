import pytest
import requests
import uuid

BASE_URL = "http://127.0.01:5000"
tasks = []

def test_create_task():
    new_task_data = {
        "title": "Mova tarefa - teste",
        "description": "Descrição nova tarefa - teste"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 201
    #response = requests.get(f"{BASE_URL}/tasks").json()
    response_json = requests.get(f"{BASE_URL}/tasks").json()
    #response_json = response.json()
    index_task = int(response_json["total_tasks"])
    assert uuid.UUID(response_json['tasks'][index_task - 1]['id'])
    tasks.append(response_json['tasks'][index_task - 1]['id'])
    

