# 管理体系内部审核（internal-management-audit）

> 主色：`#C8102E`
> 范式：混合式双版（MD + HTML），由 `scripts/build_report.py` 生成。

## 简介

面向内审员与体系工程师的审核策划与实施助手。覆盖 ISO 9001 / IATF 16949 / EMS 等管理体系的内部审核全流程：年度审核方案、检查表、不符合项报告、整改闭环台账与标准化审核报告。

## 适用角色

- 内审员：实施现场审核、记录发现、开具不符合项。
- 体系工程师 / 体系主管：策划审核方案、编制检查表、跟踪整改与归档报告。

## 目录结构

```
internal-management-audit/
├── SKILL.md                  # 技能定义（10 节结构 + TRACE 自评）
├── README.md                 # 本文件
├── scripts/
│   └── build_report.py       # 双版报告生成器（MD + HTML）
└── references/
    ├── audit_checklist.md    # 条款/过程/产品检查要点库
    └── nc_classification.md  # 不符合项分级与描述规范
```

## 快速开始

1. 调用技能，提供：审核标准、审核类型（体系/过程/产品）、审核范围。
2. 获取年度审核方案与检查表。
3. 将现场发现交给技能整理为不符合项与整改台账。
4. 运行脚本产出最终报告双版：

```bash
python scripts/build_report.py --input sample.json --md-out output/audit_report.md --html-out output/audit_report.html
# 或使用内置演示数据（无需输入文件）：
python scripts/build_report.py
```

## 报告双版说明

- **MD 版**：适合纳入知识库、版本管理与审阅批注。
- **HTML 版**：适合汇报演示，主色 `#C8102E`，含策划、检查表、不符合项、整改台账与结论。

## 注意事项

- 所有判定与签字由企业人员负责，技能仅提供方法与模板。
- 标准条款引用以 ISO 9001:2015 / IATF 16949:2016 / ISO 19011 为准；企业特定要求以「待企业补充」标注。
- 演示数据为内置小样本，正式使用前请替换为真实数据。
