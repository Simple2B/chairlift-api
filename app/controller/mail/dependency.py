from functools import lru_cache
from fastapi import Depends
from app.config import get_settings, Settings
from .mail_client import MailClient


@lru_cache
def get_mail_client(settings: Settings = Depends(get_settings)):
    return MailClient(settings)
