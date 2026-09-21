# 全体像（2系統のコピー）

```
┌─────────────────────────────┐
│ Container                   │ ← ローカル
│ /var/dlt/pipelines/         │
│   source_to_analytics/      │
│     state.json              │ ← 作業用キャッシュ（消えてよい）
└─────────────┬───────────────┘
              │ run() のたびに同期
              ▼
┌─────────────────────────────┐
│ Analytics DB                │  ← 永続
│ raw._dlt_pipeline_state     │  ← 正本候補
│ raw._dlt_loads              │  ← 「成功した load」判定に使う
│ raw._dlt_version            │  ← schema 版
└─────────────────────────────┘
```

識別キーは次の3つ。

- pipeline_name（いまは source_to_analytics）
- destination の接続先（analytics DB）
- dataset_name（raw）

## 1. DB に「記録する」流れ（Write）
pipeline.run(source) の後半で、普通のデータと同じく load package の一部として state も載せるイメージ。

- extract 中に incremental が last_value（cursor）を state に書く
- normalize → load で、業務テーブルと一緒に
    - raw._dlt_pipeline_state に state の JSON blob
    - raw._dlt_loads に load 成否が入る
- 同時にローカル state.json も更新される

「state 専用の INSERT を自分で書く」必要はなく、load が成功した時点で destination にも残る設計。

## 2. DB から「使う」流れ（Restore）

run() の いちばん最初（extract の前）に入る。

```py
# dlt.pipeline
# sync state with destination
if (
    self.config.restore_from_destination
    and not self.dev_mode
    and not self._state_restored
    and (self._destination or destination)
):
    self._sync_destination(destination, staging, dataset_name)
    # sync only once
    self._state_restored = True
```

条件の意味:

- restore_from_destination=True: デフォルト ON（設定クラスで明記）
- not dev_mode: 開発用フルリセットモードではない
- not _state_restored: このプロセスでまだ sync していない
- destination がある: どこから戻すか分かる

sync の中身

- ローカル state を読む（無い／空なら version が若い or 新規扱い）
- _restore_state_from_destination() で DB から最新 state を取る
- remote の _state_version ≥ local なら remote を採用し、ローカルに書き戻す
- そのあと incremental 付き extract が、復元された last_value を使う

DB からの読み方は、だいたい次の SQL です（get_stored_state）。

```sql
SELECT ... FROM raw._dlt_pipeline_state AS s
JOIN raw._dlt_loads AS l ON l.load_id = s._dlt_load_id
WHERE s.pipeline_name = 'source_to_analytics'
  AND l.status = 0          -- 成功した load だけ
ORDER BY load_id DESC
LIMIT 1
```
つまり「テーブルに載っている最新行」ではなく、成功した load に紐づく最新 state です。失敗した load の state は採用しない。

## 3. なぜ「消しても増分が続く」のか（1本のタイムライン）

```txt
[前回成功]
  extract(cursor更新) → load → DBに state v6 + ローカル state.json

[Container / state.json 削除]
  ローカル無し、DB に v6 は残る

[今回 run]
  ① restore_from_destination → DB の v6 を読む
  ② ローカル state.json を v6 相当で作り直す
  ③ extract は updated_at >= 復元した last_value
  ④ load → DB に v7、ローカルも v7
```

## 4. デフォルトがどこに書いてあるか
設定クラス:

```
restore_from_destination: bool = True
（dlt.pipeline.configuration.PipelineConfiguration）
```

意図的に切るなら .dlt/config.toml などで restore_from_destination = false。
