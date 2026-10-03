"""Category-level comparison with the reference project's 144-cell summary."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rules.jinjing.geju import GejuContext, analyze_geju


FIXTURE = ROOT / "tests" / "fixtures" / "skyeyes_summary_144.json"
REPORT = ROOT / "tests" / "reports" / "skyeyes_summary_audit.md"
CATEGORIES = ("掩", "擊", "迫", "囚", "關", "格", "對", "提挾")
CLASSIFICATIONS = (
    "一致", "部分對應／新舊規則兼有", "舊表有標籤／金鏡未判",
    "金鏡新增／舊表未列", "兩表皆無所審類別",
)


def old_categories(summary: str) -> set[str]:
    summary = summary or ""
    checks = {
        "掩": ("掩",),
        "擊": ("擊", "击"),
        "迫": ("迫",),
        "囚": ("囚",),
        "關": ("關", "关"),
        "格": ("格",),
        "對": ("對", "对"),
        "提挾": ("挾", "挟"),
    }
    return {category for category, variants in checks.items() if any(token in summary for token in variants)}


def build_rows() -> list[dict]:
    artifact = json.loads(FIXTURE.read_text(encoding="utf-8"))
    rows = []
    for row in artifact["rows"]:
        context = GejuContext(
            taiyi=row["太乙"],
            wenchang=row["文昌"],
            shiji=row["始擊"],
            home_big=row["主大"],
            home_vassal=row["主參"],
            away_big=row["客大"],
            away_vassal=row["客參"],
        )
        detail = analyze_geju(context)
        current = {event["格局"] for event in detail["事件"]} & set(CATEGORIES)
        previous = old_categories(row["舊表摘要"])
        if previous == current:
            label = "一致"
        elif previous & current:
            label = "部分對應／新舊規則兼有"
        elif previous:
            label = "舊表有標籤／金鏡未判"
        elif current:
            label = "金鏡新增／舊表未列"
        else:
            label = "兩表皆無所審類別"
        rows.append({**row, "舊類": previous, "金鏡類": current, "分類": label})
    return rows


def render_report(rows: list[dict]) -> str:
    counts = Counter(row["分類"] for row in rows)
    artifact = json.loads(FIXTURE.read_text(encoding="utf-8"))
    lines = [
        "# `skyeyes_summary` 144 局差異審計",
        "",
        f"> 對照來源：`kentang2017/kintaiyi` 固定提交 `{artifact['reference_commit']}`。",
        "> 本報告比较旧摘要类别与《金镜》动态格局类别，不要求事件字典机械全等。旧摘要没有值事门输入，故不审计执提／提格；复合格局另由单项规则测试覆盖。",
        "> 测试使用随仓库保存的144行位置快照，规则模块不运行或导入参考仓库代码。",
        "",
        "## 分类计数",
        "",
        "| 分类 | 局数 |",
        "|---|---:|",
    ]
    lines.extend(f"| {name} | {counts[name]} |" for name in CLASSIFICATIONS)
    lines.extend([
        "",
        "## 逐局对照",
        "",
        "| 遁 | 局 | 太乙宫 | 旧表摘要 | 旧类别 | 金镜类别 | 分类 |",
        "|---|---:|---:|---|---|---|---|",
    ])
    for row in rows:
        previous = "、".join(c for c in CATEGORIES if c in row["舊類"]) or "—"
        current = "、".join(c for c in CATEGORIES if c in row["金鏡類"]) or "—"
        lines.append(
            f"| {row['遁']} | {row['局']} | {row['太乙']} | {row['舊表摘要'] or '—'} | "
            f"{previous} | {current} | {row['分類']} |"
        )
    lines.extend([
        "",
        "## 差异判读",
        "",
        "- 旧表有而新算法未判的项目，先复核家法、摘要术语及十六神精确位置；不能据此自动修改《金镜》主规则。",
        "- 新算法新增的项目，表示旧摘要未列出同类标签；需回看历史局例原文。",
        "- 219年第36局的“客关主目”保留为《太乙淘金歌》对照语；主算法按《金镜》只以四将同宫判关。",
        "- “四郭社”只作为异文文本，不作为主输出字段。",
        "",
    ])
    return "\n".join(lines)


def test_audit_covers_all_144_cells_and_reports_every_difference_class():
    rows = build_rows()
    assert len(rows) == 144
    assert Counter(row["遁"] for row in rows) == {"陽": 72, "陰": 72}
    assert set(row["分類"] for row in rows) <= set(CLASSIFICATIONS)
    assert "# `skyeyes_summary` 144 局差異審計" in render_report(rows)


if __name__ == "__main__":
    report_rows = build_rows()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render_report(report_rows), encoding="utf-8")
    print(f"wrote {REPORT} ({len(report_rows)} rows)")

