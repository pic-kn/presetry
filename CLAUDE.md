## コミットメッセージのルール

コミットメッセージは必ず以下の形式で書くこと：

```
【プロジェクト】何を作っているかの説明（1行で簡潔に）
【課題】何の問題を解決したか
【解決】どう解決したか
【指示】ユーザーからのプロンプト（抽象的な言葉）→Claudeが具体化した内容
【手作業】ユーザーが自分で行った手動作業（なければ「なし」）
```

### 具体例

```
【プロジェクト】GitHubのコードをpushすると毎日20時にXへ自動投稿されるシステム【課題】bashのgrepでUnicodeエスケープが機能せずデータが入らない【解決】Python3でフィールド抽出する方式に変更【指示】「データが入らない」→post_to_notion.ymlのbash grep抽出をPython3のreモジュールに書き直せ【手作業】なし
```

### ルール

- `【】`の中の改行は不可。各項目は1行で書くこと
- 5つのタグがすべて存在する場合のみNotionに自動蓄積される（手作業は「なし」でも可）
- 【指示】は「ユーザーの言葉（抽象）→Claudeが具体化した内容」の形式で書くこと
- この形式に従うことで、GitHub ActionsがNotionに自動蓄積し、毎日20:00 JSTにXへ自動投稿される

## ワークフロー構成

| ファイル | トリガー | 役割 |
|---|---|---|
| `post_to_notion.yml` | mainへのpush | コミットメッセージを解析してNotionに登録 |
| `post_to_x.yml` | 毎日20:00 JST | NotionのReadyアイテムをXに投稿 |
| `sync_to_repos.yml` | mainへのpush（CLAUDE.mdまたはpost_to_notion.yml変更時） | presetryとcolor-memoへ自動同期 |

## 連携リポジトリ

- `pic-kn/presetry`
- `pic-kn/color-memo`

上記リポジトリはこのリポジトリと同じNotionデータベースを共有しており、`sync_to_repos.yml` によってCLAUDE.mdとpost_to_notion.ymlが自動的に最新版に保たれる。
