"""Generate a large, realistic seed dataset covering ~30 brands and ~500 models."""

import random
from datetime import date

from app.database import Base, SessionLocal, engine
from app.models import Brand, BrandSeries, CarModel, RetentionRate

# Brand → { country, retention_tier (1=best, 5=worst), series }
BRANDS = {
    # 日系 (high retention)
    "丰田":   {"country": "日系", "tier": 1, "series": ["卡罗拉","凯美瑞","RAV4荣放","汉兰达","亚洲龙","威兰达","锋兰达","雷凌","普拉多","赛那"]},
    "本田":   {"country": "日系", "tier": 1, "series": ["思域","雅阁","CR-V","皓影","XR-V","飞度","凌派","冠道","艾力绅","奥德赛"]},
    "雷克萨斯":{"country": "日系", "tier": 1, "series": ["ES","RX","NX","UX","LS","LX"]},
    "日产":   {"country": "日系", "tier": 2, "series": ["轩逸","天籁","逍客","奇骏","劲客","途达"]},
    "马自达": {"country": "日系", "tier": 3, "series": ["昂克赛拉","阿特兹","CX-5","CX-4","CX-30"]},
    "斯巴鲁": {"country": "日系", "tier": 2, "series": ["森林人","傲虎","XV"]},

    # 德系 (good retention)
    "奔驰":   {"country": "德系", "tier": 2, "series": ["C级","E级","S级","GLC","GLE","GLA","A级"]},
    "宝马":   {"country": "德系", "tier": 2, "series": ["3系","5系","X3","X5","X1","1系","4系"]},
    "奥迪":   {"country": "德系", "tier": 3, "series": ["A4L","A6L","Q5L","Q3","A3","Q7"]},
    "大众":   {"country": "德系", "tier": 3, "series": ["朗逸","速腾","迈腾","帕萨特","途观L","探岳","途岳","高尔夫","宝来","探歌"]},
    "保时捷": {"country": "德系", "tier": 1, "series": ["卡宴","Macan","Panamera","911"]},

    # 自主品牌
    "比亚迪": {"country": "自主", "tier": 3, "series": ["秦PLUS","汉","宋PLUS","唐","海豚","海豹","元PLUS","驱逐舰05"]},
    "吉利":   {"country": "自主", "tier": 4, "series": ["帝豪","博越","星瑞","星越L","缤越","豪越","领克03","领克01"]},
    "长安":   {"country": "自主", "tier": 4, "series": ["CS75 PLUS","逸动","UNI-V","UNI-K","CS55 PLUS","CS35 PLUS"]},
    "长城":   {"country": "自主", "tier": 4, "series": ["哈弗H6","哈弗大狗","坦克300","魏牌VV7","欧拉好猫"]},
    "奇瑞":   {"country": "自主", "tier": 4, "series": ["瑞虎8","瑞虎7","艾瑞泽8","艾瑞泽5","捷途X70"]},
    "蔚来":   {"country": "自主", "tier": 5, "series": ["ES6","ET5","ET7","ES8","EC6"]},
    "理想":   {"country": "自主", "tier": 3, "series": ["L7","L8","L9","ONE"]},
    "小鹏":   {"country": "自主", "tier": 5, "series": ["P7","P5","G6","G9"]},

    # 美系
    "别克":   {"country": "美系", "tier": 4, "series": ["英朗","君威","昂科威","GL8","威朗","昂科拉"]},
    "凯迪拉克":{"country": "美系", "tier": 4, "series": ["CT5","XT5","XT4","CT6","XT6"]},
    "福特":   {"country": "美系", "tier": 4, "series": ["蒙迪欧","锐界","福克斯","探险者","领裕"]},
    "雪佛兰": {"country": "美系", "tier": 5, "series": ["科鲁泽","迈锐宝XL","探界者","创酷"]},
    "特斯拉": {"country": "美系", "tier": 5, "series": ["Model 3","Model Y","Model S","Model X"]},

    # 韩系
    "现代":   {"country": "韩系", "tier": 4, "series": ["伊兰特","索纳塔","途胜","ix35","库斯途"]},
    "起亚":   {"country": "韩系", "tier": 5, "series": ["K3","K5","智跑","狮铂拓界","嘉华"]},

    # 欧系
    "沃尔沃": {"country": "欧系", "tier": 3, "series": ["XC60","S60","S90","XC40","XC90"]},
    "路虎":   {"country": "欧系", "tier": 4, "series": ["揽胜","揽胜极光","发现运动版","卫士"]},
}

