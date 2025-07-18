from fastapi import status
from fastapi.testclient import TestClient

from app.models.user import UpdatePassword, UserPublic, UserUpdate


def test_update_password_me(auth_client: TestClient):
    update_password = UpdatePassword(
        current_password="password", new_password="new_password"
    )
    response = auth_client.patch(
        "api/users/me/password", json=update_password.model_dump()
    )

    # reset password (temporary solution)
    reset_password = UpdatePassword(
        current_password="new_password", new_password="password"
    )
    auth_client.patch("api/users/me/password", json=reset_password.model_dump())

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_password_me_with_incorrect_password(auth_client: TestClient):
    update_password = UpdatePassword(
        current_password="wrong password", new_password="new_password"
    )
    response = auth_client.patch(
        "api/users/me/password", json=update_password.model_dump()
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_password_me_with_same_password(auth_client: TestClient):
    update_password = UpdatePassword(
        current_password="password", new_password="password"
    )
    response = auth_client.patch(
        "api/users/me/password", json=update_password.model_dump()
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    print(response.json())
    assert response.json() == {
        "detail": "New password must be different from the current one."
    }


def test_update_user_me_username(auth_client: TestClient):
    update_user = UserUpdate(username="new_username")
    response = auth_client.patch(
        "api/users/me", json=update_user.model_dump(exclude_unset=True)
    )
    assert response.status_code == status.HTTP_200_OK
    updated_user = UserPublic.model_validate(response.json())
    assert update_user.username == updated_user.username


def test_update_user_me_email(auth_client: TestClient):
    update_user = UserUpdate(email="new_email@example.com")
    response = auth_client.patch(
        "api/users/me", json=update_user.model_dump(exclude_unset=True)
    )
    assert response.status_code == status.HTTP_200_OK
    updated_user = UserPublic.model_validate(response.json())
    assert update_user.email == updated_user.email


# WITHOUT AUTH


def test_update_password_me_without_auth(client: TestClient):
    update_password = UpdatePassword(
        current_password="password", new_password="new_password"
    )
    response = client.patch("api/users/me/password", json=update_password.model_dump())
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_user_me_username_without_auth(client: TestClient):
    update_user = UserUpdate(username="new_username")
    response = client.patch(
        "api/users/me", json=update_user.model_dump(exclude_unset=True)
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_user_me_email_without_auth(client: TestClient):
    update_user = UserUpdate(email="new_email@example.com")
    response = client.patch(
        "api/users/me", json=update_user.model_dump(exclude_unset=True)
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
