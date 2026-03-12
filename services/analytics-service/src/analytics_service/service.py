from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from analytics_service.models import Click


async def get_url_stats(session: AsyncSession, short_code: str) -> dict:
    total = await session.scalar(
        select(func.count()).where(Click.short_code == short_code)
    )

    recent_clicks = (
        await session.execute(
            select(Click)
            .where(Click.short_code == short_code)
            .order_by(Click.clicked_at.desc())
            .limit(20)
        )
    ).scalars().all()

    referrers = (
        await session.execute(
            select(Click.referrer, func.count().label("count"))
            .where(Click.short_code == short_code, Click.referrer != "")
            .group_by(Click.referrer)
            .order_by(func.count().desc())
            .limit(10)
        )
    ).all()

    return {
        "short_code": short_code,
        "total_clicks": total or 0,
        "top_referrers": [{"referrer": r, "count": c} for r, c in referrers],
        "recent_clicks": [
            {
                "ip_address": c.ip_address,
                "user_agent": c.user_agent,
                "referrer": c.referrer,
                "clicked_at": c.clicked_at.isoformat() if c.clicked_at else None,
            }
            for c in recent_clicks
        ],
    }
