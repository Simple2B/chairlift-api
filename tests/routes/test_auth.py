from pytest import MonkeyPatch
from http import HTTPStatus
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import schema as s
from app import model as m
from app.controller import MailClient
from app.config import Settings
from tests.conftest import get_test_settings

settings: Settings = get_test_settings()

USER_NAME = "michael"
USER_EMAIL = settings.TEST_TARGET_EMAIL
USER_PASSWORD = "secret"
USER_GOOGLE_ID = "123456789"
USER_PICTURE_URL = "uploads/image.png"


def test_google_auth(client: TestClient, db: Session):
    request = s.UserGoogleLogin(
        email=USER_EMAIL,
        username=USER_NAME,
        google_openid_key=USER_GOOGLE_ID,
        picture=USER_PICTURE_URL,
    )

    user: m.User = db.query(m.User).filter_by(email=USER_EMAIL).first()
    # Checking if user logged in via google succesfully
    response = client.post("/api/google_login", json=request.dict())
    assert response and response.ok, "unexpected response"

    # Checking if token exists
    token = s.Token.parse_obj(response.json())
    assert token.access_token

    user: m.User = db.query(m.User).filter_by(email=USER_EMAIL).first()
    response = client.post("/api/google_login", json=request.dict())
    assert response and response.ok, "unexpected response"

    # Checking for existing of token
    token = s.Token.parse_obj(response.json())
    assert token.access_token

    # Checking if user's google open id key stays the same
    user: m.User = db.query(m.User).filter_by(email=USER_EMAIL).first()
    assert user.google_openid_key == USER_GOOGLE_ID


def test_signup_and_email_password_reset(
    client: TestClient, db: Session, mail_client: MailClient
):
    # Mocking email sending
    request_data = s.UserSignUp(email=USER_EMAIL, username=USER_NAME)

    # Testing email
    with mail_client.mail.record_messages() as outbox:
        response = client.post("/api/sign_up", json=request_data.dict())
        assert response.status_code == 200
        assert len(outbox) == 1

    # Testing if user exists
    user = db.query(m.User).filter_by(email=USER_EMAIL).first()

    assert not user.is_verified
    assert user.verification_token
    assert response.status_code == 200

    # Checking if user trying to sign up with the same credentials
    response = client.post("/api/sign_up", json=request_data.dict())
    assert response.status_code == HTTPStatus.CONFLICT


def test_signup_and_fail_send_email(
    client: TestClient, db: Session, monkeypatch: MonkeyPatch
):
    from app import controller

    def mock_send_email(
        self: MailClient,
        email: s.EmailListSchema,
        username: str,
        verification_link: str,
    ):
        from smtplib import SMTPAuthenticationError

        assert email
        assert username
        assert verification_link

        raise SMTPAuthenticationError(code=56, msg="Test ERROR")

    monkeypatch.setattr(
        controller.mail.mail_client.MailClient, "send_email", mock_send_email
    )
    response = client.post(
        "/api/sign_up",
        json=s.UserSignUp(email=USER_EMAIL, username=USER_NAME).dict(),
    )

    assert not response
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert not db.query(m.User).count()


def test_reset_password(client: TestClient, db: Session):
    # create new user
    user = m.User(username=USER_NAME, email=USER_EMAIL, password=USER_PASSWORD)

    db.add(user)
    db.commit()
    db.refresh(user)
    assert not user.is_verified

    data_reset_password = s.ResetPasswordData(
        password=USER_PASSWORD, verification_token=user.verification_token
    )
    response = client.post("api/user/reset_password", json=data_reset_password.dict())

    assert response.ok

    user: m.User = db.query(m.User).filter_by(email=USER_EMAIL).first()

    assert user.verification_token
    assert user.is_verified


def test_login(client: TestClient, db: Session):
    # create new user
    user = m.User(
        username=USER_NAME,
        email=USER_EMAIL,
        password=USER_PASSWORD,
        picture=USER_PICTURE_URL,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Check if current user is not verified
    response = client.post(
        "/api/login", data=dict(username=USER_EMAIL, password=USER_PASSWORD)
    )
    assert response.status_code == HTTPStatus.NOT_ACCEPTABLE

    # making user verified
    user: m.User = db.query(m.User).get(user.id)
    user.is_verified = True
    db.commit()

    # login by username and password
    response = client.post(
        "/api/login", data=dict(username=USER_EMAIL, password=USER_PASSWORD)
    )
    assert response and response.ok, "unexpected response"

    # get user by id
    user: m.User = (
        db.query(m.User).filter_by(username=USER_NAME, email=USER_EMAIL).first()
    )
    assert user.username == USER_NAME
    assert user.email == USER_EMAIL
