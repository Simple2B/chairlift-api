from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import model, schema

USER_NAME = "michael"
USER_EMAIL = "test@test.ku"
USER_PASSWORD = "secret"
USER_GOOGLE_ID = "123456789"


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

    assert len(user_model.own_groups) == len(test_data["test_groups"])
