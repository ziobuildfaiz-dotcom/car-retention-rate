"""Seed the database with sample retention rate data for major car brands."""

import random
from datetime import date

from app.database import Base, SessionLocal, engine
from app.models import Brand, BrandSeries, CarModel, RetentionRate

SEED_DATA = {
    "丰田": {
        "country": "日系",
        "series": {
            "卡罗拉": {
                "type": "轿车",
                "models": [
                    ("2022款 1.2T S-CVT 先锋版", 2022, 11.98, "1.2T", "汽油", "CVT"),
                    ("2021款 1.2T S-CVT 精英版", 2021, 12.88, "1.2T", "汽油", "CVT"),
                    ("2020款 1.2T S-CVT 豪华版", 2020, 13.58, "1.2T", "汽油", "CVT"),
                    ("2022款 双擎 1.8L E-CVT 先锋版", 2022, 13.58, "1.8L", "混动", "E-CVT"),
                    ("2020款 双擎 1.8L E-CVT 精英版", 2020, 14.38, "1.8L", "混动", "E-CVT"),
                ],
            },
            "凯美瑞": {
                "type": "轿车",
                "models": [
                    ("2022款 2.0E 精英版", 2022, 17.98, "2.0L", "汽油", "CVT"),
                    ("2021款 2.0G 豪华版", 2021, 19.98, "2.0L", "汽油", "CVT"),
                    ("2022款 双擎 2.5HG 豪华版", 2022, 23.98, "2.5L", "混动", "E-CVT"),
                    ("2020款 2.5Q 旗舰版", 2020, 25.98, "2.5L", "汽油", "AT"),
                ],
            },
            "RAV4荣放": {
                "type": "SUV",
                "models": [
                    ("2022款 2.0L CVT 两驱都市版", 2022, 17.58, "2.0L", "汽油", "CVT"),
                    ("2021款 2.0L CVT 两驱风尚版", 2021, 19.58, "2.0L", "汽油", "CVT"),
                    ("2020款 双擎 2.5L E-CVT 四驱精英版", 2020, 23.78, "2.5L", "混动", "E-CVT"),
                ],
            },
            "汉兰达": {
                "type": "SUV",
                "models": [
                    ("2022款 2.0T 四驱尊贵版 7座", 2022, 30.98, "2.0T", "汽油", "AT"),
                    ("2021款 2.5L 双擎 四驱尊贵版 7座", 2021, 32.98, "2.5L", "混动", "E-CVT"),
                    ("2020款 2.0T 两驱精英版 5座", 2020, 23.98, "2.0T", "汽油", "AT"),
                ],
            },
        },
    },
    "本田": {
        "country": "日系",
        "series": {
            "思域": {
                "type": "轿车",
                "models": [
                    ("2022款 180TURBO CVT 尚擎版", 2022, 13.69, "1.5T", "汽油", "CVT"),
                    ("2021款 240TURBO CVT 劲动版", 2021, 14.29, "1.5T", "汽油", "CVT"),
                    ("2020款 220TURBO CVT 燃动版", 2020, 14.59, "1.5T", "汽油", "CVT"),
                ],
            },
            "雅阁": {
                "type": "轿车",
                "models": [
                    ("2022款 260TURBO CVT 豪华版", 2022, 19.28, "1.5T", "汽油", "CVT"),
                    ("2021款 锐·混动 2.0L E-CVT 锐智版", 2021, 23.68, "2.0L", "混动", "E-CVT"),
                    ("2020款 260TURBO CVT 尊贵版", 2020, 20.98, "1.5T", "汽油", "CVT"),
                ],
            },
            "CR-V": {
                "type": "SUV",
                "models": [
                    ("2022款 240TURBO CVT 两驱风尚版", 2022, 19.58, "1.5T", "汽油", "CVT"),
                    ("2021款 锐·混动 2.0L E-CVT 两驱净驰版", 2021, 24.18, "2.0L", "混动", "E-CVT"),
                ],
            },
        },
    },
    "大众": {
        "country": "德系",
        "series": {
            "朗逸": {
                "type": "轿车",
                "models": [
                    ("2022款 1.5L 自动风尚版", 2022, 12.49, "1.5L", "汽油", "AT"),
                    ("2021款 1.4TSI DSG 舒适版", 2021, 14.69, "1.4T", "汽油", "DSG"),
                    ("2020款 1.5L 自动舒适版", 2020, 13.69, "1.5L", "汽油", "AT"),
                ],
            },
            "帕萨特": {
                "type": "轿车",
                "models": [
                    ("2022款 330TSI DSG 精英版", 2022, 20.39, "2.0T", "汽油", "DSG"),
                    ("2021款 380TSI DSG 豪华版", 2021, 24.09, "2.0T", "汽油", "DSG"),
                ],
            },
            "途观L": {
                "type": "SUV",
                "models": [
                    ("2022款 330TSI DSG 两驱智享版", 2022, 21.78, "2.0T", "汽油", "DSG"),
                    ("2021款 380TSI DSG 四驱R-Line 越享版7座", 2021, 26.98, "2.0T", "汽油", "DSG"),
                ],
            },
        },
    },
    "比亚迪": {
        "country": "自主",
        "series": {
            "秦PLUS": {
                "type": "轿车",
                "models": [
                    ("2022款 DM-i 55KM 尊贵型", 2022, 11.18, "1.5L", "插混", "E-CVT"),
                    ("2021款 EV 500KM 豪华型", 2021, 13.98, None, "纯电", "AT"),
                ],
            },
            "汉": {
                "type": "轿车",
                "models": [
                    ("2022款 EV 创世版 715KM 前驱尊荣型", 2022, 26.98, None, "纯电", "AT"),
                    ("2022款 DM-i 121KM 尊贵型", 2022, 21.78, "1.5T", "插混", "E-CVT"),
                ],
            },
            "宋PLUS": {
                "type": "SUV",
                "models": [
                    ("2022款 DM-i 110KM 旗舰型", 2022, 15.78, "1.5L", "插混", "E-CVT"),
                    ("2021款 EV 505KM 尊贵型", 2021, 16.98, None, "纯电", "AT"),
                ],
            },
        },
    },
    "奔驰": {
        "country": "德系",
        "series": {
            "C级": {
                "type": "轿车",
                "models": [
                    ("2022款 C 200 L 运动版", 2022, 32.52, "1.5T", "汽油", "AT"),
                    ("2021款 C 260 L 运动星耀臻藏版", 2021, 35.68, "1.5T", "汽油", "AT"),
                ],
            },
            "GLC": {
                "type": "SUV",
                "models": [
                    ("2022款 GLC 260 L 4MATIC 动感型", 2022, 40.63, "2.0T", "汽油", "AT"),
                    ("2021款 GLC 300 L 4MATIC 豪华型", 2021, 47.98, "2.0T", "汽油", "AT"),
                ],
            },
        },
    },
    "宝马": {
        "country": "德系",
        "series": {
            "3系": {
                "type": "轿车",
                "models": [
                    ("2022款 320Li M运动套装", 2022, 32.19, "2.0T", "汽油", "AT"),
                    ("2021款 325Li M运动曜夜套装", 2021, 35.89, "2.0T", "汽油", "AT"),
                ],
            },
            "X3": {
                "type": "SUV",
                "models": [
                    ("2022款 xDrive25i M运动套装", 2022, 39.69, "2.0T", "汽油", "AT"),
                    ("2021款 xDrive30i 领先型 M曜夜套装", 2021, 47.98, "2.0T", "汽油", "AT"),
                ],
            },
        },
    },
}


