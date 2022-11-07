from sqlalchemy.orm import Session
import app.model as m
from tests.conftest import get_test_settings

settings = get_test_settings()

USER_NAME = "michael"
USER_EMAIL = settings.TEST_TARGET_EMAIL
USER_PICTURE_URL = "uploads/image.png"
USER_PASSWORD = "secret"


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


def test_create_user_subscription(db: Session):
    # check if subscription belongs to users
    user = m.User(
        email=USER_EMAIL,
        username=USER_NAME,
        password=USER_PASSWORD,
        picture=USER_PICTURE_URL,
    )
    db.add(user)
    db.commit()

    subscription = m.Subscription(user_id=user.id)
    db.add(subscription)
    db.commit()
    assert user.subscription

    # check if subscription DOES NOT belong to users
    user2 = m.User(
        email="non_existing_user@gmail.com",
        username="non_existing_username",
        password=USER_PASSWORD,
        picture=USER_PICTURE_URL,
    )
    db.add(user2)
    db.commit()
    subscription2 = m.Subscription(user_id=user.id)
    db.add(subscription2)
    db.commit()
    assert not user2.subscription
