
def test_projects_list_unauthorized(client):
    response = client.get("/projects")
    assert response.status_code == 401