VEHICLE_TYPES = {
    # Cars
    "卡罗拉":"轿车","凯美瑞":"轿车","亚洲龙":"轿车","雷凌":"轿车",
    "思域":"轿车","雅阁":"轿车","飞度":"轿车","凌派":"轿车",
    "ES":"轿车","LS":"轿车","UX":"SUV","NX":"SUV","RX":"SUV","LX":"SUV",
    "轩逸":"轿车","天籁":"轿车",
    "昂克赛拉":"轿车","阿特兹":"轿车",
    "C级":"轿车","E级":"轿车","S级":"轿车","A级":"轿车",
    "3系":"轿车","5系":"轿车","1系":"轿车","4系":"轿车",
    "A4L":"轿车","A6L":"轿车","A3":"轿车",
    "朗逸":"轿车","速腾":"轿车","迈腾":"轿车","帕萨特":"轿车","高尔夫":"轿车","宝来":"轿车",
    "Panamera":"轿车","911":"跑车",
    "秦PLUS":"轿车","汉":"轿车","海豚":"轿车","海豹":"轿车","驱逐舰05":"轿车",
    "帝豪":"轿车","星瑞":"轿车","领克03":"轿车",
    "逸动":"轿车","UNI-V":"轿车",
    "艾瑞泽8":"轿车","艾瑞泽5":"轿车",
    "ET5":"轿车","ET7":"轿车",
    "P7":"轿车","P5":"轿车",
    "君威":"轿车","威朗":"轿车","英朗":"轿车",
    "CT5":"轿车","CT6":"轿车",
    "蒙迪欧":"轿车","福克斯":"轿车",
    "科鲁泽":"轿车","迈锐宝XL":"轿车",
    "Model 3":"轿车","Model S":"轿车",
    "伊兰特":"轿车","索纳塔":"轿车",
    "K3":"轿车","K5":"轿车",
    "S60":"轿车","S90":"轿车",
    # SUVs
    "RAV4荣放":"SUV","汉兰达":"SUV","威兰达":"SUV","锋兰达":"SUV","普拉多":"SUV",
    "CR-V":"SUV","皓影":"SUV","XR-V":"SUV","冠道":"SUV",
    "逍客":"SUV","奇骏":"SUV","劲客":"SUV","途达":"SUV",
    "CX-5":"SUV","CX-4":"SUV","CX-30":"SUV",
    "森林人":"SUV","傲虎":"SUV","XV":"SUV",
    "GLC":"SUV","GLE":"SUV","GLA":"SUV",
    "X3":"SUV","X5":"SUV","X1":"SUV",
    "Q5L":"SUV","Q3":"SUV","Q7":"SUV",
    "途观L":"SUV","探岳":"SUV","途岳":"SUV","探歌":"SUV",
    "卡宴":"SUV","Macan":"SUV",
    "宋PLUS":"SUV","唐":"SUV","元PLUS":"SUV",
    "博越":"SUV","星越L":"SUV","缤越":"SUV","豪越":"SUV","领克01":"SUV",
    "CS75 PLUS":"SUV","UNI-K":"SUV","CS55 PLUS":"SUV","CS35 PLUS":"SUV",
    "哈弗H6":"SUV","哈弗大狗":"SUV","坦克300":"SUV","魏牌VV7":"SUV","欧拉好猫":"SUV",
    "瑞虎8":"SUV","瑞虎7":"SUV","捷途X70":"SUV",
    "ES6":"SUV","ES8":"SUV","EC6":"SUV",
    "L7":"SUV","L8":"SUV","L9":"SUV",
    "G6":"SUV","G9":"SUV",
    "昂科威":"SUV","昂科拉":"SUV",
    "XT5":"SUV","XT4":"SUV","XT6":"SUV",
    "锐界":"SUV","探险者":"SUV","领裕":"SUV",
    "探界者":"SUV","创酷":"SUV",
    "Model Y":"SUV","Model X":"SUV",
    "途胜":"SUV","ix35":"SUV",
    "智跑":"SUV","狮铂拓界":"SUV",
    "XC60":"SUV","XC40":"SUV","XC90":"SUV",
    "揽胜":"SUV","揽胜极光":"SUV","发现运动版":"SUV","卫士":"SUV",
    "赛那":"MPV","艾力绅":"MPV","奥德赛":"MPV","GL8":"MPV","库斯途":"MPV","嘉华":"MPV",
    "ONE":"SUV",
}

FUEL_TYPES = {
    "比亚迪": {"秦PLUS": "插混", "汉": "纯电", "宋PLUS": "插混", "唐": "插混", "海豚": "纯电", "海豹": "纯电", "元PLUS": "纯电", "驱逐舰05": "插混"},
    "蔚来": {"ES6": "纯电", "ET5": "纯电", "ET7": "纯电", "ES8": "纯电", "EC6": "纯电"},
    "理想": {"L7": "增程", "L8": "增程", "L9": "增程", "ONE": "增程"},
    "小鹏": {"P7": "纯电", "P5": "纯电", "G6": "纯电", "G9": "纯电"},
    "特斯拉": {"Model 3": "纯电", "Model Y": "纯电", "Model S": "纯电", "Model X": "纯电"},
}

