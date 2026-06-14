"""Github_rank_agent 入口（CLI）。

子指令：
    fetch                抓本週排行寫入 research_github（預設）
    digest [--week W]    印某週排行（含個人評價/研究狀態）供 agent 編排好料總結
    interested <repo...> 標記想進一步研究
    rate <repo> <1-10> [--notes ...]   設定個人評價
    researched <repo>    標記已研究完畢
    to-research          列出 status=interested 的 repo（供「深度研究」指令）

repo 一律用 owner/name。
"""
from __future__ import annotations

import argparse
import sys

from github_rank_agent import storage
from github_rank_agent.sources import ENABLED_SOURCES

# Windows 終端預設非 UTF-8，避免中文輸出亂碼
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def cmd_fetch() -> None:
    """抓各來源本週排行並 UPSERT。"""
    storage.init_db()
    total = 0
    for source in ENABLED_SOURCES:
        try:
            records = source.fetch()
        except Exception as exc:  # 單一來源失敗不影響其他來源
            print(f"[skip] {source.name}: 抓取失敗 - {exc}")
            continue
        n = storage.upsert_records(records)
        total += n
        print(f"[ok]   {source.name}: 抓到 {n} 筆")
    print(f"完成：共寫入/更新 {total} 筆 -> {storage.config.DB_PATH}")


def cmd_digest(week: str | None) -> None:
    """印某週排行（最新週為預設），帶出個人評價與研究狀態。"""
    storage.init_db()
    rows = storage.load_week_digest(week)
    if not rows:
        print("（沒有資料；先執行 `python main.py fetch`）")
        return
    print(f"== 週別 {rows[0]['week']}　共 {len(rows)} 筆 ==")
    for r in rows:
        tags = []
        if r["research_status"] == "done":
            tags.append("✅已研究")
        elif r["research_status"] == "interested":
            tags.append("⭐想研究")
        elif r["research_status"] == "researching":
            tags.append("🔬研究中")
        if r["personal_rating"] is not None:
            tags.append(f"評{r['personal_rating']}")
        tag_str = f"  [{' '.join(tags)}]" if tags else ""
        stars = r["total_stars"]
        growth = r["weekly_growth"]
        desc = (r["description"] or "").strip()
        print(f"#{r['rank']:>2} {r['repo_full_name']}  ⭐{stars}  🔺{growth}{tag_str}")
        print(f"     {r['repo_url']}")
        if desc:
            print(f"     {desc}")


def cmd_interested(repos: list[str]) -> None:
    storage.init_db()
    for repo in repos:
        storage.mark_interested(repo)
        print(f"⭐ 已標記想研究：{repo}")


def cmd_rate(repo: str, rating: int, notes: str | None) -> None:
    storage.init_db()
    storage.set_evaluation(repo, rating=rating, notes=notes)
    print(f"已評價 {repo}：{rating}/10" + (f"（{notes}）" if notes else ""))


def cmd_researched(repo: str) -> None:
    storage.init_db()
    storage.mark_researched(repo)
    print(f"✅ 已標記研究完畢：{repo}")


def cmd_set_desc(repo: str, text: str, week: str | None) -> None:
    storage.init_db()
    n = storage.set_description(repo, text, week=week)
    if n:
        print(f"已更新描述：{repo}")
    else:
        print(f"找不到對應列（repo={repo} week={week or '最新'}）")


def cmd_to_research() -> None:
    storage.init_db()
    rows = storage.get_research(status="interested")
    if not rows:
        print("（目前沒有想研究的 repo）")
        return
    print(f"待深度研究（{len(rows)}）：")
    for r in rows:
        print(f"  - {r['repo_full_name']}（標記於 {r['interested_at']}）")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Github_rank_agent CLI")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("fetch", help="抓本週排行寫入 DB")

    d = sub.add_parser("digest", help="印某週排行供編排好料總結")
    d.add_argument("--week", default=None, help="週別 YYYY-Www，預設最新週")

    i = sub.add_parser("interested", help="標記想進一步研究")
    i.add_argument("repos", nargs="+", help="owner/name（可多個）")

    rt = sub.add_parser("rate", help="設定個人評價")
    rt.add_argument("repo")
    rt.add_argument("rating", type=int, help="1~10")
    rt.add_argument("--notes", default=None)

    rs = sub.add_parser("researched", help="標記已研究完畢")
    rs.add_argument("repo")

    sd = sub.add_parser("set-desc", help="覆寫某 repo 的乾淨英文描述")
    sd.add_argument("repo")
    sd.add_argument("text")
    sd.add_argument("--week", default=None, help="週別 YYYY-Www，預設最新週")

    sub.add_parser("to-research", help="列出 status=interested 的 repo")
    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    cmd = args.cmd or "fetch"  # 無子指令時預設 fetch
    if cmd == "fetch":
        cmd_fetch()
    elif cmd == "digest":
        cmd_digest(args.week)
    elif cmd == "interested":
        cmd_interested(args.repos)
    elif cmd == "rate":
        cmd_rate(args.repo, args.rating, args.notes)
    elif cmd == "researched":
        cmd_researched(args.repo)
    elif cmd == "set-desc":
        cmd_set_desc(args.repo, args.text, args.week)
    elif cmd == "to-research":
        cmd_to_research()


if __name__ == "__main__":
    main()
