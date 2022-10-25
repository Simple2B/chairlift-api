from pytest import MonkeyPatch
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

import app.model as m
import app.schema as s
from app.config import settings as conf
from app.controller.mail import mail

USER_NAME = "michael"
USER_EMAIL = conf.TEST_TARGET_EMAIL
USER_PASSWORD = "secret"
USER_GOOGLE_ID = "123456789"
USER_PICTURE_URL = "uploads/image.png"
USER_ID = 12345


def test_model_relations(db: Session, test_data: dict):
    for user in test_data["test_users"]:
        user_model: m.User = m.User(
            username=user["username"], password=user["password"], email=user["email"]
        )

        db.add(user_model)
        db.commit()

    assert len(db.query(m.User).all()) == len(test_data["test_users"])

    user_model = (
        db.query(m.User)
        .filter_by(username=test_data["test_users"][0]["username"])
        .first()
    )

    for group in test_data["test_groups"]:
        group["group_owner"] = user_model.id
        group_model: m.Group = m.Group(**group)

        db.add(group_model)
        db.commit()

    db.refresh(user_model)

    assert len(user_model.own_groups) == len(test_data["test_groups"])


def test_forget_password(client: TestClient, db: Session, monkeypatch=MonkeyPatch):

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
    with mail.record_messages() as outbox:
        request = s.EmailSchema(email=USER_EMAIL)
        response = client.post("/api/user/forgot_password", json=request.dict())
        assert response.status_code == 200
        assert len(outbox) == 1


def test_create_user_subscription(db: Session):
    # check if subscription belongs to users
    user = m.User(
        id=USER_ID,
        email=USER_EMAIL,
        username=USER_NAME,
        password=USER_PASSWORD,
        picture=USER_PICTURE_URL,
    )
    subscription = m.Subscription(user_id=user.id)
    db.add(user)
    db.add(subscription)
    db.commit()
    assert user.subscription

    # check if subscription DOES NOT belong to users
    user2 = m.User(
        id=54321,
        email="non_existing_user@gmail.com",
        username="non_existing_username",
        password=USER_PASSWORD,
        picture=USER_PICTURE_URL,
    )
    subscription2 = m.Subscription(user_id=999)
    db.add(user2)
    db.add(subscription2)
    db.commit()
    assert not user2.subscription
