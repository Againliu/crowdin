# Crowdin API 覆盖率审计（2026-06-03）

> 官方 API 共 338 个端点，29 个类别。我们只读 token 实测确认可用 51 个。

## 官方 OpenAPI 规范获取

```bash
# 下载完整 OpenAPI 3.0 YAML（45,900 行）
curl -sL 'https://support.crowdin.com/src/assets/api/crowdin/file-based.yml' -o /tmp/crowdin_openapi.yml

# 解析端点列表
python3 -c "
import yaml
from collections import defaultdict
with open('/tmp/crowdin_openapi.yml') as f:
    spec = yaml.safe_load(f)
by_tag = defaultdict(list)
for path, methods in spec['paths'].items():
    for m, d in methods.items():
        if m in ('get','post','put','delete','patch'):
            for t in d.get('tags', ['Untagged']):
                by_tag[t].append((m.upper(), path, d.get('summary','')))
for tag in sorted(by_tag):
    print(f'{tag}: {len(by_tag[tag])} endpoints')
"
```

## 审计结果汇总

| 类别 | 官方端点 | 我们可用(GET) | 状态 |
|------|---------|-------------|------|
| Projects | 17 | 2 | ✅ 核心可用 |
| Source Files | 24 | 3 (branches only) | ❌ files/dirs 404 |
| Source Strings | 6 | 3 | ✅ 核心可用 |
| String/Asset Translations | 19 | 7 | ✅ 核心可用 |
| Translation Status | 9 | 5 | ✅ 核心可用 |
| Translations (导出) | 28 | 8 | ✅ Bundle 可用 |
| Labels | 9 | 2 | ✅ |
| Glossaries | 21 | 7 | ✅ |
| Translation Memory | 20 | 7 | ✅ |
| Languages | 5 | 2 | ✅ |
| Users | 7 | 3 | ✅ |
| Tasks | 19 | 6 | ✅ |
| Reports | 19 | 5 | ⚠️ 需写token生成 |
| Issues | 2 | 1 | ✅ |
| Comments | 7 | 2 | ✅ |
| Screenshots | 13 | 4 | ✅ |
| Dictionaries | 2 | 1 | ✅ |
| Machine Translation | 3 | 2 | ✅ |
| Style Guides | 5 | 2 | ✅ |
| Storage | 4 | 2 | ⚠️ 未验证 |
| AI | 48 | ~30 | 🔵 新功能，待探索 |
| AI Gateway | 5 | 5 | 🔵 |
| Webhooks | 5 | 2 | 🔵 |
| Org Webhooks | 5 | 2 | 🔵 |
| Distributions | 7 | 3 | 🔵 |
| Applications | 10 | 5 | 🔵 |
| Integrations | 15 | 10 | 🔵 |
| Notifications | 2 | 0 | 🔒 全写 |
| Security Logs | 2 | 2 | 🔵 |

## 实测端点状态（2026-06-03）

| 端点 | 状态 | 备注 |
|------|------|------|
| GET /languages | ✅ 200 | 5 items (limit=5) |
| GET /projects/{id}/languages/progress | ✅ 200 | 16 语言全部返回 |
| GET /projects/{id}/members | ✅ 200 | |
| GET /projects/{id}/tasks | ✅ 200 | |
| GET /projects/{id}/comments | ✅ 200 | 1 item |
| GET /projects/{id}/screenshots | ✅ 200 | 0 items |
| GET /projects/{id}/dictionaries | ✅ 200 | 16 语言条目 |
| GET /projects/{id}/pre-translations | ✅ 200 | 0 items |
| GET /projects/{id}/bundles/{id} | ✅ 200 | 18 字段 |
| GET /projects/{id}/branches/{id}/languages/progress | ✅ 200 | |
| GET /glossaries/{id} | ✅ 200 | |
| GET /tms | ✅ 200 | 7 TMs |
| GET /mts | ✅ 200 | 2 MT engines |
| GET /user/tasks | ✅ 200 | |
| GET /style-guides | ✅ 200 | |
| GET /projects/{id}/issues | ✅ 200 | 0 items |
| GET /projects/{id}/qa-checks | 💥 timeout | 大数据量超时(>10s) |
| GET /projects/{id}/votes | ❌ 400 | 必须传 translationId |
| GET /projects/{id}/approvals | ❌ 400 | 必须传 translationId |
| GET /projects/{id}/translations | ❌ 400 | 必须传 languageId |
| GET /projects/{id}/files | ❌ 404 | token 不可见 |
| GET /projects/{id}/directories | ❌ 404 | token 不可见 |
| GET /projects/{id}/bundles/{id}/files | ❌ 404 | |

## 如何重新审计

1. 重新下载 OpenAPI YAML
2. 解析出所有 GET 端点
3. 逐个调一遍（带 token），记录 200/400/403/404
4. 对比本文件和 SKILL.md 端点索引表
