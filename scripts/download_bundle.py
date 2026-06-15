#!/usr/bin/env python3
"""从 Crowdin 下载 Bundle 翻译包（Android strings.xml / iOS Localizable.strings / JSON 等）

用法:
  # 列出所有 bundles
  python3 download_bundle.py --project 744513 --list

  # 下载 Android 包（bundle id=10，所有语言）
  python3 download_bundle.py --project 744513 --bundle 10

  # 下载 iOS 包
  python3 download_bundle.py --project 744513 --bundle 12

  # 指定输出路径
  python3 download_bundle.py --project 744513 --bundle 10 --out /tmp/android_translations.zip

  # 解压到指定目录
  python3 download_bundle.py --project 744513 --bundle 10 --extract /tmp/translations/
"""
import argparse, json, os, sys, time, zipfile, io
import requests

sys.path.insert(0, os.path.dirname(__file__))

def get_token():
    return open(os.path.expanduser("~/.hermes/credentials/crowdin.txt")).read().strip()

def headers():
    return {"Authorization": "Bearer " + get_token(), "Content-Type": "application/json"}

def list_bundles(project_id):
    """列出项目所有 bundles"""
    url = f"https://api.crowdin.com/api/v2/projects/{project_id}/bundles"
    offset = 0
    all_bundles = []
    while True:
        r = requests.get(url, headers=headers(), params={"limit": 50, "offset": offset})
        if r.status_code != 200:
            print(f"❌ HTTP {r.status_code}: {r.text[:200]}", file=sys.stderr)
            sys.exit(1)
        data = r.json()["data"]
        all_bundles.extend([d["data"] for d in data])
        if len(data) < 50:
            break
        offset += 50
    return all_bundles

def create_export(project_id, bundle_id):
    """创建 bundle 导出任务"""
    url = f"https://api.crowdin.com/api/v2/projects/{project_id}/bundles/{bundle_id}/exports"
    r = requests.post(url, headers=headers(), json={})
    if r.status_code not in (200, 202):
        print(f"❌ 创建导出失败: HTTP {r.status_code}: {r.text[:300]}", file=sys.stderr)
        sys.exit(1)
    return r.json()["data"]

def check_export(project_id, bundle_id, export_id):
    """查询导出状态"""
    url = f"https://api.crowdin.com/api/v2/projects/{project_id}/bundles/{bundle_id}/exports/{export_id}"
    r = requests.get(url, headers=headers())
    return r.json()["data"]

def get_download_url(project_id, bundle_id, export_id):
    """获取下载链接"""
    url = f"https://api.crowdin.com/api/v2/projects/{project_id}/bundles/{bundle_id}/exports/{export_id}/download"
    r = requests.get(url, headers=headers())
    if r.status_code != 200:
        print(f"❌ 获取下载链接失败: HTTP {r.status_code}: {r.text[:300]}", file=sys.stderr)
        sys.exit(1)
    return r.json()["data"]["url"]

def download_file(url, output_path):
    """下载文件"""
    r = requests.get(url)
    if r.status_code != 200:
        print(f"❌ 下载失败: HTTP {r.status_code}", file=sys.stderr)
        sys.exit(1)
    with open(output_path, "wb") as f:
        f.write(r.content)
    return len(r.content)

def main():
    parser = argparse.ArgumentParser(description="Crowdin Bundle 翻译包下载")
    parser.add_argument("--project", type=int, default=744513, help="项目 ID（默认 xagone=744513）")
    parser.add_argument("--bundle", type=int, help="Bundle ID")
    parser.add_argument("--list", action="store_true", help="列出所有 bundles")
    parser.add_argument("--out", help="输出 zip 文件路径")
    parser.add_argument("--extract", help="解压到指定目录")
    args = parser.parse_args()

    if args.list:
        bundles = list_bundles(args.project)
        print(f"项目 {args.project} 共 {len(bundles)} 个 Bundle：")
        print(f"{'ID':>5s}  {'名称':<35s}  {'格式':<25s}  {'导出模式'}")
        print("-" * 100)
        for b in bundles:
            print(f"{b['id']:>5d}  {b['name']:<35s}  {b['format']:<25s}  {b['exportPattern']}")
        return

    if not args.bundle:
        parser.print_help()
        return

    # 1. 创建导出
    print(f"📦 创建 Bundle {args.bundle} 导出任务...", file=sys.stderr)
    export = create_export(args.project, args.bundle)
    export_id = export["identifier"]
    print(f"   任务 ID: {export_id}", file=sys.stderr)

    # 2. 轮询等待完成
    max_wait = 120
    start = time.time()
    while time.time() - start < max_wait:
        status = check_export(args.project, args.bundle, export_id)
        if status["status"] == "finished":
            break
        if status["status"] in ("failed", "cancelled"):
            print(f"❌ 导出失败: {status['status']}", file=sys.stderr)
            sys.exit(1)
        print(f"   ⏳ {status['status']} ({status['progress']}%)...", file=sys.stderr)
        time.sleep(3)
    else:
        print(f"❌ 导出超时 ({max_wait}s)", file=sys.stderr)
        sys.exit(1)

    # 3. 获取下载链接
    print(f"✅ 导出完成，获取下载链接...", file=sys.stderr)
    dl_url = get_download_url(args.project, args.bundle, export_id)

    # 4. 下载
    out_path = args.out or f"/tmp/crowdin_bundle_{args.bundle}.zip"
    print(f"📥 下载中...", file=sys.stderr)
    size = download_file(dl_url, out_path)
    print(f"✅ 已保存: {out_path} ({size:,} bytes)", file=sys.stderr)

    # 5. 可选解压
    if args.extract:
        os.makedirs(args.extract, exist_ok=True)
        with zipfile.ZipFile(out_path) as zf:
            names = zf.namelist()
            zf.extractall(args.extract)
            print(f"📂 已解压 {len(names)} 个文件到: {args.extract}", file=sys.stderr)
            for n in sorted(names)[:10]:
                print(f"   {n}")
            if len(names) > 10:
                print(f"   ... 还有 {len(names)-10} 个")

    if not args.extract:
        # 显示 zip 内容
        with zipfile.ZipFile(out_path) as zf:
            names = sorted(zf.namelist())
            print(f"\n包含 {len(names)} 个文件：")
            for n in names:
                info = zf.getinfo(n)
                print(f"  {n:<50s} {info.file_size:>10,} bytes")

if __name__ == "__main__":
    main()
