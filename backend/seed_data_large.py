"""Fast bulk seed: 28 brands, ~800 models. Uses bulk inserts for speed."""

import random
from datetime import date

from app.database import SessionLocal, engine, Base
from app.models import Brand, BrandSeries, CarModel, RetentionRate

# Brand definitions with retention influence factors
BRAND_DEFS = [
    # (name, country, series_list, retention_base) -- higher base = better retention
    ("丰田", "日系", ["卡罗拉","凯美瑞","RAV4荣放","汉兰达","亚洲龙","威兰达","雷凌","普拉多","赛那"], 72),
    ("本田", "日系", ["思域","雅阁","CR-V","皓影","XR-V","飞度","冠道"], 70),
    ("雷克萨斯","日系",["ES","RX","NX","UX","LX"],73),
    ("日产","日系",["轩逸","天籁","逍客","奇骏"],64),
    ("马自达","日系",["昂克赛拉","阿特兹","CX-5","CX-4"],60),
    ("奔驰","德系",["C级","E级","S级","GLC","GLE","GLA"],65),
    ("宝马","德系",["3系","5系","X3","X5","X1"],63),
    ("奥迪","德系",["A4L","A6L","Q5L","Q3","A3"],58),
    ("大众","德系",["朗逸","速腾","迈腾","帕萨特","途观L","探岳","高尔夫"],56),
    ("保时捷","德系",["卡宴","Macan","Panamera"],68),
    ("比亚迪","自主",["秦PLUS","汉","宋PLUS","唐","海豚","海豹","元PLUS"],58),
    ("吉利","自主",["帝豪","博越","星瑞","星越L","缤越","领克03"],50),
    ("长安","自主",["CS75 PLUS","逸动","UNI-V","UNI-K","CS55 PLUS"],48),
    ("长城","自主",["哈弗H6","哈弗大狗","坦克300","欧拉好猫"],52),
    ("奇瑞","自主",["瑞虎8","瑞虎7","艾瑞泽8","捷途X70"],46),
    ("蔚来","自主",["ES6","ET5","ET7","ES8"],42),
    ("理想","自主",["L7","L8","L9","ONE"],55),
    ("小鹏","自主",["P7","P5","G6","G9"],38),
    ("别克","美系",["英朗","君威","昂科威","GL8"],50),
    ("凯迪拉克","美系",["CT5","XT5","XT4","CT6"],45),
    ("福特","美系",["蒙迪欧","锐界","福克斯","探险者"],48),
    ("雪佛兰","美系",["科鲁泽","迈锐宝XL","探界者"],42),
    ("特斯拉","美系",["Model 3","Model Y"],40),
    ("现代","韩系",["伊兰特","索纳塔","途胜","ix35"],46),
    ("起亚","韩系",["K3","K5","智跑","狮铂拓界"],42),
    ("沃尔沃","欧系",["XC60","S60","S90","XC90"],56),
    ("路虎","欧系",["揽胜","揽胜极光","发现运动版","卫士"],48),
]

VEHICLE_TYPE_MAP = {
    "卡罗拉":"轿车","凯美瑞":"轿车","亚洲龙":"轿车","雷凌":"轿车","赛那":"MPV",
    "思域":"轿车","雅阁":"轿车","飞度":"轿车","冠道":"SUV",
    "ES":"轿车","RX":"SUV","NX":"SUV","UX":"SUV","LX":"SUV",
    "轩逸":"轿车","天籁":"轿车",
    "昂克赛拉":"轿车","阿特兹":"轿车",
    "C级":"轿车","E级":"轿车","S级":"轿车",
    "3系":"轿车","5系":"轿车",
    "A4L":"轿车","A6L":"轿车",
    "朗逸":"轿车","速腾":"轿车","迈腾":"轿车","帕萨特":"轿车","高尔夫":"轿车",
    "Panamera":"轿车",
    "秦PLUS":"轿车","汉":"轿车","海豚":"轿车","海豹":"轿车",
    "帝豪":"轿车","星瑞":"轿车","领克03":"轿车",
    "逸动":"轿车","UNI-V":"轿车",
    "艾瑞泽8":"轿车",
    "ET5":"轿车","ET7":"轿车",
    "P7":"轿车","P5":"轿车",
    "英朗":"轿车","君威":"轿车",
    "CT5":"轿车","CT6":"轿车",
    "蒙迪欧":"轿车","福克斯":"轿车",
    "科鲁泽":"轿车","迈锐宝XL":"轿车",
    "Model 3":"轿车",
    "伊兰特":"轿车","索纳塔":"轿车",
    "K3":"轿车","K5":"轿车",
    "S60":"轿车","S90":"轿车",
    "GL8":"MPV",
}

