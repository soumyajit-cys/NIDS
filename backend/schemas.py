"""
models/schemas.py
─────────────────
Pydantic v2 schemas used across the NIDS backend.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


# ─── Enums ────────────────────────────────────────────────────────────────────

class Severity(str, Enum):
    LOW    = "LOW"
    MEDIUM = "MEDIUM"
    HIGH   = "HIGH"


class Protocol(str, Enum):
    TCP   = "TCP"
    UDP   = "UDP"
    ICMP  = "ICMP"
    OTHER = "OTHER"


class AlertType(str, Enum):
    PORT_SCAN          = "PORT_SCAN"
    SYN_FLOOD          = "SYN_FLOOD"
    PAYLOAD_INJECTION  = "PAYLOAD_INJECTION"
    ML_ANOMALY         = "ML_ANOMALY"
    UNKNOWN            = "UNKNOWN"


# ─── Geo Location ─────────────────────────────────────────────────────────────

class GeoLocation(BaseModel):
    country:   Optional[str]  = None
    city:      Optional[str]  = None
    latitude:  Optional[float] = None
    longitude: Optional[float] = None
    isp:       Optional[str]  = None


# ─── Raw Packet ───────────────────────────────────────────────────────────────

class PacketData(BaseModel):
    """Represents a captured network packet."""
    timestamp:  datetime = Field(default_factory=datetime.utcnow)
    src_ip:     str
    dst_ip:     str
    src_port:   Optional[int]  = None
    dst_port:   Optional[int]  = None
    protocol:   Protocol       = Protocol.OTHER
    length:     int            = 0
    flags:      Optional[str]  = None   # TCP flags as string, e.g. "S", "SA"
    payload:    Optional[str]  = None   # hex or truncated ASCII


# ─── Alert ────────────────────────────────────────────────────────────────────

class Alert(BaseModel):
    """Structured intrusion alert."""
    id:          Optional[str]  = None   # MongoDB _id as str
    timestamp:   datetime       = Field(default_factory=datetime.utcnow)
    alert_type:  AlertType
    severity:    Severity
    src_ip:      str
    dst_ip:      Optional[str]  = None
    src_port:    Optional[int]  = None
    dst_port:    Optional[int]  = None
    protocol:    Optional[Protocol] = None
    description: str
    raw_data:    Optional[dict[str, Any]] = None
    geo:         Optional[GeoLocation]    = None
    acknowledged: bool = False

    model_config = {"populate_by_name": True}


# ─── Auth ─────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


# ─── API response wrappers ────────────────────────────────────────────────────

class PaginatedAlerts(BaseModel):
    total:  int
    page:   int
    limit:  int
    alerts: list[Alert]


class StatsResponse(BaseModel):
    total_alerts:      int
    alerts_by_type:    dict[str, int]
    alerts_by_severity: dict[str, int]
    top_src_ips:       list[dict[str, Any]]
    protocol_dist:     dict[str, int]
    timeline:          list[dict[str, Any]]   # [{timestamp, count}]