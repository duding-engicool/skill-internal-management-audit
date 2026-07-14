#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""内部审核四阶段文档生成器（txt + md）。

用法：
  python build_report.py --stage scheme   --input info.json --out-dir .
  python build_report.py --stage plan     --input info.json --out-dir .
  python build_report.py --stage checklist --input info.json --out-dir .
  python build_report.py --stage report   --input info.json --out-dir .

info.json 为各阶段收集到的信息（字段均可选，缺失自动标「待补充」）。
所有产物写入 --out-dir（默认当前工作目录），不依赖任何第三方库。
"""
import argparse
import json
import os
import datetime


def _g(d, key, default="待补充"):
    v = d.get(key)
    if v in (None, "", [], {}):
        return default
    return v


def _lines(v):
    if isinstance(v, list):
        return "\n".join(f"- {x}" for x in v) if v else "待补充"
    return str(v)


def render_scheme(d):
    title = "内部审核方案"
    purpose = _g(d, "purpose", "通过内部审核，确认质量管理体系与适用标准的符合性、有效性，识别改进机会。")
    scope = _g(d, "scope")
    criteria = _g(d, "criteria", _g(d, "standard", "待补充（审核标准）"))
    team = _lines(_g(d, "audit_team", []))
    period = _g(d, "plan_period")
    focus = _g(d, "focus")
    resources = _lines(_g(d, "resources", []))
    md = f"""# {title}

## 1. 审核目的
{purpose}

## 2. 审核范围
{scope}

## 3. 审核准则
{criteria}

## 4. 审核组织与职责
{team}

## 5. 审核时间安排
{period}

## 6. 风险识别与重点关注过程
{focus}

## 7. 审核资源
{resources}

## 8. 审核方案批准
| 角色 | 姓名 | 签字 | 日期 |
|------|------|------|------|
| 编制 |      |      |      |
| 审核 |      |      |      |
| 批准 |      |      |      |
"""
    return title, md


def render_plan(d):
    title = "内部审核实施计划"
    basic = _g(d, "basic_info", "（复用阶段1：目的/范围/准则）")
    team = _lines(_g(d, "audit_team", []))
    schedule = _lines(_g(d, "schedule", []))
    meetings = _g(d, "meetings")
    notes = _g(d, "notes")
    md = f"""# {title}

## 1. 基本信息
{basic}

## 2. 审核组成员及分工
{team}

## 3. 详细日程安排
{schedule}

## 4. 首次会议、末次会议安排
{meetings}

## 5. 备注要求
{notes}
"""
    return title, md


def render_checklist(d):
    title = "内部审核检查表汇编"
    depts = d.get("departments") or []
    if not depts:
        depts = [{"name": "待补充", "responsibilities": "待补充", "core_processes": "待补充",
                  "special_requirements": "无", "criteria": "待补充", "items": []}]
    blocks = []
    for i, dep in enumerate(depts, 1):
        name = _g(dep, "name")
        resp = _g(dep, "responsibilities")
        core = _g(dep, "core_processes")
        spec = _g(dep, "special_requirements", "无")
        crit = _g(dep, "criteria")
        items = dep.get("items") or []
        if items:
            rows = "\n".join(
                f"| {_g(it,'clause')} | {_g(it,'question')} | {_g(it,'method')} |   |   |"
                for it in items
            )
        else:
            rows = "| 待补充 | 待补充 | 待补充 |   |   |"
        block = f"""### 检查表 {i}：{name}

- 受审核部门/过程：{name}
- 主要职责：{resp}
- 核心过程：{core}
- 特殊审核要求：{spec}
- 审核准则：{crit}

| 条款号 | 审核内容/提问 | 查证方法 | 符合/不符合/观察项 | 备注 |
|--------|--------------|----------|-------------------|------|
{rows}

- 审核人员签字：__________  受审核部门负责人签字：__________  日期：__________
"""
        blocks.append(block)
    md = f"# {title}\n\n" + "\n".join(blocks)
    return title, md


def render_report(d):
    title = "内部审核报告"
    overview = _g(d, "overview")
    basis = _g(d, "basis", _g(d, "criteria", "待补充"))
    team = _lines(_g(d, "audit_team", []))
    review = _g(d, "system_review")
    ncs = _lines(_g(d, "nonconformities", []))
    obs = _g(d, "observations", "无观察项")
    improve = _lines(_g(d, "improvements", []))
    conclusion = _g(d, "conclusion")
    attachments = _g(d, "attachments", "不符合项清单、审核检查表汇编、审核计划、审核方案")
    md = f"""# {title}

## 1. 审核概况
{overview}

## 2. 审核依据
{basis}

## 3. 审核组成员及分工
{team}

## 4. 体系运行综述
{review}

## 5. 不符合项汇总
{ncs}

## 6. 观察项汇总
{obs}

## 7. 改进建议
{improve}

## 8. 审核结论
{conclusion}

## 9. 附件
{attachments}

## 10. 表尾（签字栏）
| 角色 | 姓名 | 签字 | 日期 |
|------|------|------|------|
| 审核组长 |      |      |      |
| 审核组成员 |      |      |      |
| 批准人 |      |      |      |
"""
    return title, md


STAGES = {
    "scheme": render_scheme,
    "plan": render_plan,
    "checklist": render_checklist,
    "report": render_report,
}


def md_to_txt(md: str) -> str:
    """将 markdown 转为纯文本（去表格线、标题#，加分隔线）。"""
    out = []
    for line in md.splitlines():
        s = line.rstrip()
        if s.startswith("# "):
            out.append(s[2:])
            out.append("=" * 40)
        elif s.startswith("## "):
            out.append(s[3:])
            out.append("-" * 36)
        elif s.startswith("### "):
            out.append(s[4:])
            out.append("-" * 28)
        elif s.startswith(("#",)):
            out.append(s.lstrip("# "))
        elif s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            out.append(" | ".join(cells))
        elif s.startswith("- "):
            out.append(s)
        else:
            out.append(s)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="内部审核四阶段文档生成器")
    ap.add_argument("--stage", required=True, choices=list(STAGES.keys()), help="阶段")
    ap.add_argument("--input", required=True, help="收集信息 JSON 文件路径")
    ap.add_argument("--out-dir", default=os.getcwd(), help="输出目录，默认当前工作目录")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    title, md = STAGES[args.stage](data)
    date = datetime.date.today().strftime("%Y%m%d")
    base = f"{title}_{date}"
    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)
    md_path = os.path.join(out_dir, base + ".md")
    txt_path = os.path.join(out_dir, base + ".txt")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(md_to_txt(md))
    print(f"已生成：{md_path}\n已生成：{txt_path}")


if __name__ == "__main__":
    main()