def generate_retention(guide_price: float | None, fuel_type: str | None, vehicle_type: str | None) -> dict:
    """Generate realistic retention rates based on vehicle characteristics."""
    base_1yr = random.uniform(72, 88)
    base_3yr = random.uniform(55, 70)
    base_5yr = random.uniform(38, 55)

    if fuel_type == "混动" or fuel_type == "插混":
        base_1yr += random.uniform(1, 4)
        base_3yr += random.uniform(2, 5)
        base_5yr += random.uniform(2, 4)
    elif fuel_type == "纯电":
        base_1yr -= random.uniform(3, 8)
        base_3yr -= random.uniform(5, 12)
        base_5yr -= random.uniform(8, 15)

    if vehicle_type == "SUV":
        base_1yr += random.uniform(1, 3)
        base_3yr += random.uniform(1, 3)
        base_5yr += random.uniform(1, 2)

    if guide_price and guide_price > 30:
        base_1yr -= random.uniform(2, 5)
        base_3yr -= random.uniform(3, 6)
        base_5yr -= random.uniform(2, 5)

    return {
        "retention_1yr": round(min(base_1yr, 95), 1),
        "retention_2yr": round(min(base_1yr - random.uniform(4, 8), 90), 1),
        "retention_3yr": round(min(base_3yr, 82), 1),
        "retention_4yr": round(min(base_3yr - random.uniform(5, 9), 75), 1),
        "retention_5yr": round(min(base_5yr, 68), 1),
    }


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Brand).count() > 0:
        print("Database already has data, skipping seed.")
        db.close()
        return

    for brand_name, brand_data in SEED_DATA.items():
        brand = Brand(name=brand_name, country=brand_data["country"])
        db.add(brand)
        db.flush()

        for series_name, series_data in brand_data["series"].items():
            series = BrandSeries(
                brand_id=brand.id,
                name=series_name,
                vehicle_type=series_data["type"],
            )
            db.add(series)
            db.flush()

            for model_name, year, price, disp, fuel, trans in series_data["models"]:
                model = CarModel(
                    series_id=series.id,
                    model_year=year,
                    specific_model=model_name,
                    guide_price=price,
                    displacement=disp,
                    fuel_type=fuel,
                    transmission=trans,
                )
                db.add(model)
                db.flush()

                rates = generate_retention(price, fuel, series_data["type"])
                retention = RetentionRate(
                    model_id=model.id,
                    source="seed",
                    scrape_date=date(2025, 1, 15),
                    retention_1yr=rates["retention_1yr"],
                    retention_2yr=rates["retention_2yr"],
                    retention_3yr=rates["retention_3yr"],
                    retention_4yr=rates["retention_4yr"],
                    retention_5yr=rates["retention_5yr"],
                    avg_listed_price=round(price * rates["retention_3yr"] / 100, 2) if price else None,
                    sample_count=random.randint(50, 500),
                )
                db.add(retention)

    db.commit()
    model_count = db.query(CarModel).count()
    rate_count = db.query(RetentionRate).count()
    print(f"Seed complete: {db.query(Brand).count()} brands, {model_count} models, {rate_count} retention records")
    db.close()


if __name__ == "__main__":
    seed()
