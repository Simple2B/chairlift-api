from http import HTTPStatus
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import schema
from app import model
from app.controller import mail

USER_NAME = "michael"
USER_EMAIL = "test@test.ku"
USER_PASSWORD = "secret"
USER_GOOGLE_ID = "123456789"


def test_google_auth(client: TestClient, db: Session):
    request = schema.UserGoogleLogin(
        email=USER_EMAIL,
        username=USER_NAME,
        google_openid_key=USER_GOOGLE_ID,
    )

    user: model.User = db.query(model.User).filter_by(email=USER_EMAIL).first()

    # Checking if user logged in via google succesfully
    response = client.post("/api/google_login", json=request.dict())
    assert response and response.ok, "unexpected response"

    # Checking if token exists
    token = schema.Token.parse_obj(response.json())
    assert token.access_token

    user: model.User = db.query(model.User).filter_by(email=USER_EMAIL).first()
    response = client.post("/api/google_login", json=request.dict())
    assert response and response.ok, "unexpected response"

    # Checking for existing of token
    token = schema.Token.parse_obj(response.json())
    assert token.access_token

    # Checking if user's google open id key stays the same
    user: model.User = db.query(model.User).filter_by(email=USER_EMAIL).first()
    assert user.google_openid_key == USER_GOOGLE_ID


def test_sign_up_and_email_password_reset(client: TestClient, db: Session):
    # Mocking email sending
    request_data = schema.UserSignUp(email=USER_EMAIL, username=USER_NAME)

    # Testing email
    with mail.record_messages() as outbox:
        response = client.post("/api/sign_up", json=request_data.dict())
        assert response.status_code == 200
        assert len(outbox) == 1

    # Testing if user exists
    user = db.query(model.User).filter_by(email=USER_EMAIL).first()

    assert not user.is_verified
    assert user.verification_token
    assert response.status_code == 200

    # Checking if user trying to sign up with the same credentials
    response = client.post("/api/sign_up", json=request_data.dict())
    assert response.status_code == HTTPStatus.CONFLICT


def test_reset_password(client: TestClient, db: Session):
    # create new user
    user = model.User(username=USER_NAME, email=USER_EMAIL, password=USER_PASSWORD)

    db.add(user)
    db.commit()
    db.refresh(user)
    assert not user.is_verified

    data_reset_password = schema.ResetPasswordData(
        password=USER_PASSWORD, verification_token=user.verification_token
    )
    response = client.post("api/user/reset_password", json=data_reset_password.dict())

    assert response.ok

    user = db.query(model.User).filter_by(email=USER_EMAIL).first()

    assert not user.verification_token
    assert user.is_verified


def test_login(client: TestClient, db: Session):
    # create new user
    user = model.User(username=USER_NAME, email=USER_EMAIL, password=USER_PASSWORD)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Check if current user is not verified
    response = client.post(
        "/api/login", data=dict(username=USER_EMAIL, password=USER_PASSWORD)
    )
    assert response.status_code == HTTPStatus.NOT_ACCEPTABLE

    # making user verified
    user = db.query(model.User).get(user.id)
    user.is_verified = True
    db.commit()

    # login by username and password
    response = client.post(
        "/api/login", data=dict(username=USER_EMAIL, password=USER_PASSWORD)
    )
    assert response and response.ok, "unexpected response"

    token = schema.Token.parse_obj(response.json())
    headers = {"Authorization": f"Bearer {token.access_token}"}

    # get user by id
    response = client.get(f"/api/user/{user.id}", headers=headers)
    assert response and response.ok
    user = schema.UserOut.parse_obj(response.json())
    assert user.username == USER_NAME
