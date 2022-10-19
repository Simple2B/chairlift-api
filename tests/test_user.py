from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import model, schema

USER_NAME = "michael"
USER_EMAIL = "test@test.ku"
USER_PASSWORD = "secret"
USER_GOOGLE_ID = '123456789'


def test_model_relations(db: Session, test_data: dict):
    for user in test_data["test_users"]:
        user_model: model.User = model.User(
            username=user["username"], password=user["password"], email=user["email"]
        )

        db.add(user_model)
        db.commit()

    assert len(db.query(model.User).all()) == len(test_data["test_users"])

    user_model = (
        db.query(model.User)
        .filter_by(username=test_data["test_users"][0]["username"])
        .first()
    )

    for group in test_data["test_groups"]:
        group["group_owner"] = user_model.id
        group_model: model.Group = model.Group(**group)

        db.add(group_model)
        db.commit()

    db.refresh(user_model)

    # TODO add many to many user_group check
    assert len(user_model.own_groups) == len(test_data["test_groups"])


def test_auth(client: TestClient, db: Session):
    # data = {"username": USER_NAME, "email": USER_EMAIL, "password": USER_PASSWORD}
    data = schema.UserCreate(
        username=USER_NAME,
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )
    # create new user
    response = client.post("api/user/", json=data.dict())
    assert response.status_code == HTTPStatus.CREATED

    new_user = schema.UserOut.parse_obj(response.json())
    user = db.query(model.User).get(new_user.id)
    assert user.username == new_user.username

    # check if email already exists
    data.username += "abc"
    response = client.post("/api/user/", json=data.dict())
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Email already exists"

    # check if username already exists
    data.username = USER_NAME
    data.email += "abc"
    response = client.post("/api/user/", json=data.dict())
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Username already exists"
    # login by username and password
    response = client.post(
        "/api/login", data=dict(username=USER_NAME, password=USER_PASSWORD)
    )
    assert response and response.ok, "unexpected response"
    token = schema.Token.parse_obj(response.json())
    headers = {"Authorization": f"Bearer {token.access_token}"}

    # get user by id
    response = client.get(f"/api/user/{new_user.id}", headers=headers)
    assert response and response.ok
    user = schema.UserOut.parse_obj(response.json())
    assert user.username == USER_NAME


def test_google_auth(client: TestClient, db: Session):
    data = schema.UserCreate(
        username=USER_NAME,
        email=USER_EMAIL,
        password=USER_GOOGLE_ID,
        google_openid_key=USER_GOOGLE_ID,
    )

    # create new user
    response = client.post("api/user/", json=data.dict())
    assert response.status_code == HTTPStatus.CREATED

    new_user = schema.UserOut.parse_obj(response.json())
    user = db.query(model.User).get(new_user.id)
    assert user.username == new_user.username

    # check if email already exists
    data.username += "abc"
    response = client.post("/api/user/", json=data.dict())
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Email already exists"

    # check if username already exists
    data.username = USER_NAME
    data.email += "abc"
    response = client.post("/api/user/", json=data.dict())
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Username already exists"

    # login by email and google_openid_key
    request = schema.UserGoogleLogin(email=USER_EMAIL,
                                     username=USER_NAME,
                                     google_openid_key=USER_GOOGLE_ID,)

    response = client.post("/api/google_login", data=request)
    assert response
    assert response and response.ok, "unexpected response"

    # ???
    # token = schema.Token.parse_obj(response.json())
    # headers = {"Authorization": f"Bearer {token.access_token}"}

    # get user by id
    # response = client.get(f"/user/{new_user.id}", headers=headers)
    # assert response and response.ok
    # user = schema.UserOut.parse_obj(response.json())
    # assert user.username == USER_NAME