TRANSMISSIONS = ["CVT", "AT", "DSG", "E-CVT", "MT"]
YEARS = list(range(2015, 2025))

# Tier to base retention (3yr)
TIER_BASE = {1: (68, 78), 2: (63, 72), 3: (58, 68), 4: (50, 62), 5: (40, 55)}
# Vehicle type modifier
TYPE_MOD = {"轿车": 0, "SUV": (2, 5), "MPV": (0, 3), "跑车": (-3, 0)}
# Fuel type modifier (deviation from base)
FUEL_MOD = {"汽油": (0, 0), "混动": (2, 6), "插混": (1, 4), "纯电": (-12, -3), "增程": (-3, 2)}
# Price modifier (luxury penalty)
PRICE_MOD = {(5, 15): (2, 5), (15, 25): (0, 2), (25, 40): (-3, 0), (40, 200): (-8, -3)}


def gen_model_name(series: str, year: int) -> str:
    displacements = {
        "卡罗拉": ["1.2T", "1.5L", "1.8L"], "凯美瑞": ["2.0L", "2.5L"],
        "雅阁": ["1.5T", "2.0L"], "CR-V": ["1.5T", "2.0L"],
        "RAV4荣放": ["2.0L", "2.5L"], "汉兰达": ["2.0T", "2.5L"],
        "思域": ["1.5T"], "轩逸": ["1.6L"], "天籁": ["2.0L", "2.0T"],
        "朗逸": ["1.5L", "1.4T"], "帕萨特": ["2.0T"], "迈腾": ["2.0T"],
        "3系": ["2.0T"], "5系": ["2.0T", "3.0T"],
        "C级": ["1.5T", "2.0T"], "E级": ["2.0T"],
        "A4L": ["2.0T"], "A6L": ["2.0T", "3.0T"],
        "哈弗H6": ["1.5T", "2.0T"], "CS75 PLUS": ["1.5T", "2.0T"],
        "博越": ["1.5T", "1.8T"], "瑞虎8": ["1.6T", "2.0T"],
        "Model 3": ["后驱标准续航", "长续航全驱"],
        "Model Y": ["后驱标准续航", "长续航全驱"],
        "ES6": ["75kWh", "100kWh"], "ET5": ["75kWh", "100kWh"],
        "L7": ["Pro", "Max"], "L8": ["Pro", "Max"], "L9": ["Ultra"],
        "P7": ["480km", "586km"], "G6": ["580km", "755km"],
    }
    disp_list = displacements.get(series, ["1.5T", "2.0L"])
    disp = random.choice(disp_list)
    variants = {
        "轿车": ["舒适版", "豪华版", "尊贵版", "旗舰版", "运动版"],
        "SUV": ["两驱舒适版", "两驱豪华版", "四驱尊贵版", "四驱旗舰版"],
        "MPV": ["舒适版", "豪华版", "尊贵版"],
        "跑车": ["标准版", "S版", "Turbo版"],
    }
    vtype = VEHICLE_TYPES.get(series, "轿车")
    variants_list = variants.get(vtype, ["标准版", "豪华版"])
    suffix = random.choice(variants_list)
    return f"{year}款 {disp} {suffix}"


def gen_price(series: str, tier: int) -> float:
    price_ranges = {
        "卡罗拉": (10, 15), "凯美瑞": (17, 27), "汉兰达": (24, 35), "普拉多": (44, 60),
        "思域": (11, 17), "雅阁": (17, 26), "CR-V": (17, 25),
        "ES": (29, 49), "RX": (40, 80), "LS": (87, 120),
        "轩逸": (9, 14), "天籁": (17, 24),
        "C级": (32, 38), "E级": (44, 56), "S级": (94, 180),
        "3系": (29, 40), "5系": (43, 56), "X5": (69, 86),
        "A4L": (30, 40), "A6L": (42, 65),
        "朗逸": (9, 15), "帕萨特": (18, 25), "途观L": (19, 28),
        "卡宴": (91, 200), "Macan": (57, 85),
        "秦PLUS": (9, 14), "汉": (21, 29), "宋PLUS": (14, 20),
        "哈弗H6": (9, 15), "坦克300": (19, 30),
        "博越": (9, 14), "星瑞": (11, 14),
        "CS75 PLUS": (10, 15),
        "Model 3": (23, 34), "Model Y": (26, 36),
        "ES6": (33, 47), "ET5": (29, 36),
        "L7": (30, 38), "L9": (42, 46),
        "P7": (22, 29), "G6": (20, 27),
        "GL8": (23, 47),
        "XC60": (37, 47), "XC90": (63, 78),
        "揽胜": (122, 200),
    }
    if series in price_ranges:
        lo, hi = price_ranges[series]
    else:
        lo, hi = 8 + tier * 3, 8 + (6 - tier) * 6
    return round(random.uniform(lo, hi), 2)


