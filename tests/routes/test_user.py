from pytest import MonkeyPatch
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
import app.model as m
import app.schema as s
from app.controller import MailClient
from tests.conftest import get_test_settings

settings = get_test_settings()

USER_NAME = "michael"
USER_EMAIL = settings.TEST_TARGET_EMAIL
USER_PASSWORD = "secret"
USER_PICTURE_URL = "uploads/image.png"


def test_forget_password(
    client: TestClient,
    db: Session,
    mail_client: MailClient,
    monkeypatch=MonkeyPatch,
):

    # creating user
    user = m.User(
        email=USER_EMAIL,
        username=USER_NAME,
        password=USER_PASSWORD,
        picture=USER_PICTURE_URL,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Testing if email has been sent
    with mail_client.mail.record_messages() as outbox:
        request = s.EmailSchema(email=USER_EMAIL)
        response = client.post("/api/user/forgot_password", json=request.dict())
        assert response.status_code == 200
        assert len(outbox) == 1
