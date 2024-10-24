import pytest
import requests
import uuid

BASE_URL = "http://127.0.01:5000"
tasks = []

def test_create_task():
    task_data = {
        "title": "Mova tarefa - teste",
        "description": "Descrição nova tarefa - teste"
    }
    assert requests.post(f"{BASE_URL}/tasks",json=task_data).status_code == 201
    response_json = requests.get(f"{BASE_URL}/tasks").json()
    index_task = int(response_json["total_tasks"])
    assert uuid.UUID(response_json["tasks"][index_task - 1]["id"])
    tasks.append(response_json["tasks"][index_task - 1]["id"])
    
def test_get_all_tasks():
    assert requests.get(f"{BASE_URL}/tasks").status_code == 200
    response_json = requests.get(f"{BASE_URL}/tasks").json()
    assert "tasks" in response_json

def test_get_one_task():
    assert requests.get(f"{BASE_URL}/tasks/{tasks[0]}").status_code == 200
    response_json = requests.get(f"{BASE_URL}/tasks/{tasks[0]}").json()
    assert tasks[0] == response_json["id"]

def test_update_task():
    if tasks:
        payload = {
            "completed": False,
            "title": "Atualizado",
            "description": "Atualização concluída"
        }
        response = requests.put(f"{BASE_URL}/tasks/{tasks[0]}",
            json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert "message" in response_json

def test_delete_task():
    if tasks:
        assert requests.delete(
            f"{BASE_URL}/tasks/{tasks[0]}"
        ).status_code == 200
        assert tasks not in requests.get(f"{BASE_URL}/tasks")