def gen_retention(tier: int, vehicle_type: str, fuel_type: str, guide_price: float) -> dict:
    base_min, base_max = TIER_BASE[tier]
    base_3yr = random.uniform(base_min, base_max)

    tmod = TYPE_MOD.get(vehicle_type, 0)
    if isinstance(tmod, tuple):
        base_3yr += random.uniform(*tmod)

    fmod = FUEL_MOD.get(fuel_type, (0, 0))
    if isinstance(fmod, tuple):
        base_3yr += random.uniform(*fmod)

    for (lo, hi), (pmin, pmax) in PRICE_MOD.items():
        if lo <= guide_price < hi:
            base_3yr += random.uniform(pmin, pmax)

    base_3yr = min(85, max(25, base_3yr))
    decay_1 = random.uniform(6, 10)
    decay_2 = random.uniform(5, 8)
    decay_3 = random.uniform(4, 7)
    decay_4 = random.uniform(3, 6)

    return {
        "retention_1yr": round(min(95, base_3yr + decay_1 + decay_2 + decay_3 + decay_4), 1),
        "retention_2yr": round(min(90, base_3yr + decay_2 + decay_3 + decay_4), 1),
        "retention_3yr": round(base_3yr, 1),
        "retention_4yr": round(max(20, base_3yr - decay_3), 1),
        "retention_5yr": round(max(15, base_3yr - decay_3 - decay_4), 1),
    }


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Brand).count() > 30:
        print("Database already has data, skipping.")
        db.close()
        return

    # Clear existing seed data
    db.query(RetentionRate).delete()
    db.query(CarModel).delete()
    db.query(BrandSeries).delete()
    db.query(Brand).delete()
    db.commit()

    total = 0
    for brand_name, bdata in BRANDS.items():
        brand = Brand(name=brand_name, country=bdata["country"])
        db.add(brand)
        db.flush()

        for series_name in bdata["series"]:
            vtype = VEHICLE_TYPES.get(series_name, "轿车")
            series = BrandSeries(brand_id=brand.id, name=series_name, vehicle_type=vtype)
            db.add(series)
            db.flush()

            for year in YEARS:
                # Skip years where the series didn't exist
                if series_name in ("L7", "L8", "L9", "海豹", "G6", "G9") and year < 2022:
                    continue
                if series_name in ("秦PLUS", "汉", "宋PLUS", "海豚", "驱逐舰05", "元PLUS") and year < 2020:
                    continue
                if series_name in ("ES6", "ET5", "ET7", "ES8", "EC6", "P7", "P5") and year < 2018:
                    continue
                if series_name in ("ONE",) and year < 2019:
                    continue
                if series_name in ("Model 3",) and year < 2019:
                    continue
                if series_name in ("Model Y",) and year < 2021:
                    continue

                # 1-3 variants per year
                for _ in range(random.randint(1, 3)):
                    model_name = gen_model_name(series_name, year)
                    fuel = FUEL_TYPES.get(brand_name, {}).get(series_name, random.choice(["汽油", "汽油", "汽油", "混动"]))
                    price = gen_price(series_name, bdata["tier"])
                    trans = "E-CVT" if fuel in ("混动", "插混", "增程") else "AT" if fuel == "纯电" else random.choice(TRANSMISSIONS)

                    model = CarModel(
                        series_id=series.id,
                        model_year=year,
                        specific_model=model_name,
                        guide_price=price,
                        displacement="N/A" if fuel in ("纯电", "增程") else f"{random.choice(['1.5','2.0','1.2','1.6','1.4','2.5','3.0'])}{random.choice(['T','L'])}",
                        fuel_type=fuel,
                        transmission=trans,
                    )
                    db.add(model)
                    db.flush()

                    rates = gen_retention(bdata["tier"], vtype, fuel, price)
                    retention = RetentionRate(
                        model_id=model.id,
                        source="seed_large",
                        scrape_date=date(2025, 6, 1),
                        retention_1yr=rates["retention_1yr"],
                        retention_2yr=rates["retention_2yr"],
                        retention_3yr=rates["retention_3yr"],
                        retention_4yr=rates["retention_4yr"],
                        retention_5yr=rates["retention_5yr"],
                        avg_listed_price=round(price * rates["retention_3yr"] / 100, 2),
                        sample_count=random.randint(30, 500),
                    )
                    db.add(retention)
                    total += 1

    db.commit()
    print(f"Seed complete: {db.query(Brand).count()} brands, {db.query(CarModel).count()} models, {total} retention records")
    db.close()


if __name__ == "__main__":
    seed()
