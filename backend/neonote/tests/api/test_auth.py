from fastapi import status
from fastapi.testclient import TestClient

from neonote.models.user import User, UserPublic


def test_login(client: TestClient, superuser: User):
    response = client.post(
        "api/login", data={"username": "admin", "password": "password"}
    )
    assert response.status_code == status.HTTP_200_OK
    UserPublic.model_validate(response.json())
    assert "neonote_token" in response.cookies
    assert response.cookies["neonote_token"] is not None
    assert "neonote_token" in client.cookies


def test_login_with_incorrect_password(client: TestClient):
    response = client.post("api/login", data={"username": "admin", "password": "wrong"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Incorrect username or password"}


def test_login_with_incorrect_username(client: TestClient):
    response = client.post(
        "api/login", data={"username": "wrong", "password": "password"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Incorrect username or password"}


def test_logout(client: TestClient):
    response = client.post(
        "api/login", data={"username": "admin", "password": "password"}
    )
    response = client.post("api/logout")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert "neonote_token" not in client.cookies


def test_whoami(auth_client: TestClient):
    response = auth_client.get("api/whoami")
    assert response.status_code == 200
    UserPublic.model_validate(response.json())


# WITHOUT AUTH


def test_lagout_without_auth(client: TestClient):
    response = client.post("api/logout")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_whoami_without_auth(client: TestClient):
    response = client.get("api/whoami")
    assert response.status_code == status.HTTP_403_FORBIDDEN
