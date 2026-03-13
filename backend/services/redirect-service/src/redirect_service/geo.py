from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import geoip2.database

logger = logging.getLogger(__name__)

_reader: geoip2.database.Reader | None = None
_unavailable = False


def _get_reader() -> geoip2.database.Reader | None:
    global _reader, _unavailable  # noqa: PLW0603
    if _unavailable:
        return None
    if _reader is not None:
        return _reader
    try:
        import geoip2.database  # noqa: PLC0415

        _reader = geoip2.database.Reader("/data/GeoLite2-Country.mmdb")
    except Exception:
        logger.warning("GeoIP database not available, country lookup disabled")
        _unavailable = True
        return None
    return _reader


def lookup_country(ip_address: str) -> str:
    reader = _get_reader()
    if reader is None:
        return ""
    try:
        resp = reader.country(ip_address)
    except Exception:
        return ""
    else:
        return resp.country.iso_code or ""
