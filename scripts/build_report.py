#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
管理体系内部审核报告生成器
读入结构化结果 JSON，生成 MD 文档 + 精美网页版 HTML（主色 #C8102E）。

用法：
  python build_report.py --input result.json --md-out report.md --html-out report.html
  python build_report.py                      # 使用内置演示数据，输出到 ./output/

输入 JSON 结构：
{
  "meta": {"standard":"ISO9001/IATF16949","audit_type":"体系审核","scope":"...","period":"2026年度","planned_date":"2026-03-10"},
  "plan": [{"month":"3月","type":"体系审核","scope":"QMS 4-10章","auditor":"张三"}],
  "checklist": [{"clause":"4.4","requirement":"确定所需过程","check_point":"是否识别过程接口","evidence":"过程清单"}],
  "nonconformities": [{"id":"NC-01","clause":"8.5.1","severity":"一般","requirement":"...","evidence":"...","gap":"..."}],
  "corrective_actions": [{"nc_id":"NC-01","action":"...","owner":"李四","due":"2026-04-10","status":"整改中"}]
}
"""
import argparse
import json
import os
import sys
import html
from datetime import datetime

MAIN = "#C8102E"  # 主色


def esc(s):
    return html.escape(str(s), quote=True)


def load_result(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ----------------------------- 内置演示数据 -----------------------------
DEMO = {
    "meta": {
        "standard": "ISO9001:2015 / IATF16949:2016",
        "audit_type": "体系审核（年度）",
        "scope": "QMS 全部条款（4-10章）及制造过程",
        "period": "2026年度（演示数据，待企业补充）",
        "planned_date": "2026-03-10"
    },
    "plan": [
        {"month": "3月", "type": "体系审核", "scope": "QMS 4-10章", "auditor": "张三（待测）"},
        {"month": "6月", "type": "制造过程审核", "scope": "焊接/装配过程", "auditor": "李四（待测）"},
        {"month": "9月", "type": "产品审核", "scope": "A类件总成", "auditor": "王五（待测）"},
        {"month": "11月", "type": "体系审核（跟踪）", "scope": "不符合项闭环验证", "auditor": "张三（待测）"}
    ],
    "checklist": [
        {"clause": "4.4", "requirement": "确定QMS所需过程及接口", "check_point": "是否建立过程清单并明确职责接口", "evidence": "过程识别清单"},
        {"clause": "8.5.1", "requirement": "生产和服务提供的控制", "check_point": "作业指导书是否现行有效并受控", "evidence": "SOP发放记录"},
        {"clause": "9.2", "requirement": "内部审核", "check_point": "内审方案是否覆盖体系/过程/产品", "evidence": "年度审核方案"},
        {"clause": "10.2", "requirement": "不合格和纠正措施", "check_point": "纠正措施是否含根因分析与横向展开", "evidence": "8D/纠正措施报告"}
    ],
    "nonconformities": [
        {"id": "NC-01", "clause": "8.5.1", "severity": "一般",
         "requirement": "受控条件下生产，使用现行有效文件",
         "evidence": "装配工位SOP版本为2024版，最新为2026版未换发",
         "gap": "现场使用文件与受控版本不一致"},
        {"id": "NC-02", "clause": "9.2.2", "severity": "观察项",
         "requirement": "内审员应保持客观公正",
         "evidence": "内审员能力矩阵未记录培训与资格确认",
         "gap": "内审员资格证据不完整"}
    ],
    "corrective_actions": [
        {"nc_id": "NC-01", "action": "回收旧版SOP，换发2026版并培训签字", "owner": "生产部", "due": "2026-03-20", "status": "整改中"},
        {"nc_id": "NC-02", "action": "补全内审员培训记录与资格确认表", "owner": "体系部", "due": "2026-03-25", "status": "待整改"}
    ]
}


# ----------------------------- MD 生成 -----------------------------
def build_md(r):
    L = []
    m = r.get("meta", {})
    L.append("# 管理体系内部审核报告\n")
    L.append("## 一、审核概况\n")
    L.append(f"- 审核标准：{m.get('standard','')}")
    L.append(f"- 审核类型：{m.get('audit_type','')}")
    L.append(f"- 审核范围：{m.get('scope','')}")
    L.append(f"- 审核周期：{m.get('period','')}")
    L.append(f"- 计划日期：{m.get('planned_date','')}")
    L.append("")
    L.append("## 二、年度审核方案\n")
    L.append("| 月份 | 审核类型 | 覆盖范围 | 审核员 |")
    L.append("|------|----------|----------|--------|")
    for p in r.get("plan", []) or []:
        L.append(f"| {p.get('month','')} | {p.get('type','')} | {p.get('scope','')} | {p.get('auditor','')} |")
    L.append("")
    L.append("## 三、审核检查表要点\n")
    L.append("| 条款 | 标准要求 | 检查要点 | 证据期望 |")
    L.append("|------|----------|----------|----------|")
    for c in r.get("checklist", []) or []:
        L.append(f"| {c.get('clause','')} | {c.get('requirement','')} | {c.get('check_point','')} | {c.get('evidence','')} |")
    L.append("")
    L.append("## 四、不符合项清单\n")
    L.append("| 编号 | 条款 | 级别 | 标准要求 | 客观证据 | 差距 |")
    L.append("|------|------|------|----------|----------|------|")
    for n in r.get("nonconformities", []) or []:
        L.append(f"| {n.get('id','')} | {n.get('clause','')} | {n.get('severity','')} | {n.get('requirement','')} | {n.get('evidence','')} | {n.get('gap','')} |")
    L.append("")
    L.append("## 五、整改追踪台账\n")
    L.append("| 关联不符合项 | 纠正措施 | 责任部门 | 计划完成 | 状态 |")
    L.append("|--------------|----------|----------|----------|------|")
    for a in r.get("corrective_actions", []) or []:
        L.append(f"| {a.get('nc_id','')} | {a.get('action','')} | {a.get('owner','')} | {a.get('due','')} | {a.get('status','')} |")
    L.append("")
    L.append("## 六、审核结论\n")
    L.append("- 本次审核共发现不符合项 " + str(len(r.get("nonconformities", []) or [])) +
             " 项，其中严重 0 / 一般 " +
             str(sum(1 for n in r.get('nonconformities', []) if n.get('severity') == '一般')) +
             " / 观察 " +
             str(sum(1 for n in r.get('nonconformities', []) if n.get('severity') == '观察项')) + "。")
    L.append("- 整改闭环率、过程有效性评价详见管理评审输入（由企业判定）。〔结论由企业审核组签署〕")
    L.append("")
    L.append(f"> 报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} ｜ 主色 {MAIN}")
    return "\n".join(L)


# ----------------------------- HTML 生成 -----------------------------
CSS = """
:root{ --main:%s; --bg:#f7f8fa; --card:#fff; --ink:#1f2937; --muted:#6b7280; --line:#e5e7eb; }
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.7;padding:32px}
.wrap{max-width:1100px;margin:0 auto}
header{text-align:center;padding:30px 0 20px;border-bottom:3px solid var(--main);margin-bottom:28px}
header h1{font-size:27px;letter-spacing:1px}
header .meta{color:var(--muted);font-size:14px;margin-top:10px}
.sec{background:var(--card);border-radius:14px;padding:24px;box-shadow:0 4px 16px rgba(0,0,0,.06);margin-bottom:26px}
.sec h2{font-size:21px;margin-bottom:16px;border-left:5px solid var(--main);padding-left:12px}
table{width:100%%;border-collapse:collapse;font-size:14px}
th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}
th{background:#fef2f4;color:var(--main);font-weight:700}
tr:nth-child(even){background:#fafafa}
.sev-major{color:#b91c1c;font-weight:700}
.sev-minor{color:#d97706;font-weight:700}
.sev-ob{color:#2563eb;font-weight:700}
.conclusion{background:#fef2f4;border-left:5px solid var(--main);padding:16px 18px;border-radius:8px;font-size:15px}
footer{text-align:center;color:var(--muted);font-size:12px;margin-top:20px}
""" % MAIN


def build_html(r):
    m = r.get("meta", {})

    def sev_cls(s):
        if s == "严重":
            return "sev-major"
        if s == "一般":
            return "sev-minor"
        return "sev-ob"

    plan_rows = "".join(
        f"<tr><td>{esc(p.get('month',''))}</td><td>{esc(p.get('type',''))}</td>"
        f"<td>{esc(p.get('scope',''))}</td><td>{esc(p.get('auditor',''))}</td></tr>"
        for p in r.get("plan", []) or [])
    chk_rows = "".join(
        f"<tr><td>{esc(c.get('clause',''))}</td><td>{esc(c.get('requirement',''))}</td>"
        f"<td>{esc(c.get('check_point',''))}</td><td>{esc(c.get('evidence',''))}</td></tr>"
        for c in r.get("checklist", []) or [])
    nc_rows = "".join(
        f"<tr><td>{esc(n.get('id',''))}</td><td>{esc(n.get('clause',''))}</td>"
        f"<td class='{sev_cls(n.get('severity',''))}'>{esc(n.get('severity',''))}</td>"
        f"<td>{esc(n.get('requirement',''))}</td><td>{esc(n.get('evidence',''))}</td><td>{esc(n.get('gap',''))}</td></tr>"
        for n in r.get("nonconformities", []) or [])
    ca_rows = "".join(
        f"<tr><td>{esc(a.get('nc_id',''))}</td><td>{esc(a.get('action',''))}</td>"
        f"<td>{esc(a.get('owner',''))}</td><td>{esc(a.get('due',''))}</td><td>{esc(a.get('status',''))}</td></tr>"
        for a in r.get("corrective_actions", []) or [])

    ncs = r.get("nonconformities", []) or []
    major = sum(1 for n in ncs if n.get("severity") == "严重")
    minor = sum(1 for n in ncs if n.get("severity") == "一般")
    ob = sum(1 for n in ncs if n.get("severity") == "观察项")

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>管理体系内部审核报告 · {esc(m.get('standard',''))}</title>
<style>{CSS}</style></head>
<body><div class="wrap">
<header>
  <h1>管理体系内部审核报告</h1>
  <div class="meta">标准：{esc(m.get('standard',''))} ｜ 类型：{esc(m.get('audit_type',''))} ｜ 范围：{esc(m.get('scope',''))}</div>
  <div class="meta">周期：{esc(m.get('period',''))} ｜ 计划日期：{esc(m.get('planned_date',''))}</div>
</header>

<section class="sec">
  <h2>一、年度审核方案</h2>
  <table><thead><tr><th>月份</th><th>审核类型</th><th>覆盖范围</th><th>审核员</th></tr></thead>
  <tbody>{plan_rows}</tbody></table>
</section>

<section class="sec">
  <h2>二、审核检查表要点</h2>
  <table><thead><tr><th>条款</th><th>标准要求</th><th>检查要点</th><th>证据期望</th></tr></thead>
  <tbody>{chk_rows}</tbody></table>
</section>

<section class="sec">
  <h2>三、不符合项清单</h2>
  <table><thead><tr><th>编号</th><th>条款</th><th>级别</th><th>标准要求</th><th>客观证据</th><th>差距</th></tr></thead>
  <tbody>{nc_rows}</tbody></table>
</section>

<section class="sec">
  <h2>四、整改追踪台账</h2>
  <table><thead><tr><th>关联不符合项</th><th>纠正措施</th><th>责任部门</th><th>计划完成</th><th>状态</th></tr></thead>
  <tbody>{ca_rows}</tbody></table>
</section>

<section class="sec">
  <h2>五、审核结论</h2>
  <div class="conclusion">
    本次审核共发现不符合项 <b>{len(ncs)}</b> 项（严重 {major} / 一般 {minor} / 观察 {ob}）。<br>
    整改闭环率、过程有效性评价详见管理评审输入。结论由企业审核组签署。
  </div>
</section>

<footer>本报告由 管理体系内部审核技能 生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')} · 主色 {MAIN}</footer>
</div></body></html>"""


def main():
    ap = argparse.ArgumentParser(description="管理体系内部审核报告生成器")
    ap.add_argument("--input", help="结构化结果 JSON 路径（缺省使用内置演示数据）")
    ap.add_argument("--md-out", help="输出 MD 路径")
    ap.add_argument("--html-out", help="输出 HTML 路径")
    args = ap.parse_args()

    if args.input:
        try:
            r = load_result(args.input)
        except Exception as e:
            sys.stderr.write(f"读取输入失败：{e}\n")
            sys.exit(1)
    else:
        r = DEMO
        sys.stderr.write("未指定 --input，使用内置演示数据。\n")

    out_dir = None
    if not args.md_out and not args.html_out:
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(out_dir, exist_ok=True)
        args.md_out = os.path.join(out_dir, "audit_report.md")
        args.html_out = os.path.join(out_dir, "audit_report.html")

    if args.md_out:
        with open(args.md_out, "w", encoding="utf-8") as f:
            f.write(build_md(r))
        sys.stderr.write(f"MD 已生成：{args.md_out}\n")
    if args.html_out:
        with open(args.html_out, "w", encoding="utf-8") as f:
            f.write(build_html(r))
        sys.stderr.write(f"HTML 已生成：{args.html_out}\n")


if __name__ == "__main__":
    main()
