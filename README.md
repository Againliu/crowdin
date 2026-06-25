# 🌐 Crowdin — Multilingual Copy Management for XAG Agri-Tech Products

[中文](#中文说明)

Read-only integration with [Crowdin](https://crowdin.com) for XAG (极飞科技) agricultural technology products. Query translation status across **9 products and 18 target languages**, export localization bundles, and detect formatting inconsistencies — all through a single API token.

## What This Skill Provides

### Translation Intelligence

| Capability | Description | Data Granularity |
|-----------|-------------|-----------------|
| **Project inventory** | List all 9 XAG products on Crowdin | Project name, ID, source/target languages |
| **Translation progress** | Real-time completion stats per language | Total strings, translated, approved, coverage % |
| **String search** | Find source copy by text, identifier, or tag | Full string content with context metadata |
| **Bundle export** | Download ready-to-use localization packages | Android `strings.xml`, iOS `Localizable.strings`, JSON, CSV |
| **Progress tracking** | Historical translation velocity | Per-language trend over time |

### Quality Assurance

| Capability | Description |
|-----------|-------------|
| **Placeholder consistency check** | Detect format-string mismatches across languages (`%1$s` vs `%s` vs `%1@`) |
| **Coverage gap analysis** | Identify which languages are falling behind |
| **String audit** | Export all strings with translation status for external review |

### Data Access

| Data Type | Available Fields |
|-----------|-----------------|
| **Source strings** | ID, identifier, text, context, tags, max length, labels |
| **Translations** | Translated text, approval status, translator, vote count |
| **Project metadata** | Name, description, source language, target languages, member count |
| **Glossaries** | Term, translation, part of speech, description, language |
| **Translation memories** | Source segment, target segment, language pair |
| **Progress stats** | Total phrases, translated, approved, coverage percentage per language |

## Products Covered

| Product | Crowdin Project | Target Languages |
|---------|----------------|-----------------|
| **XAG ONE (极飞农服)** | Main project | **17 languages** — the most comprehensive |
| XAG AutoPilot (极飞农机) | Secondary | 14 languages (incl. en/ja/ko/ru/tr/id/th/ug) |
| XAG Farm (极飞农场) | Consumer-facing | 9 languages (ar/ru/tr/en/vi/km/th/ug/uz) |
| XAG Go (极飞无人车) | Robotics | 8 languages (fr/es/ja/ko/tr/en/id/th) |
| Xcare Tool (极加检修) | Maintenance | 1 language (en) |
| XAG Service / XAG Mes / Admin | Internal | 1 language each (en) |

> These are snapshots. Run `scripts/get_progress.py` for real-time data — Crowdin is the single source of truth.

## API Coverage

**51 of 338 official Crowdin endpoints** verified usable (read-only token scope):

| Category | Endpoints | Key Operations |
|----------|-----------|---------------|
| Projects | 4 | List, get details, languages, members |
| Source strings | 3 | List, search by text/identifier, get by ID |
| Translations | 3 | List translations, build via Bundle, download |
| Bundles | 5 | List, create, export, download, delete |
| Progress | 2 | Translation progress, QA check progress |
| Glossaries | 4 | List glossaries, terms, search |
| Translation Memory | 3 | List TMs, search segments |
| Members | 2 | List project members, get details |
| Tasks | 3 | List, get, search |
| Comments | 2 | List string comments |
| Screenshots | 3 | List screenshots, get, list tags |
| MT Engines | 2 | List engines, translate via engine |
| Languages | 2 | List supported languages, get details |
| Issues | 3 | List, get, search string issues |
| Labels | 4 | List, add, remove, assign to strings |

## Included Scripts

| Script | Purpose | Example |
|--------|---------|---------|
| `list_projects.py` | List all XAG Crowdin projects | `python3 scripts/list_projects.py` |
| `get_progress.py` | Translation progress per language | `python3 scripts/get_progress.py --project 744513` |
| `lookup_string.py` | Search source strings | `python3 scripts/lookup_string.py --project 744513 --text "作业"` |
| `download_bundle.py` | Export localization bundle (3-step) | `python3 scripts/download_bundle.py --project 744513 --bundle 123` |
| `export_to_excel.py` | Full string export to Excel | `python3 scripts/export_to_excel.py --project 744513 --lang en` |
| `check_placeholders.py` | Detect format-string issues | `python3 scripts/check_placeholders.py --project 744513` |

## Prerequisites

- Python 3.8+
- `requests` and `openpyxl` (`pip install requests openpyxl`)
- A Crowdin Personal Access Token (read-only scope)

## Setup

1. Copy `crowdin/` into your agent's skills directory
2. Store your Crowdin API token in a secure file (e.g. `~/.hermes/credentials/crowdin.txt`, chmod 600)
3. Verify: `python3 scripts/list_projects.py`

## Typical Use Cases

- **"How many languages does XAG ONE support?"** → Run `get_progress.py`, get exact count + coverage per language
- **"Is the Turkish translation for the spray module done?"** → Search strings, check translation status
- **"Export all English strings for the QA team"** → Run `export_to_excel.py`
- **"Are there format-string bugs in the latest build?"** → Run `check_placeholders.py`
- **Pre-release translation review** → Download bundle, diff against previous version

## Reference Documents

| File | Contents |
|------|----------|
| `references/official-api-audit.md` | Full endpoint audit: which of 338 endpoints work, which don't, and why |
| `references/placeholder-scan-baseline.md` | Baseline results from the placeholder consistency scan |

## Version

v1.3.5 · Updated 2026-06-14

---

## 中文说明

# 🌐 Crowdin — 极飞农服产品多语言文案管理平台

只读访问 [Crowdin](https://crowdin.com)，覆盖极飞科技农业技术产品的全部多语言文案管理。跨 **9 个产品、18 种目标语言** 查询翻译状态，导出本地化包，检测格式化不一致问题 — 一个 API Token 搞定。

## 核心能力

### 翻译情报

| 能力 | 说明 | 数据粒度 |
|------|------|---------|
| **项目清单** | 列出全部 9 个极飞产品 | 项目名、ID、源/目标语言 |
| **翻译进度** | 每种语言的实时完成统计 | 总条数、已翻译、已批准、覆盖率 |
| **文案搜索** | 按文本、identifier 或标签查找源文案 | 完整文案内容 + 上下文元数据 |
| **Bundle 导出** | 下载可直接使用的本地化包 | Android `strings.xml`、iOS `Localizable.strings`、JSON、CSV |
| **进度追踪** | 历史翻译速度 | 各语言随时间变化趋势 |

### 质量保证

| 能力 | 说明 |
|------|------|
| **占位符一致性检查** | 检测多语言间格式化字符串不一致（`%1$s` vs `%s` vs `%1@`） |
| **覆盖率差距分析** | 识别哪些语言翻译进度落后 |
| **文案审计** | 导出所有文案及翻译状态，供外部审核 |

### 可访问的数据

| 数据类型 | 可用字段 |
|---------|---------|
| **源文案** | ID、identifier、文本、上下文、标签、最大长度、标注 |
| **翻译** | 译文、批准状态、翻译者、投票数 |
| **项目元数据** | 名称、描述、源语言、目标语言、成员数 |
| **术语库** | 术语、翻译、词性、描述、语言 |
| **翻译记忆库** | 源片段、目标片段、语言对 |
| **进度统计** | 总词条数、已翻译、已批准、各语言覆盖率 |

## 覆盖的产品

| 产品 | Crowdin 项目 | 目标语言数 |
|------|-------------|-----------|
| **极飞农服 XAG ONE** | 主项目 | **17 种语言**（最全面） |
| 极飞农机 XAG AutoPilot | 次主项目 | 14 种（含 en/ja/ko/ru/tr/id/th/ug） |
| 极飞农场 XAG Farm | 面向消费者 | 9 种（ar/ru/tr/en/vi/km/th/ug/uz） |
| 极飞无人车 XAG Go | 机器人 | 8 种（fr/es/ja/ko/tr/en/id/th） |
| 极加检修 Xcare Tool | 维保 | 1 种（en） |
| 极飞服务 / XAG Mes / 管理平台 | 内部 | 各 1 种（en） |

> 以上为快照值。运行 `scripts/get_progress.py` 获取实时数据 — Crowdin 是唯一权威来源。

## API 覆盖

官方 338 个端点中 **51 个** 已验证可用（只读 Token 范围）：

| 分类 | 端点数 | 主要操作 |
|------|--------|---------|
| 项目 | 4 | 列出、详情、语言、成员 |
| 源字符串 | 3 | 列出、按文本/identifier 搜索、按 ID 获取 |
| 翻译 | 3 | 列出翻译、通过 Bundle 构建、下载 |
| Bundle | 5 | 列出、创建、导出、下载、删除 |
| 进度 | 2 | 翻译进度、QA 检查进度 |
| 术语库 | 4 | 列出术语库、术语、搜索 |
| 翻译记忆库 | 3 | 列出 TM、搜索片段 |
| 成员 | 2 | 列出项目成员、详情 |
| 任务 | 3 | 列出、获取、搜索 |
| 评论 | 2 | 列出字符串评论 |
| 截图 | 3 | 列出截图、获取、列出标签 |
| MT 引擎 | 2 | 列出引擎、通过引擎翻译 |
| 语言 | 2 | 列出支持语言、详情 |
| 问题 | 3 | 列出、获取、搜索字符串问题 |
| 标签 | 4 | 列出、添加、删除、分配给字符串 |

## 附带脚本

| 脚本 | 用途 | 示例 |
|------|------|------|
| `list_projects.py` | 列出所有极飞 Crowdin 项目 | `python3 scripts/list_projects.py` |
| `get_progress.py` | 各语言翻译进度 | `python3 scripts/get_progress.py --project 744513` |
| `lookup_string.py` | 搜索源字符串 | `python3 scripts/lookup_string.py --project 744513 --text "作业"` |
| `download_bundle.py` | 导出本地化包（三步） | `python3 scripts/download_bundle.py --project 744513 --bundle 123` |
| `export_to_excel.py` | 全量导出到 Excel | `python3 scripts/export_to_excel.py --project 744513 --lang en` |
| `check_placeholders.py` | 检测格式化字符串问题 | `python3 scripts/check_placeholders.py --project 744513` |

## 环境要求

- Python 3.8+
- `requests` 和 `openpyxl`（`pip install requests openpyxl`）
- Crowdin 个人访问令牌（只读权限）

## 安装

1. 将 `crowdin/` 目录复制到你的 Agent skills 目录
2. 将 Crowdin API Token 存到安全文件（如 `~/.hermes/credentials/crowdin.txt`，chmod 600）
3. 验证：`python3 scripts/list_projects.py`

## 典型使用场景

- **"极飞农服支持几种语言？"** → 运行 `get_progress.py`，秒出精确数量 + 各语言覆盖率
- **"土耳其语喷洒模块翻译完了吗？"** → 搜索字符串，检查翻译状态
- **"导出所有英文文案给 QA 团队"** → 运行 `export_to_excel.py`
- **"最新构建有格式化字符串 bug 吗？"** → 运行 `check_placeholders.py`
- **发布前翻译审核** → 下载 Bundle，与上一版本做 diff

## 参考文档

| 文件 | 内容 |
|------|------|
| `references/official-api-audit.md` | 完整端点审计：338 个端点中哪些可用、哪些不可用、原因 |
| `references/placeholder-scan-baseline.md` | 占位符一致性扫描的基线结果 |

## 版本

v1.3.5 · 更新于 2026-06-14