ELECTRIC_SERIES = {
    "秦PLUS":"插混","汉":"纯电","宋PLUS":"插混","唐":"插混",
    "海豚":"纯电","海豹":"纯电","元PLUS":"纯电",
    "L7":"增程","L8":"增程","L9":"增程","ONE":"增程",
    "ES6":"纯电","ET5":"纯电","ET7":"纯电","ES8":"纯电",
    "P7":"纯电","P5":"纯电","G6":"纯电","G9":"纯电",
    "Model 3":"纯电","Model Y":"纯电",
    "欧拉好猫":"纯电",
}

PRICE_MAP = {
    "卡罗拉":(10,15),"凯美瑞":(17,27),"汉兰达":(24,35),"普拉多":(44,60),"赛那":(30,40),
    "亚洲龙":(19,27),"威兰达":(17,26),"雷凌":(10,14),
    "思域":(11,17),"雅阁":(17,26),"CR-V":(17,25),"皓影":(16,24),"XR-V":(12,16),"飞度":(7,10),"冠道":(22,33),
    "ES":(29,49),"RX":(40,80),"NX":(30,50),"UX":(25,35),"LX":(87,150),
    "轩逸":(9,14),"天籁":(17,24),"逍客":(13,19),"奇骏":(17,26),
    "昂克赛拉":(10,15),"阿特兹":(17,22),"CX-5":(16,23),"CX-4":(13,19),
    "C级":(32,38),"E级":(44,56),"S级":(94,180),"GLC":(40,50),"GLE":(69,88),"GLA":(27,33),
    "3系":(29,40),"5系":(43,56),"X3":(38,48),"X5":(69,86),"X1":(27,34),
    "A4L":(30,40),"A6L":(42,65),"Q5L":(37,48),"Q3":(27,35),"A3":(19,25),
    "朗逸":(9,15),"速腾":(12,16),"迈腾":(18,25),"帕萨特":(18,25),"途观L":(19,28),"探岳":(18,26),"高尔夫":(12,16),
    "卡宴":(91,200),"Macan":(57,85),"Panamera":(97,200),
    "秦PLUS":(9,14),"汉":(21,29),"宋PLUS":(14,20),"唐":(20,30),"海豚":(9,13),"海豹":(18,26),"元PLUS":(12,16),
    "帝豪":(6,9),"博越":(9,14),"星瑞":(11,14),"星越L":(13,18),"缤越":(7,11),"领克03":(13,20),
    "CS75 PLUS":(10,15),"逸动":(7,10),"UNI-V":(10,14),"UNI-K":(14,18),"CS55 PLUS":(8,12),
    "哈弗H6":(9,15),"哈弗大狗":(11,17),"坦克300":(19,30),"欧拉好猫":(10,15),
    "瑞虎8":(9,15),"瑞虎7":(7,11),"艾瑞泽8":(10,13),"捷途X70":(7,11),
    "ES6":(33,47),"ET5":(29,36),"ET7":(42,50),"ES8":(45,58),
    "L7":(30,38),"L8":(34,40),"L9":(42,46),"ONE":(32,35),
    "P7":(22,29),"P5":(15,19),"G6":(20,27),"G9":(28,35),
    "英朗":(8,12),"君威":(17,22),"昂科威":(18,26),"GL8":(23,47),
    "CT5":(27,35),"XT5":(33,42),"XT4":(25,32),"CT6":(35,48),
    "蒙迪欧":(15,22),"锐界":(22,31),"福克斯":(10,15),"探险者":(30,40),
    "科鲁泽":(7,10),"迈锐宝XL":(15,20),"探界者":(16,23),
    "Model 3":(23,34),"Model Y":(26,36),
    "伊兰特":(9,13),"索纳塔":(16,21),"途胜":(16,22),"ix35":(12,17),
    "K3":(9,12),"K5":(15,20),"智跑":(13,18),"狮铂拓界":(17,23),
    "XC60":(37,47),"S60":(29,38),"S90":(40,50),"XC90":(63,78),
    "揽胜":(122,200),"揽胜极光":(35,45),"发现运动版":(38,50),"卫士":(68,85),
}


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if db.query(Brand).count() > 10:
        print("Already seeded, skip.")
        db.close()
        return

    db.query(RetentionRate).delete()
    db.query(CarModel).delete()
    db.query(BrandSeries).delete()
    db.query(Brand).delete()
    db.commit()

    brands_to_add = []
    for name, country, series_list, base in BRAND_DEFS:
        brands_to_add.append(Brand(name=name, country=country))
    db.add_all(brands_to_add)
    db.flush()

    brand_map = {b.name: b.id for b in db.query(Brand).all()}

    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]

    models_batch = []
    rates_batch = []
    count = 0

    for name, country, series_list, base in BRAND_DEFS:
        bid = brand_map[name]
        for sname in series_list:
            vtype = VEHICLE_TYPE_MAP.get(sname, "SUV")
            series = BrandSeries(brand_id=bid, name=sname, vehicle_type=vtype)
            db.add(series)
            db.flush()
            sid = series.id

            for year in years:
                # Skip years where model didn't exist yet
                if sname in ELECTRIC_SERIES and year < 2020:
                    continue
                if sname in ("Model 3",) and year < 2020:
                    continue
                if sname in ("Model Y",) and year < 2021:
                    continue
                if sname in ("L7","L8","L9","海豹","G6","G9") and year < 2022:
                    continue

                fuel = ELECTRIC_SERIES.get(sname, random.choice(["汽油","汽油","汽油","混动"]))
                prange = PRICE_MAP.get(sname, (8 + base//15, 8 + (85 - base)//8))
                price = round(random.uniform(*prange), 2)

                # Retention calculation
                r3 = base + random.uniform(-5, 8)
                if fuel == "混动" or fuel == "增程":
                    r3 += random.uniform(2, 6)
                elif fuel == "纯电":
                    r3 -= random.uniform(5, 15)
                elif fuel == "插混":
                    r3 += random.uniform(0, 4)
                if vtype == "SUV":
                    r3 += random.uniform(1, 4)
                if price > 40:
                    r3 -= random.uniform(2, 7)
                r3 = min(82, max(25, r3))

                d1, d2, d3, d4 = [random.uniform(3, 7) for _ in range(4)]
                r1 = round(min(93, r3 + d1 + d2 + d3 + d4), 1)
                r2 = round(min(88, r3 + d2 + d3 + d4), 1)
                r3v = round(r3, 1)
                r4 = round(max(18, r3 - d3), 1)
                r5 = round(max(12, r3 - d3 - d4), 1)
                disp = "N/A" if fuel in ("纯电","增程") else f"{random.choice(['1.5','2.0','1.6','2.5'])}{random.choice(['T','L'])}"

                model = CarModel(
                    series_id=sid,
                    model_year=year,
                    specific_model=f"{year}款 {random.choice(['标准版','豪华版','尊贵版'])}",
                    guide_price=price,
                    displacement=disp,
                    fuel_type=fuel,
                    transmission="CVT" if fuel in ("混动","插混") else "AT",
                )
                db.add(model)
                db.flush()

                rate = RetentionRate(
                    model_id=model.id,
                    source="seed",
                    scrape_date=date(2025, 6, 1),
                    retention_1yr=r1, retention_2yr=r2, retention_3yr=r3v,
                    retention_4yr=r4, retention_5yr=r5,
                    avg_listed_price=round(price * r3v / 100, 2),
                    sample_count=random.randint(30, 400),
                )
                db.add(rate)
                count += 1

                if count % 300 == 0:
                    db.commit()
                    print(f"  ... {count} records")

    db.commit()
    total_models = db.query(CarModel).count()
    total_rates = db.query(RetentionRate).count()
    print(f"Seed done: {db.query(Brand).count()} brands, {total_models} models, {total_rates} rates")
    db.close()


if __name__ == "__main__":
    seed()
