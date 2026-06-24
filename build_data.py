#!/usr/bin/env python3
"""
为「F1 队友排位中位差」网页生成本地数据。

用法:
    python build_data.py 2024            # 生成 data/quali-2024.json
    python build_data.py 2021 2022 2023 2024   # 一次生成多个赛季

生成的 JSON 会被 f1-teammate-quali-gap.html 自动优先读取(本地优先,
读不到再走实时 API)。本地数据 = 离线可用、不受地区/跨域限制、秒开。

数据源:免费的 Jolpica-F1 API(Ergast 后继,无需密钥)。
        https://github.com/jolpica/jolpica-f1

—— 关于 FastF1 ——
FastF1 是一个 Python 库(不是浏览器能直接调用的 HTTP API),适合在这一步用来
取更丰富的数据(遥测、轮胎、练习赛圈速)。如果你想用 FastF1 代替下面的 Jolpica
取数,可参考 build_with_fastf1() 里的示例(需要先 `pip install fastf1`)。
"""
import json
import os
import sys
import time
import urllib.request

API = "https://api.jolpi.ca/ergast/f1"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "f1-quali-gap/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def build_season(year):
    """从 Jolpica 拉取整季排位结果,整理成网页需要的结构。"""
    by_round = {}
    offset, total = 0, 1
    while offset < total:
        url = f"{API}/{year}/qualifying/?limit=100&offset={offset}&format=json"
        md = fetch_json(url)["MRData"]
        total = int(md["total"])
        races = md["RaceTable"]["Races"]
        for race in races:
            rd = race["round"]
            bucket = by_round.setdefault(
                rd, {"round": rd, "raceName": race["raceName"], "results": []}
            )
            for q in race.get("QualifyingResults", []):
                d, c = q["Driver"], q["Constructor"]
                bucket["results"].append({
                    "driverId": d["driverId"],
                    "code": d.get("code") or d["familyName"][:3].upper(),
                    "name": d["familyName"],
                    "constructorId": c["constructorId"],
                    "constructorName": c["name"],
                    "Q1": q.get("Q1", ""),
                    "Q2": q.get("Q2", ""),
                    "Q3": q.get("Q3", ""),
                })
        offset += 100
        if not races:
            break
        time.sleep(0.3)  # 对公共 API 友好一点
    rounds = sorted(by_round.values(), key=lambda r: int(r["round"]))
    return {"year": int(year), "rounds": rounds}


def build_with_fastf1(year):
    """
    可选:用 FastF1 取数(更丰富,但更慢,首次会下载并缓存)。
    需要 `pip install fastf1`。这里给出取「每位车手每个排位阶段最快圈」的思路,
    输出结构与 build_season 一致,可直接替换使用。
    """
    import fastf1  # noqa: 延迟导入,未安装也不影响 Jolpica 路径

    fastf1.Cache.enable_cache(os.path.join(os.path.dirname(__file__), ".fastf1cache"))
    schedule = fastf1.get_event_schedule(year, include_testing=False)
    rounds = []
    for _, ev in schedule.iterrows():
        rnd = int(ev["RoundNumber"])
        if rnd < 1:
            continue
        try:
            q = fastf1.get_session(year, rnd, "Q")
            q.load(telemetry=False, weather=False, messages=False)
        except Exception as e:  # 该站可能尚未举行
            print(f"  跳过 R{rnd}: {e}")
            continue
        results = []
        for _, r in q.results.iterrows():
            def fmt(td):
                if td is None or (hasattr(td, "isnull") and td.isnull()):
                    return ""
                s = td.total_seconds()
                return f"{int(s // 60)}:{s % 60:06.3f}" if s else ""
            results.append({
                "driverId": str(r.get("DriverId", r.get("Abbreviation", ""))).lower(),
                "code": r.get("Abbreviation", ""),
                "name": r.get("LastName", ""),
                "constructorId": str(r.get("TeamId", r.get("TeamName", ""))).lower().replace(" ", "_"),
                "constructorName": r.get("TeamName", ""),
                "Q1": fmt(r.get("Q1")), "Q2": fmt(r.get("Q2")), "Q3": fmt(r.get("Q3")),
            })
        rounds.append({"round": str(rnd), "raceName": ev["EventName"], "results": results})
    return {"year": int(year), "rounds": rounds}


def main():
    years = sys.argv[1:] or ["2024"]
    os.makedirs(OUT_DIR, exist_ok=True)
    for y in years:
        print(f"拉取 {y} 赛季…")
        data = build_season(y)               # 想用 FastF1 就换成 build_with_fastf1(y)
        path = os.path.join(OUT_DIR, f"quali-{y}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        print(f"  已写入 {path}  (共 {len(data['rounds'])} 站)")
    print("完成。刷新 f1-teammate-quali-gap.html 即可读取本地数据。")


if __name__ == "__main__":
    main()
