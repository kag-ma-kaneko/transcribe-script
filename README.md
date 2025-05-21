# Whisper Transcription Tool

Whisper を使って複数の音声ファイル（`.flac`, `.aac`）を並列に文字起こしする Python スクリプトです。  
話者ごとにファイルを分けて保存しておけば、時系列に並んだ発話ログを生成します。

---

## 🧩 特徴

- OpenAI Whisper を使用した高精度文字起こし
- `target/` フォルダ内の音声ファイルを一括処理
- スレッド並列処理による高速化
- 発言者名をファイル名から自動取得
- 出力は発話時刻順に並べられた 1 つのテキストファイル

---

## 📦 セットアップ

### 1. Poetry で仮想環境を構築

```bash
poetry install
```

Whisper をまだ追加していない場合は以下で追加：

```bash
poetry add git+https://github.com/openai/whisper.git
```

---

## 📁 音声ファイルの準備

- スクリプトと同じディレクトリに `target/` フォルダを作成してください。
- 話者ごとにファイル名をつけて `.flac` または `.aac` 形式で保存します。

例：

```
target/
├── kaneko.flac
├── aoyama.flac
└── iwashita.flac
```

---

## 🚀 使い方

```bash
poetry run python transcribe.py
```

### モデル指定（例：高精度モデル `large` を使用）

```bash
poetry run python transcribe.py --model large
```

---

## ⚙️ オプション

| オプション | 説明                    | デフォルト | 備考                                       |
| ---------- | ----------------------- | ---------- | ------------------------------------------ |
| `--model`  | 使用する Whisper モデル | `medium`   | `tiny`, `base`, `small`, `medium`, `large` |

---

## 📄 出力

文字起こし結果は `transcription_output.txt` に保存されます。  
例：

```
[0.53s][kaneko] おはようございます。
[1.82s][aoyama] はい、おはようございます。
[3.01s][iwashita] 今日の議題は...
```

---

## 🛠 推奨事項

- 音質を重視する場合は `.flac`（ロスレス形式）を使用してください。
- 長時間処理や精度重視の場合は `--model large` の使用を推奨します。
- スレッド数やファイル形式の対応を追加したい場合はスクリプトをご調整ください。

---

## 📘 ライセンス

[MIT License](LICENSE)

---

## 🙋 サポート

不明点や改善提案がある場合は Issue を立ててください。
