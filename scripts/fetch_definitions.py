#!/usr/bin/env python3
# v1.1
"""
セッション開始時にNotionの定義DBからデータを取得してCLAUDE.mdを更新するスクリプト
"""
import os
import re
import requests

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
NOTION_DEFINITION_DB_ID = os.environ.get("NOTION_DEFINITION_DB_ID")

if not NOTION_API_KEY or not NOTION_DEFINITION_DB_ID:
    print("NOTION_API_KEY または NOTION_DEFINITION_DB_ID が未設定のためスキップします")
    exit(0)

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Notionから定義を全件取得
res = requests.post(
    f"https://api.notion.com/v1/databases/{NOTION_DEFINITION_DB_ID}/query",
    headers=headers,
    json={"sorts": [{"property": "定義名", "direction": "ascending"}]}
)

if res.status_code != 200:
    print(f"Notion取得失敗: {res.text}")
    exit(1)

pages = res.json().get("results", [])
definitions = []

for page in pages:
    props = page["properties"]

    def get_text(prop_name):
        prop = props.get(prop_name, {})
        if prop.get("title"):
            return prop["title"][0]["text"]["content"] if prop["title"] else ""
        if prop.get("rich_text"):
            return prop["rich_text"][0]["text"]["content"] if prop["rich_text"] else ""
        if prop.get("select"):
            return prop["select"]["name"] if prop["select"] else ""
        return ""

    name = get_text("定義名")
    category = get_text("カテゴリ")
    scope = get_text("スコープ") or "共通"
    content = get_text("内容")
    example = get_text("事例")

    if name:
        definitions.append({
            "name": name,
            "category": category,
            "scope": scope,
            "content": content,
            "example": example
        })

print(f"{len(definitions)}件の定義を取得")

# CLAUDE.mdの定義テーブルを更新
claude_path = os.path.join(os.path.dirname(__file__), "..", "CLAUDE.md")
with open(claude_path, "r") as f:
    claude_text = f.read()

# 新しいテーブルを生成
header = "| 定義名 | カテゴリ | スコープ | 内容 | 事例 |"
separator = "|---|---|---|---|---|"
rows = [f"| {d['name']} | {d['category']} | {d['scope']} | {d['content']} | {d['example']} |"
        for d in definitions]
new_table = "\n".join([header, separator] + rows)

# 定義一覧セクションのテーブルを置換
new_text = re.sub(
    r"(### 定義一覧\n\n)\|.*?\n\|[-| ]+\|\n(?:\|.*?\n)*",
    lambda m: m.group(1) + new_table + "\n",
    claude_text,
    flags=re.DOTALL
)

if new_text == claude_text:
    print("変更なし")
else:
    with open(claude_path, "w") as f:
        f.write(new_text)
    print("CLAUDE.mdの定義テーブルを更新しました")
