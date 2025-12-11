def test_projects_list_unauthorized(client):
    response = client.get("/projects")
    assert response.status_code == 401


def test_projects_authorized_empty_list(client, register_and_login):
    token = register_and_login("testuser65", "Test1234", "test65@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    r = client.get("/projects", headers=headers)
    assert r.status_code == 200
    assert r.json() == []
