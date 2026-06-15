"""Crowdin API shared helpers (read-only)."""
import os
import requests
import time

TOKEN_PATH = os.path.expanduser("~/.hermes/credentials/crowdin.txt")
BASE = "https://api.crowdin.com/api/v2"

def get_token():
    """Read API token from secure file. Strips whitespace."""
    return open(TOKEN_PATH).read().strip()

def headers():
    return {"Authorization": f"Bearer {get_token()}"}

def get(path, params=None, retries=3):
    """GET with retries and 0.1s sleep to be polite."""
    for i in range(retries):
        r = requests.get(BASE + path, headers=headers(), params=params, timeout=60)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (404, 403):
            return None
        time.sleep(0.2 * (i + 1))
    r.raise_for_status()

def paginate(path, params=None, limit=500):
    """Yield all items from a paginated Crowdin endpoint."""
    params = dict(params or {})
    params["limit"] = limit
    offset = 0
    while True:
        params["offset"] = offset
        data = get(path, params)
        if not data or not data.get("data"):
            return
        for item in data["data"]:
            yield item
        if len(data["data"]) < limit:
            return
        offset += limit

# Known XAG project IDs (snapshot 2026-06-02)
XAG_PROJECTS = {
    744289: ("nongchang", "XAG Farm 极飞农场"),
    744297: ("xapc", "XAG AutoPilot 极飞农机"),
    744303: ("XCARETOOL", "Xcare Tool 极加检修"),
    744513: ("xagone", "XAG ONE 极飞农服"),
    746881: ("testxag001", "测试项目 001"),
    748629: ("xagservice", "XAG Service 极飞服务"),
    773277: ("xag-one-management-platform", "XAG One Management Platform 极飞农服管理平台"),
    806874: ("xag-go", "XAG Go 极飞无人车"),
    874794: ("XAGMes", "XAG Mes 极飞生产执行系统"),
}
