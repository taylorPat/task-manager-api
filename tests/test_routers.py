def test_create_task(client):
    response = client.post(
        "v1/tasks/", json={"title": "Test task", "description": "Test description"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test task"
    assert response.json()["description"] == "Test description"


def test_get_all_tasks(client):
    response = client.get("v1/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
