from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.menu_item import MenuItem
from app.models.order import OrderItem, Order

SEASON_MAP = {1: "winter", 2: "winter", 3: "spring", 4: "spring", 5: "spring",
              6: "summer", 7: "summer", 8: "summer", 9: "autumn", 10: "autumn",
              11: "autumn", 12: "winter"}

SEASON_LABEL = {"spring": "봄", "summer": "여름", "autumn": "가을", "winter": "겨울"}


class RecommendationService:
    @staticmethod
    def recommend(db: Session, store_id: str, exclude_menu_ids: list[str], limit: int = 3) -> list[dict]:
        now = datetime.now(timezone.utc)
        current_season = SEASON_MAP[now.month]

        # 인기 메뉴: 전체 주문 횟수 기준
        popular = (
            db.query(OrderItem.menu_item_id, func.sum(OrderItem.quantity).label("cnt"))
            .join(Order, Order.id == OrderItem.order_id)
            .filter(Order.store_id == store_id)
            .group_by(OrderItem.menu_item_id)
            .order_by(func.sum(OrderItem.quantity).desc())
            .all()
        )
        popular_ids = [r[0] for r in popular if r[0] not in exclude_menu_ids]

        # 계절 메뉴
        season_menus = (
            db.query(MenuItem)
            .filter(MenuItem.store_id == store_id, MenuItem.season_tag == current_season,
                    MenuItem.id.notin_(exclude_menu_ids))
            .all()
        )
        season_ids = [m.id for m in season_menus]

        # 점수: 계절+인기 > 계절 > 인기 > 나머지
        all_menus = db.query(MenuItem).filter(
            MenuItem.store_id == store_id, MenuItem.id.notin_(exclude_menu_ids)
        ).all()
        menu_map = {m.id: m for m in all_menus}

        pop_rank = {mid: i for i, mid in enumerate(popular_ids)}

        def score(m):
            s = 0
            if m.id in season_ids:
                s += 1000
            if m.id in pop_rank:
                s += 500 - pop_rank[m.id]
            return s

        ranked = sorted(all_menus, key=score, reverse=True)[:limit]

        season_label = SEASON_LABEL[current_season]
        results = []
        for m in ranked:
            reasons = []
            if m.id in pop_rank:
                reasons.append("🔥 인기 메뉴")
            if m.id in season_ids:
                reasons.append(f"🌸 {season_label} 추천")
            if not reasons:
                reasons.append("👨‍🍳 셰프 추천")
            results.append({
                "menu_item_id": m.id, "name": m.name, "price": m.price,
                "image_url": m.image_url, "reason": " · ".join(reasons),
            })
        return results
