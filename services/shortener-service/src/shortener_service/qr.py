from __future__ import annotations

import io
from typing import TYPE_CHECKING

import qrcode

if TYPE_CHECKING:
    from qrcode.image.pil import PilImage


def generate_qr_png(data: str, box_size: int = 10, border: int = 2) -> io.BytesIO:
    img: PilImage = qrcode.make(
        data,
        box_size=box_size,
        border=border,
    )
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
