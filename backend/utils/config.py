"""
utils/config.py
───────────────
Centralised settings loaded from .env via pydantic-settings.
"""

import os
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # MongoDB
    MONGO_URI: str         = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB:  str         = os.getenv("MONGO_DB",  "nids")

    # Redis
    REDIS_HOST: str        = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int        = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_PASSWORD: str    = os.getenv("REDIS_PASSWORD", "")

    # JWT
    SECRET_KEY: str        = os.getenv("SECRET_KEY", "dev-secret-change-me")
    ALGORITHM:  str        = os.getenv("ALGORITHM",  "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    # GeoIP
    GEOIP_API_KEY: str     = os.getenv("GEOIP_API_KEY", "")

    # Sniffer
    SNIFF_INTERFACE: str   = os.getenv("SNIFF_INTERFACE", "eth0")

    # ML
    ML_MODEL_PATH: str     = os.getenv("ML_MODEL_PATH", "./ml_model.pkl")

    # CORS
    CORS_ORIGINS: list[str] = [
        o.strip()
        for o in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:5173"
        ).split(",")
    ]

    # Redis channel for pub/sub
    REDIS_ALERT_CHANNEL: str = "nids:alerts"


@lru_cache
def get_settings() -> Settings:
    return Settings()