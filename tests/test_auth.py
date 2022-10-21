from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import schema
from app import model
from app.controller import fm

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
    assert not user

    response = client.post("/api/google_login", json=request.dict())
    assert response and response.ok, "unexpected response"

    token = schema.Token.parse_obj(response.json())
    assert token.access_token
    user: model.User = db.query(model.User).filter_by(email=USER_EMAIL).first()
    assert user

    response = client.post("/api/google_login", json=request.dict())
    assert response and response.ok, "unexpected response"
    token = schema.Token.parse_obj(response.json())
    assert token.access_token

    user: model.User = db.query(model.User).filter_by(email=USER_EMAIL).first()
    assert user
    assert user.google_openid_key == USER_GOOGLE_ID


def test_email_password_reset(client: TestClient, db: Session):
    fm.config.SUPPRESS_SEND = 1
    request = schema.UserSignUp(email=USER_EMAIL, username=USER_NAME)

    # Testing email
    with fm.record_messages() as outbox:
        response = client.post("/api/sign_up", json=request.dict())
        assert response.status_code == 200
        assert len(outbox) == 1

    # Testing user
    user = db.query(model.User).filter_by(email=USER_EMAIL).first()
    assert not user.is_verified
    assert user.verification_token
    assert response.status_code == 200
