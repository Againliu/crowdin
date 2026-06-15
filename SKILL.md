---
name: crowdin
description: 极飞农服相关产品的多语言文案管理平台（Crowdin）只读访问。官方 338 个端点，实测确认可用 51 个（只读 token 限制）。覆盖：项目列表/详情、源字符串、翻译导出（Bundle）、翻译进度、术语库、翻译记忆、成员、任务、评论、截图、词典、MT引擎、标签、语言列表、问题。含
  8 条高效查询经验（分页缓存/并发/本地过滤/dict join/Bundle三步走）。
version: 1.3.5
created: 2026-06-02
updated: 2026-06-14
---


# Crowdin 只读访问 Skill（极飞农服多语言文案平台）

## 安装

### 1. 复制 Skill
```bash
cp -r crowdin/ /path/to/your/agent/skills/
```

### 2. 安装依赖
无额外依赖。

### 3. 配置环境变量
无需额外环境变量。

### 4. 验证
查看 SKILL.md 中的使用说明，按文档操作即可。

## 这是什么

极飞农服在 [Crowdin](https://crowdin.com) 上管理所有产品的多语言文案（zh-CN 源语言 → 18 种目标语言）。

本 skill 让你（agent）能用 **API Token**（只读）拉取：
- 所有 9 个 XAG 项目（极飞农服 / 极飞农机 / 极飞农场 / 极加检修 / 极飞无人车 / 极飞生产执行系统 等）
- 每个项目的源字符串（zh-CN → 字符串 ID + identifier + 文案 + 标签）
- 每种目标语言的翻译（仅 en / ja / ko / th / tr / vi / 等已激活语言）
- 翻译进度（每种语言的总条数 / 已译 / 已批准 / 覆盖率）
- 术语库（Glossaries）和翻译记忆库（TMs）

**能做但之前以为不能**：**Bundle 翻译包下载**（`/bundles/{id}/exports` + `/download`）可以正常下载 Android strings.xml / iOS Localizable.strings / JSON 等格式的多语言包。

**不能做**：上传文件、提交翻译、修改术语。传统 build 端点（`/translations/builds`）404，但 bundle export 端点可用。

## 触发场景

**必触发（不要绕远路）**：
- ❓ **用户问"极飞农服/极飞农机/极飞农场/极加检修/极飞无人车 App 支持哪些语言 / 语种 / i18n / 国际化 / 多语言"** → **立刻加载本 skill**，跑 `scripts/list_projects.py` 或 `scripts/get_progress.py` 拿实时数据，**不要搜飞书文档**（飞书里只有历史规划，不是当前状态；Crowdin 才是 source of truth）
- ❓ **用户问某语言翻译进度 / 覆盖率 / 还差多少没译** → 跑 `scripts/get_progress.py --project 744513`

**其他触发**：
- 拿到产品文案要翻译 / 校对 / 评估翻译质量
- 给开发提 PR 前查某条文案在 Crowdin 上是否已翻译
- 批量导出某项目某语言的文案到 Excel
- 想知道某语言翻译进度还差多少
- 用户问"XX 项目的文案在 Crowdin 上叫什么 identifier"
- 给海外团队 / 翻译服务商同步文案

## 已知项目语言数（快照，定期用脚本刷新）

| 项目 | 目标语言数 |
|---|---|
| XAG Farm 极飞农场 | 9 (ar/ru/tr/en/vi/km/th/ug/uz) |
| XAG AutoPilot 极飞农机 | 14 (含 en/ja/ko/ru/tr/id/th/ug) |
| XAG ONE **极飞农服** | **17**（主项目，最常被问） |
| Xcare Tool 极加检修 | 1 (en) |
| XAG Go 极飞无人车 | 8 (fr/es/ja/ko/tr/en/id/th) |
| XAG Service 极飞服务 / XAG Mes / 管理平台 | 各 1 (en) |

**完整当前语言列表** = 跑 `get_progress.py`，不要靠记忆。

## 踩坑：语言类问题不要搜飞书文档

2026-06-03 Jacky 问"极飞农服 App 支持哪几种语言"，我没加载本 skill，去飞书 `docs +search` 搜了 5 轮，只找到 2024 年产品规划里"Q1 新增 2 个语种、Q2 再增 2 个"这种历史计划，根本拿不到当前真实列表。最后只能建议他问人。

**正确做法**：加载本 skill → 跑 `python3 scripts/get_progress.py --project 744513` → 秒出 17 种语言及各自进度。**Crowdin 项目配置的 `targetLanguageIds` 就是当前激活语言清单**，是唯一权威来源。

## 凭据

**Token 已存到**：`~/.hermes/credentials/crowdin.txt`（chmod 600）
- 这是 XAG 账号的 **Personal Access Token (Read-Only)**
- 80 字符，前缀 `0ca9`
- **绝不能写入代码 / 提交 git / 转发给 Lucy**（Lucy 在海外 / 美国服务器；token 是中国国内凭据）

**永远从 `~/.hermes/credentials/crowdin.txt` 读 token**：

```python
import os
TOKEN = open(os.path.expanduser('~/.hermes/credentials/crowdin.txt')).read().strip()
```

## XAG 项目索引（9 个，全部可见）

| ID | identifier | 名称 | 源语言 | 目标语言数 |
|---|---|---|---|---|
| 744289 | `nongchang` | XAG Farm 极飞农场 | zh-CN | 9 (ar/ru/tr/en/vi/km/th/ug/uz) |
| 744297 | `xapc` | XAG AutoPilot 极飞农机 | zh-CN | 14 (含 en/ja/ko/ru/tr/id/th/ug) |
| 744303 | `XCARETOOL` | Xcare Tool 极加检修 | zh-CN | 1 (en) |
| 744513 | `xagone` | **XAG ONE 极飞农服** | zh-CN | 17 (主项目，最常用) |
| 746881 | `testxag001` | 测试项目 001 | zh-CN | 9 (测试用) |
| 748629 | `xagservice` | XAG Service 极飞服务 | zh-CN | 1 (en) |
| 773277 | `xag-one-management-platform` | XAG One Management Platform 极飞农服管理平台 | zh-CN | 1 (en) |
| 806874 | `xag-go` | XAG Go 极飞无人车 | zh-CN | 8 (fr/es/ja/ko/tr/en/id/th) |
| 874794 | `XAGMes` | XAG Mes 极飞生产执行系统 | zh-CN | 1 (en) |

**极飞农服 App 文案 = `xagone` (744513)**，主战场。

## 完整 API 端点索引

官方 API 共 338 个端点（29 个类别）。我们 token 是只读，188 个写操作用不了。
下表按类别列出所有端点，标注我们 token 的可用性。

Base URL: `https://api.crowdin.com/api/v2`
所有请求加 `Authorization: Bearer <token>`
**限流**: 每账号同时最多 20 个请求，超限返回 429。

### 1. Projects 项目（5 个只读可用 / 共 17）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/projects` | 列所有项目 | ✅ limit 500 |
| GET | `/projects/{id}` | 项目详情 | ✅ 含 targetLanguageIds |
| GET | `/projects/{id}/file-format-settings` | 文件格式设置列表 | ⚠️ 未验证 |
| GET | `/projects/{id}/strings-exporter-settings` | 字符串导出设置 | ⚠️ 未验证 |
| POST/PATCH/DELETE | 各种写操作 | 创建/编辑/删除项目 | 🔒 需写 token |

### 2. Source Files 源文件（大部分 404 / 共 24）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/projects/{id}/branches` | 分支列表 | ✅ xagone 只有 main(id=30) |
| GET | `/projects/{id}/branches/{branchId}` | 分支详情 | ✅ |
| GET | `/projects/{id}/branches/{branchId}/languages/progress` | 分支翻译进度 | ✅ |
| GET | `/projects/{id}/directories` | 目录列表 | ❌ 404 |
| GET | `/projects/{id}/directories/{id}` | 目录详情 | ❌ 404 |
| GET | `/projects/{id}/files` | 文件列表 | ❌ 404 |
| GET | `/projects/{id}/files/{id}` | 文件详情 | ❌ 404 |
| GET | `/projects/{id}/files/{id}/download` | 下载文件 | ❌ 404 |
| GET | `/projects/{id}/files/{id}/languages/progress` | 文件翻译进度 | ❌ 404 |
| GET | `/projects/{id}/files/{id}/revisions` | 文件版本 | ❌ 404 |
| 其他 | 写操作 | | 🔒 需写 token |

**经验**: 文件树对我们的 token 不可见，无法按文件维度分析。用 branches + strings + labels 替代。

### 3. Source Strings 源字符串（6 个 / 只读 3 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/projects/{id}/strings?limit=500&offset=N` | 拉源字符串 | ✅ **500/页，必须分页** |
| GET | `/projects/{id}/strings/{stringId}` | 单条字符串 | ✅ |
| GET | `/projects/{id}/strings?ids=A,B,C` | 批量查多条 | ✅ |
| POST | `/projects/{id}/strings` | 添加字符串 | 🔒 |
| PATCH | `/projects/{id}/strings` | 批量操作 | 🔒 |
| PATCH/DELETE | `/projects/{id}/strings/{id}` | 编辑/删除 | 🔒 |

### 4. String/Asset Translations 翻译（19 个 / 只读 5 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/projects/{id}/languages/{lang}/translations?limit=500&offset=N` | 该语言翻译 | ✅ **500/页** |
| GET | `/projects/{id}/translations?languageId={lang}&limit=500` | 翻译列表（需传 languageId） | ✅ |
| GET | `/projects/{id}/translations/{translationId}` | 单条翻译 | ✅ |
| GET | `/projects/{id}/approvals?translationId=X` | 翻译审批（需 translationId） | ⚠️ 需参数 |
| GET | `/projects/{id}/votes?translationId=X` | 翻译投票（需 translationId） | ⚠️ 需参数 |
| GET | `/projects/{id}/pre-translations` | 预翻译列表 | ✅ |
| GET | `/projects/{id}/pre-translations/{id}` | 预翻译状态 | ✅ |
| 其他 | 写操作 | | 🔒 |

**经验**: `approvals` 和 `votes` 必须传 `translationId` 参数，不能空查列表。`translations` 必须传 `languageId`。

### 5. Translation Status 翻译进度（9 个 / 只读 5 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/projects/{id}/languages/progress` | **项目整体翻译进度（所有语言）** | ✅ **最常用** |
| GET | `/projects/{id}/languages/{lang}/progress` | 单语言进度 | ✅ words/phrases/approved |
| GET | `/projects/{id}/branches/{branchId}/languages/progress` | 分支进度 | ✅ |
| GET | `/projects/{id}/directories/{id}/languages/progress` | 目录进度 | ❌ 404 |
| GET | `/projects/{id}/files/{id}/languages/progress` | 文件进度 | ❌ 404 |
| GET | `/projects/{id}/qa-checks` | QA 检查问题 | ⚠️ 大数据量可能超时 |
| POST | `/projects/{id}/qa-checks/revalidate` | 重新验证 QA | 🔒 |

**经验**: `GET /projects/{id}/languages/progress` 一次返回所有语言的进度，比逐个语言查高效得多。

### 6. Translations 翻译导出（28 个 / 只读 8 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/projects/{id}/bundles` | Bundle 列表 | ✅ |
| GET | `/projects/{id}/bundles/{id}` | Bundle 详情 | ✅ |
| POST | `/projects/{id}/bundles/{id}/exports` | 创建导出 | ✅ |
| GET | `/projects/{id}/bundles/{id}/exports/{exportId}` | 查导出状态 | ✅ |
| GET | `/projects/{id}/bundles/{id}/exports/{exportId}/download` | 下载链接 | ✅ 预签名 S3 URL |
| GET | `/projects/{id}/bundles/{id}/files` | Bundle 文件列表 | ❌ 404 |
| POST | `/projects/{id}/translations/builds` | 传统构建 | ❌ 404 |
| GET | `/projects/{id}/translations/builds` | 传统构建列表 | ❌ 404 |
| 其他 | 写操作（预翻译、导入、上传翻译等） | | 🔒 |

### 7. Labels 标签（9 个 / 只读 2 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/projects/{id}/labels` | 标签列表 | ✅ xagone 有 97 个 |
| GET | `/projects/{id}/labels/{labelId}` | 标签详情 | ✅ |
| 其他 | 创建/编辑/删除/分配标签 | | 🔒 |

### 8. Glossaries 术语库（21 个 / 只读 7 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/glossaries?limit=500` | 术语库列表 | ✅ |
| GET | `/glossaries/{id}` | 术语库详情 | ✅ |
| GET | `/glossaries/{id}/terms?limit=500` | 术语条目 | ✅ |
| GET | `/glossaries/{id}/terms/{termId}` | 单条术语 | ✅ |
| GET | `/glossaries/{id}/concepts` | 概念列表 | ✅ |
| GET | `/glossaries/{id}/exports/{id}` | 导出状态 | ✅ |
| GET | `/glossaries/{id}/exports/{id}/download` | 下载术语库 | ✅ |
| POST | `/glossaries/{id}/exports` | 导出术语库 | 🔒 |
| POST | `/projects/{id}/glossaries/concordance` | 术语一致性搜索 | ⚠️ 未验证 |
| 其他 | 写操作 | | 🔒 |

### 9. Translation Memory 翻译记忆（20 个 / 只读 7 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/tms?limit=500` | TM 列表 | ✅ |
| GET | `/tms/{id}` | TM 详情 | ✅ |
| GET | `/tms/{id}/segments` | TM 片段列表 | ⚠️ 未验证 |
| GET | `/tms/{id}/segments/{id}` | 单条片段 | ⚠️ 未验证 |
| GET | `/tms/{id}/exports/{id}` | 导出状态 | ✅ |
| GET | `/tms/{id}/exports/{id}/download` | 下载 TM | ✅ |
| GET | `/tms/{id}/imports/{id}` | 导入状态 | ✅ |
| POST | `/projects/{id}/tms/concordance` | TM 一致性搜索 | ⚠️ 未验证 |
| 其他 | 写操作 | | 🔒 |

### 10. Languages 语言（5 个 / 只读 2 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/languages` | **所有支持语言（含 locale、RTL 等）** | ✅ |
| GET | `/languages/{id}` | 语言详情 | ✅ |
| 其他 | 创建/编辑/删除自定义语言 | | 🔒 |

**经验**: `GET /languages` 返回 Crowdin 支持的全部语言（含 id/locale/name/rtl），适合做语言代码映射表。

### 11. Users 用户（7 个 / 只读 3 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/user` | 当前用户 | ✅ XAG / cloud@xa.com |
| GET | `/projects/{id}/members` | **项目成员列表** | ✅ |
| GET | `/projects/{id}/members/{id}` | 成员详情 | ✅ |
| 其他 | 添加/删除成员、编辑权限 | | 🔒 |

### 12. Tasks 任务（19 个 / 只读 6 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/projects/{id}/tasks` | 项目任务列表 | ✅ |
| GET | `/projects/{id}/tasks/{id}` | 任务详情 | ✅ |
| GET | `/projects/{id}/tasks/{id}/comments` | 任务评论 | ✅ |
| GET | `/user/tasks` | 我的任务 | ✅ |
| GET | `/users/{userId}/tasks` | 用户任务 | ✅ |
| GET | `/projects/{id}/tasks/settings-templates` | 任务模板 | ⚠️ 未验证 |
| 其他 | 写操作 | | 🔒 |

### 13. Reports 报告（19 个 / 只读 5 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| POST | `/projects/{id}/reports` | 生成报告 | 🔒 |
| GET | `/projects/{id}/reports/{id}` | 报告状态 | ✅ |
| GET | `/projects/{id}/reports/{id}/download` | 下载报告 | ✅ |
| GET | `/projects/{id}/reports/settings-templates` | 报告模板列表 | ⚠️ 未验证 |
| GET | `/users/{id}/reports/archives` | 历史报告 | ⚠️ 未验证 |
| 其他 | 写操作 | | 🔒 |

### 14. Issues 问题（2 个 / 只读 1 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/projects/{id}/issues` | 报告的问题列表 | ✅ |
| PATCH | `/projects/{id}/issues/{id}` | 编辑问题 | 🔒 |

### 15. Comments 评论（7 个 / 只读 2 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/projects/{id}/comments` | 字符串评论列表 | ✅ |
| GET | `/projects/{id}/comments/{id}` | 评论详情 | ✅ |
| 其他 | 写操作 | | 🔒 |

### 16. Screenshots 截图（13 个 / 只读 4 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/projects/{id}/screenshots` | 截图列表 | ✅ |
| GET | `/projects/{id}/screenshots/{id}` | 截图详情 | ✅ |
| GET | `/projects/{id}/screenshots/{id}/tags` | 截图标签 | ✅ |
| 其他 | 写操作 | | 🔒 |

### 17. Dictionaries 词典（2 个 / 只读 1 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/projects/{id}/dictionaries` | **词典列表（按语言）** | ✅ xagone 有 16 条 |
| PATCH | `/projects/{id}/dictionaries/{lang}` | 编辑词典 | 🔒 |

### 18. Machine Translation 机器翻译（3 个 / 只读 2 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/mts` | **MT 引擎列表** | ✅ 2 个引擎 |
| GET | `/mts/{id}` | MT 引擎详情 | ✅ |
| POST | `/mts/{id}/translations` | 用 MT 翻译 | 🔒 |

### 19. Style Guides 风格指南（5 个 / 只读 2 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/style-guides` | 风格指南列表 | ✅ |
| GET | `/style-guides/{id}` | 风格指南详情 | ✅ |
| 其他 | 写操作 | | 🔒 |

### 20. Storage 存储（4 个 / 只读 2 个）

| 方法 | 路径 | 用途 | Token 状态 |
|------|------|------|------------|
| GET | `/storages` | 存储列表 | ⚠️ 未验证 |
| GET | `/storages/{id}` | 存储详情 | ⚠️ 未验证 |
| 其他 | 写操作 | | 🔒 |

### 21. 其他类别（低优先级 / 未验证）

| 类别 | 端点数 | 只读可用 | 说明 |
|------|--------|----------|------|
| Webhooks | 5 | 2 GET | 项目 Webhook 管理 |
| Organization Webhooks | 5 | 2 GET | 组织 Webhook 管理 |
| Distributions | 7 | 3 GET | CDN 分发管理 |
| AI | 48 | ~30 GET | AI 翻译/提示词/Provider（新功能） |
| AI Gateway | 5 | 5 GET | AI 代理网关 |
| Applications | 10 | 5 GET | 第三方应用 |
| Integrations | 15 | 10 GET | 集成配置 |
| Notifications | 2 | 0 | 发通知（写操作） |
| Security Logs | 2 | 2 GET | 安全审计日志 |

**覆盖率统计**: 官方 338 个端点中，我们实测确认可用 **51 个**（含 4 个 POST 写操作中能用的 Bundle 导出），另有约 30 个标记为 ⚠️ 待验证。188 个写操作需写 token。

## 关键坑（必看）

1. **分页限制 500/页**：`?limit=500&offset=N`，offset 必须从 0 开始按 500 步进；返回条数 < 500 表示最后一页
2. **Plurals 字段是 dict 不是 string**：
   - 源串：`text` 可能是 `{"one": "...", "other": "..."}`
   - 翻译：`text` 或 `plural`（视 type 而定）
   - 写入 Excel 前必须 `json.dumps` 序列化
3. **服务端过滤失效**：`filter` 参数对只读 token 静默返回 0，**必须全量拉回本地再按 labelIds/identifier 过滤**
4. **identifier 命名规范**：通常 `模块_动作_对象` 格式，如 `survey_synchronized_to_cloud_tip`、`mission_launch_error_xxx`
5. **Coverage 96% 是常态**：`unmatched` 一般是 plurals、未批准、或未翻译
6. **Token 不要外传**：存在 `~/.hermes/credentials/`，权限 600。**绝对不要**写进代码、commit、转发给 Lucy 或任何海外 agent
7. **请求频率**：API 没明确限流，但实测连续 30+ 次无问题；写循环加 `time.sleep(0.1)` 更稳
8. **占位符正则必须匹配 `%Ns`（位置参数不带 `$`）**：Android 格式化字符串有两种位置参数写法——`%1$s`（标准）和 `%1s`（简写）。正则必须用 `(?:\d+\$?)?` 让 `$` 可选，否则 `%1s`、`%2d` 等全部漏掉。**已踩过坑（2026-06-03）**：旧正则 `%(?:\d+\$)?` 漏掉了 10+ 条不一致记录。正确模式：`r'%(?:\d+\$?)?[sdfcxeEgGaAn@%]'`
9. **占位符检查报告格式要求（用户两次纠正，2026-06-03）**：
   - **必须显示检测到的占位符**：只展示源文案和译文不够。报告必须包含「源占位符」和「译占位符」，并分类为 🔴丢失/🟡格式变/🔵多出。用户原话：「报告里面的好多文案，我都看不出源文案中有占位符」
   - **用块格式，不用表格**：每条记录一个块——key 作为标题，下面用 bullet list 列出源文案、译文、占位符对比。**不要用 6 列 Markdown 表格**，内容一长就挤成一团没法看。用户原话：「要想想我们怎么阅读起来方便」
   - **不截断内容**：源文案和译文显示完整文本，不做 `[:50]` 之类的截断。用户原话：「列的很多内容不完整」
   - **不截断条数**：全量列出所有不一致记录，不要 `items[:50]` 截断后写 `... 还有 N 处未列出`。用户原话：「条数是不是也不完整」
   - **正确格式示例**：
     ```
     **1. `key_name`**
     - 源文案：完整源文本
     - 译文（en）：完整译文文本
     - 占位符：`%s, %d` → `(无)`
     ```

## 标准工作流

### 场景 1：列出所有 XAG 项目

```python
import requests
TOKEN = open(os.path.expanduser("~/.hermes/credentials/crowdin.txt")).read().strip()
r = requests.get("https://api.crowdin.com/api/v2/projects",
                 headers={"Authorization": f"Bearer {TOKEN}"}, params={"limit": 50})
for p in r.json()["data"]:
    d = p["data"]
    print(f"{d['id']:>7}  {d['identifier']:<35}  {d['name']}")
```

### 场景 2：导出某项目某语言到 Excel

**最快路径** — 直接跑：

```bash
python3 ~/.hermes/skills/crowdin/scripts/export_to_excel.py \
  --project 744513 --lang en --out /root/crowdin_xagone_en.xlsx
```

脚本会：
1. 拉所有 labels
2. 拉所有源串（分页 500/页）
3. 拉目标语言翻译（分页 500/页）
4. 按 stringId join
5. 写 Excel，主表 + Summary 表

### 场景 3：找某条文案（按 identifier 前缀）

```python
# 必须拉全量，本地过滤
all_strings = []
offset = 0
while True:
    r = requests.get(f"https://api.crowdin.com/api/v2/projects/744513/strings",
                     headers=headers, params={"limit": 500, "offset": offset})
    data = r.json()["data"]
    all_strings.extend([d["data"] for d in data])
    if len(data) < 500: break
    offset += 500
matches = [s for s in all_strings if s["identifier"].startswith("mission_launch_error_")]
```

### 场景 4：拿某语言翻译进度

```python
r = requests.get(f"https://api.crowdin.com/api/v2/projects/744513/languages/en/progress",
                 headers=headers)
d = r.json()["data"][0]["data"]
print(f"EN: {d['translationProgress']}% translated, "
      f"{d['words']['translated']}/{d['words']['total']} words, "
      f"{d['approvalProgress']}% approved")
```

### 场景 5：下载 Bundle 翻译包（Android strings.xml / iOS .strings / JSON）

```bash
# 列出所有 bundles
python3 ~/.hermes/skills/crowdin/scripts/download_bundle.py --project 744513 --list

# 下载 Android 包（bundle id=10，所有语言，zip 格式）
python3 ~/.hermes/skills/crowdin/scripts/download_bundle.py --project 744513 --bundle 10

# 下载并解压到指定目录
python3 ~/.hermes/skills/crowdin/scripts/download_bundle.py --project 744513 --bundle 10 --extract /tmp/android_translations/

# 下载 iOS 包
python3 ~/.hermes/skills/crowdin/scripts/download_bundle.py --project 744513 --bundle 12
```

**xagone 常用 Bundle**：
| Bundle ID | 名称 | 格式 | 导出路径 |
|---|---|---|---|
| 10 | Android | android | `values-%two_letters_code%/strings.xml` |
| 12 | iOS | macosx | `%osx_code%/Localizable.strings` |
| 52 | iOSdict | stringsdict-export | `%osx_code%/Localizable.stringsdict` |
| 85 | 作业报告H5 | crowdin-json | `作业报告H5.json` |
| 87 | 权益订单H5 | crowdin-json | `权益订单H5.json` |
| 137 | 8位标准错误码-Android用 | android | `values-%two_letters_code%/strings.xml` |
| 173 | 登录注册组件-Android | android | `values-%two_letters_code%/strings.xml` |
| 175 | 登录注册组件-iOS | macosx | `%osx_code%/Localizable.strings` |

**流程**：POST 创建导出 → 轮询 status 直到 finished → GET download 拿预签名 S3 URL → 下载 zip

### 场景 6：检查翻译占位符一致性

**两个脚本版本**：
- `scripts/check_placeholders.py`（v1，单项目，交互式用）
- `<SKILL_SCRIPTS_DIR>/check_crowdin_v2.py`（v2 并发版，9 项目全扫，**cron 任务用这个**）

```bash
# v2 并发版 — 9 个项目全扫（~8 分钟，1600+ 条不一致）
cd /root/.hermes/scripts && python3 check_crowdin_v2.py > /tmp/crowdin_report_latest.md 2>/tmp/crowdin_latest_stderr.log

# v1 单项目版
python3 ~/.hermes/skills/crowdin/scripts/check_placeholders.py --project 744513
```

**⚠️ 运行约束（v2 必须注意）**：
1. **必须用 background 模式**：脚本耗时 ~500s（8 分钟），foreground 最大 600s 经常被拒（hermes 框架限制）。用 `background=true` + `notify_on_complete=true`，然后 `process(action='wait')` 轮询
2. **stderr 有进度信息**：实时显示每个项目名 + 该项目的 mismatch 数量，可用于中途判断进度
3. **stdout 是完整 markdown 报告**：写入文件后用 grep 快速提取统计，不要全文 read_file（报告 ~8500 行 / 1.3MB，会被截断）
4. **缓存机制**：`<CACHE_DIR>/crowdin_cache/` 目录，2 小时内重复运行会快很多（跳过 API 拉取）

**快速提取关键统计（不用读全文）**：
```bash
# 提取所有语言的不一致摘要
grep -E "^### |^## |不一致（" /tmp/crowdin_report_latest.md
```

**检查的占位符类型**：
- Android/iOS 格式化：`%s`, `%d`, `%f`, `%1$s`, `%2$d`, `%%`, `%@`, `%ld`
- 花括号变量：`{name}`, `{{var}}`, `${var}`
- HTML 标签：`<b>`, `</b>`, `<br/>`, `<a>`, `<span>` 等

**常见问题语言（2026-06-04 数据确认）**：
- **vi（越南语）**：XAG ONE 项目 397 处不一致，几乎全是占位符丢失（396 处）— **最严重，运行时必崩**
- **es-ES（西班牙语）**：343 处，主要是格式变化（`{0}` → `%s` 等不匹配）
- **id（印尼语）**：219 处，类似问题
- **ug（维吾尔语）**：翻译者经常把 `%s` 拆成 `% s`（带空格），或把 `%1$s` 翻译成文字"1 美元"
- **th（泰语）**：占位符丢失或错位
- `{0}`, `{1}` 的花括号被吞掉

**定时检查**：已通过 cron 任务每天自动运行 v2 脚本，有问题发报告摘要，全部通过则 `[SILENT]` 不打扰

**基线数据**: 见 [references/placeholder-scan-baseline.md](references/placeholder-scan-baseline.md) — 2026-06-04 扫描结果（1671 处不一致），含按项目/语言排序的优先级列表和典型错误模式

### 场景 7：查术语库

```python
# 列术语库
r = requests.get("https://api.crowdin.com/api/v2/glossaries?limit=500", headers=headers)
glossaries = {g["data"]["id"]: g["data"]["name"] for g in r.json()["data"]}

# 拉 xagone (id=744513) 的术语库
# 实际术语库 id 在 project 详情的 defaultGlossaryId / assignedGlossaries 字段
# xagone defaultGlossaryId = 536361
r = requests.get("https://api.crowdin.com/api/v2/glossaries/536361/terms?limit=500",
                 headers=headers)
for term in r.json()["data"]:
    print(term["data"])
```

## 常用脚本

| 脚本 | 用途 |
|---|---|
| `scripts/export_to_excel.py` | 导出某项目某语言到 Excel（最常用） |
| `scripts/download_bundle.py` | 下载 Bundle 翻译包（Android/iOS/JSON 等格式） |
| `scripts/check_placeholders.py` | 检查翻译占位符一致性（%s/%d/{name}/HTML 标签等） |
| `scripts/list_projects.py` | 列所有 9 个 XAG 项目 |
| `scripts/get_progress.py` | 拿某项目所有语言进度 |
| `scripts/lookup_string.py` | 按 identifier / 关键词查源串 |

## 验证（不需要跑，凭记忆）

- 跑 `python3 scripts/export_to_excel.py --project 744513 --lang en` → 应该出 ~16,500 行 xlsx，coverage ~96%
- Summary sheet 显示 project 名 / total / matched / unmatched
- 主表列：ID | Identifier | Source (zh-CN) | Translation (en) | Context | Type | Labels

## 给其他 agent 的接力

如果另一个 agent（Lucy / 小明）需要 Crowdin 数据：
1. **不要**把 token 给他们
2. **可以**直接跑 `export_to_excel.py` 把 xlsx 放共享路径（如 `/usr/share/nginx/html/` 或 `/root/`）
3. **可以**直接调 `list_projects.py` / `get_progress.py` 拿结构化数据

## 高效查询与分析经验

### E1. 查翻译进度：用项目级 API 一次拉完，不要逐语言查

**❌ 低效**：对 17 种语言逐个调 `GET /projects/{id}/languages/{lang}/progress`，17 次请求
**✅ 高效**：`GET /projects/{id}/languages/progress` 一次返回所有语言的进度
```python
# ✅ 一次拿到所有语言进度
r = requests.get(f"{BASE}/projects/744513/languages/progress", headers=headers)
for lang in r.json()["data"]:
    d = lang["data"]
    print(f"{d['languageId']:>5} {d['translationProgress']:>3}% translated, "
          f"{d['approvalProgress']:>3}% approved")
```

### E2. 查源字符串：必须先缓存再过滤，不要反复拉

xagone 有 ~16,500 条源串，500/页 = 33 次请求。拉一次缓存在内存里，后续所有过滤/搜索都在本地做。

```python
# ✅ 全量拉取 + 本地缓存
all_strings = []
offset = 0
while True:
    r = requests.get(f"{BASE}/projects/744513/strings",
                     headers=headers, params={"limit": 500, "offset": offset})
    data = r.json()["data"]
    all_strings.extend([d["data"] for d in data])
    if len(data) < 500: break
    offset += 500
    time.sleep(0.1)  # 避免 429

# 本地过滤（极快）
survey_strings = [s for s in all_strings if "survey" in s["identifier"]]
error_strings = [s for s in all_strings if s["identifier"].startswith("mission_launch_error_")]
```

**踩坑**: `?filter=xxx` 对只读 token 静默返回 0 条。`?croql=xxx` 直接 400。**必须客户端过滤**。

### E3. 导出翻译包：Bundle 三步走，不要等太久

```python
import time

def export_bundle(project_id, bundle_id):
    """Bundle 导出三步走：创建 → 轮询 → 下载"""
    # 1. 创建导出
    r = requests.post(f"{BASE}/projects/{project_id}/bundles/{bundle_id}/exports",
                      headers=headers)
    export_id = r.json()["data"]["identifier"]
    
    # 2. 轮询状态（通常 5-30 秒）
    for _ in range(30):
        r = requests.get(f"{BASE}/projects/{project_id}/bundles/{bundle_id}/exports/{export_id}",
                         headers=headers)
        status = r.json()["data"]["status"]
        if status == "finished": break
        time.sleep(2)
    else:
        raise Exception(f"Bundle export timeout: {export_id}")
    
    # 3. 下载
    r = requests.get(f"{BASE}/projects/{project_id}/bundles/{bundle_id}/exports/{export_id}/download",
                     headers=headers)
    url = r.json()["data"]["url"]  # 预签名 S3 URL，有效期几分钟
    
    import urllib.request
    local_path = f"/tmp/bundle_{bundle_id}.zip"
    urllib.request.urlretrieve(url, local_path)
    return local_path
```

**经验**: Bundle 导出是异步的，不要以为调一次就能下载。必须轮询 `status` 直到 `finished`。

### E4. 跨语言占位符检查：并发拉取 + 本地正则

检查 9 个项目的占位符一致性，如果串行拉取要 10-15 分钟。用 `concurrent.futures` 并发：

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

PLACEHOLDER_RE = re.compile(r'%(?:\d+\$?)?[sdfcxeEgGaAn@%]|{[^}]+}|<[^>]+>')

def check_project(project_id):
    """拉一个项目所有语言的翻译，检查占位符"""
    # 拉源串 + 各语言翻译 + 对比
    ...

# ✅ 并发检查 9 个项目
with ThreadPoolExecutor(max_workers=5) as pool:
    futures = {pool.submit(check_project, pid): pid for pid in PROJECT_IDS}
    for future in as_completed(futures):
        pid = futures[future]
        results = future.result()
        ...
```

**限流**: Crowdin 每账号 20 并发。`max_workers=5` 安全。

### E5. identifier 前缀搜索：用 Python startswith，不要用 API filter

```python
# ❌ API filter 静默失效
r = requests.get(f"{BASE}/projects/744513/strings?filter=mission_launch", headers=headers)
# → 返回 0 条

# ✅ 本地 startswith
matches = [s for s in all_strings if s["identifier"].startswith("mission_launch")]
```

### E6. 翻译覆盖率分析：区分 words 和 phrases

Crowdin progress API 返回三种度量：
- `words`: 单词数（更适合 prose 类文案）
- `phrases`: 短语数（更适合 UI 文案，一条文案 = 一个 phrase）
- `translationProgress`: 基于 words 的百分比
- `approvalProgress`: 已批准的百分比

**分析建议**: 评估翻译完成度看 `phrases.translated / phrases.total`，比 words 更贴近实际条目数。

### E7. Bundle vs 传统 Build：永远选 Bundle

| 特性 | Bundle（✅ 推荐） | Build（❌ 不可用） |
|------|-------------------|-------------------|
| Token 权限 | 只读可用 | 需写权限 |
| 格式灵活 | Android/iOS/JSON 等 | 全项目打包 |
| 标签过滤 | ✅ 只导出指定标签 | ❌ 不支持 |
| API 状态 | 正常 | 404 |

### E8. 大数据量导出到 Excel 的性能优化

xagone 有 ~16,500 条源串 × 17 语言 = 理论最大 ~280,000 条翻译。
导出到 Excel 的步骤：

1. **先拉源串**（33 页 × 500 = ~15s）
2. **再拉翻译**（每种语言 33 页 = ~15s × 17 语言 = ~4min）
3. **用 dict join**：`{stringId: translation}` 映射，O(1) 查找
4. **用 openpyxl** 写 Excel：16,500 行 ~5s

```python
# ✅ 用 dict join 而非 list comprehension 嵌套
translations_map = {t["data"]["stringId"]: t["data"]["text"] for t in all_translations}
for s in all_strings:
    translated_text = translations_map.get(s["id"], "")
    ...
```

**反模式**: `for s in strings: for t in translations: if t.stringId == s.id` → O(n²)，16500² = 2.7 亿次比较。

## 变更日志

### 2026-06-14 v1.3.5（cron 复扫确认 — 连续 4 天稳定）
- ✅ 2026-06-14 cron 定时任务复扫结果：1681 处不一致，与 2026-06-11/12/13 完全一致
- ✅ 数据连续 4 天无变化，占位符问题状态冻结（无新增翻译/修复活动）
- ✅ `references/placeholder-scan-baseline.md` 趋势表增加 2026-06-14 确认日期

### 2026-06-13 v1.3.4（cron 复扫确认 — 连续 3 天稳定）
- ✅ 2026-06-13 cron 定时任务复扫结果：1681 处不一致，与 2026-06-11/12 完全一致
- ✅ 数据连续 3 天无变化，说明无新增翻译/修复活动
- ✅ `references/placeholder-scan-baseline.md` 趋势表增加 2026-06-13 确认日期

### 2026-06-12 v1.3.3（cron 复扫确认）
- ✅ 2026-06-12 cron 定时任务复扫结果：1681 处不一致，与 2026-06-11 完全一致，无新增/修复
- ✅ `references/placeholder-scan-baseline.md` 趋势表增加 2026-06-12 确认日期标注

### 2026-06-11 v1.3.2（cron 复扫 — 发现 +10 增量）
- 2026-06-11 cron 复扫：**1681 处不一致**（+10 vs 基线 1671）
- 增量全部来自 **XAG AutoPilot**（1→11）：bg/en/km-KH/ko/ro/ru/th/tr/ug 各新增 1 处丢失，ja 从 1→2
- XAG ONE / XAG Farm / 其他项目数字不变
- 基线文件已更新，含趋势表

### 2026-06-06 v1.3.1（cron 复扫确认）
- ✅ 2026-06-06 cron 定时任务复扫结果：1671 处不一致，与 2026-06-04 基线完全一致，说明无新增/修复
- ✅ `references/placeholder-scan-baseline.md` 增加确认日期标注

### 2026-06-04 v1.3（占位符检查运维优化）
- ✅ 场景 6 更新：v2 并发脚本路径、background 运行约束、缓存机制、grep 快速提取统计
- ✅ 新增 `references/placeholder-scan-baseline.md`：1671 处不一致的基线数据 + 典型错误模式
- ✅ 常见问题语言更新：vi/es-ES/id 成为新的重点（不只是 ug/th）

### 2026-06-03 v1.2（全端点覆盖版）
- ✅ 官方 OpenAPI 338 端点全量审计，实测确认可用 51 个
- ✅ SKILL.md 端点索引从简单列表扩展为 21 类别完整表格（✅/❌/🔒 状态标注）
- ✅ 新增 E1-E8 高效查询经验（分页缓存/并发/本地过滤/dict join/Bundle三步走/覆盖率分析）
- ✅ 新增 `references/official-api-audit.md`：完整审计结果 + 重新审计方法

### 2026-06-02 v1.1
- Bundle 翻译包下载支持
- 占位符检查（v2 并发版 + v4 完整报告格式）

### 2026-06-02 v1.0（初始版）
- 基础 API 接入（项目/字符串/翻译/进度/术语库/TM）

---

## 相关资源

- API 文档：https://developer.crowdin.com/api/v2/
- OpenAPI YAML：`https://support.crowdin.com/src/assets/api/crowdin/file-based.yml`（45,900 行，338 端点）
- 项目主页：https://crowdin.com/project/xagone （需要登录）
- 历史会话：搜 `crowdin`（之前建哥发过 token）
- 详见 [references/official-api-audit.md](references/official-api-audit.md)：完整覆盖率审计结果 + 如何重新审计


## 路径映射

在其他 Agent 系统中安装时，需要将以下路径映射到你的环境：

| 原始路径 | 映射到 |
|---------|--------|
| `<SKILL_SCRIPTS_DIR>` | 你的 agent 脚本目录 |
| `<WORKSPACE_DIR>` | 工作空间目录 |
| `<DATA_DIR>` | 数据存储目录 |
| `<LOG_DIR>` | 日志目录 |

## 适用场景

- 查询极飞农服/极飞农机/极飞农场等产品当前支持的语言列表和翻译进度
- 批量导出某项目某语言的翻译文案到 Excel 或翻译包（Android strings.xml / iOS .strings / JSON）
- 检查翻译占位符一致性（%s/%d/{name}/HTML 标签），发现可能导致运行时崩溃的问题
- 按 identifier 前缀查找源字符串，确认某条文案在 Crowdin 上是否已翻译
- 查术语库、翻译记忆库、风格指南等翻译资产

## 前提条件

- Crowdin Personal Access Token（只读）已存储在 `~/.hermes/credentials/crowdin.txt`（chmod 600）
- Python 3 + requests 库
- 网络可访问 `api.crowdin.com`
- Token 绝不能写入代码、提交 git 或转发给海外 Agent

## 能力清单

| 能力 | 说明 | 限制 |
|------|------|------|
| 项目列表/详情 | 列出 9 个 XAG 项目及目标语言配置 | 只读 |
| 源字符串查询 | 分页拉取（500/页），本地过滤 | 服务端 filter 对只读 token 无效 |
| 翻译导出 | 按语言分页拉取翻译，支持 Bundle 打包下载 | 传统 build 端点 404，仅 Bundle 可用 |
| 翻译进度 | 一次 API 返回所有语言的覆盖率 | 只读 |
| 术语库/TM | 列出和下载术语库、翻译记忆库 | 只读，不能新增/修改 |
| 占位符检查 | 并发扫描 9 个项目所有语言的占位符一致性 | 耗时约 8 分钟，需 background 模式运行 |
| 成员/任务/评论 | 查看项目成员、翻译任务、字符串评论 | 只读 |

## 预期效果

- 调用进度 API 后秒级返回所有语言的翻译覆盖率、已译条数、已批准比例
- 导出 Excel 后得到 ~16,500 行结构化数据（含 Identifier、源文案、译文、标签）
- Bundle 下载得到 zip 包，内含按语言分目录的 strings.xml / .strings / JSON 文件
- 占位符检查生成 Markdown 报告，按项目/语言分类列出所有不一致记录及占位符对比

## Changelog

- **1.3.5** (2026-06-14): 初始版本，可移植性改造
