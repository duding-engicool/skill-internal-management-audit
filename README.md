# 管理体系内部审核（internal-management-audit）

> 范式：四阶段交互式（一问一答），产出 txt + md 文档，可直接打印。
> 内核提示词见 `references/internal_audit_phases.md`（忠实移植自 IMA 知识库「保姆级·交互式QMS内审全流程AI提示词·分四阶段版」）。

## 简介

面向内审员与体系工程师的内部审核全流程助手。按四阶段顺序（审核方案 → 实施计划 → 部门检查表 → 审核报告）逐步引导，每次只问 1 个问题、等确认再下一个，适配内审新手，贴合 ISO 9001 / IATF 16949 等体系。

## 适用角色

- 内审员：实施现场审核、记录发现、开具不符合项。
- 体系工程师 / 体系主管：策划审核方案、编制检查表、跟踪整改与归档报告。

## 目录结构

```
internal-management-audit/
├── SKILL.md                    # 技能定义（10 节结构 + TRACE 自评）
├── README.md                   # 本文件
├── scripts/
│   └── build_report.py         # 四阶段文档生成器（txt + md）
└── references/
    ├── internal_audit_phases.md # 四阶段完整交互式提示词（角色/铁律/提问清单/交付物/风险）
    ├── audit_checklist.md       # 条款/过程/产品检查要点库
    └── nc_classification.md     # 不符合项分级与描述规范
```

## 四阶段流程

1. **阶段1 编制《内部审核方案》**（固定提问 1-8）→ 交付审核方案
2. **阶段2 编制《内部审核实施计划》**（固定提问 1-6）→ 交付实施计划
3. **阶段3 编制《部门审核检查表》**（每部门 1-5）→ 交付检查表汇编
4. **阶段4 编制《内部审核报告》**（固定提问 1-8）→ 交付审核报告

## 快速开始

1. 调用技能，Agent 按阶段1提问清单逐步引导。
2. 每阶段信息收齐后，Agent 输出该阶段正式文档并请你确认。
3. 也可将收集到的信息写入 JSON，运行脚本直接生成文档：

```bash
python scripts/build_report.py --stage scheme    --input info.json --out-dir .
python scripts/build_report.py --stage plan      --input info.json --out-dir .
python scripts/build_report.py --stage checklist --input info.json --out-dir .
python scripts/build_report.py --stage report    --input info.json --out-dir .
```

## 注意事项

- 所有判定与签字由企业人员负责，技能仅提供方法与模板。
- 标准条款引用以 ISO 9001:2015 / IATF 16949:2016 为准；企业特定要求以「待企业补充」标注。
- 演示数据为内置小样本，正式使用前请替换为真实数据。
