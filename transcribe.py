import os
import whisper

# 出力ファイル名
output_file = "transcription_output.txt"

# 音声ファイルが入っているサブディレクトリのパス
base_dir = "target"

# 話者ごとのファイルを指定（必要に応じて変更してください）
files = {
    "金子": os.path.join(base_dir, "1-masakazukaneko_0.flac"),
    "青山": os.path.join(base_dir, "2-aoyamayuria_0.flac"),
    "張":  os.path.join(base_dir, "3-cho9781_0.flac"),
    "岩下": os.path.join(base_dir, "4-ym_iwashita_0.flac"),
    "千原": os.path.join(base_dir, "5-tchihara_0.flac"),
}

model = whisper.load_model("medium")

all_segments = []

for speaker, file_path in files.items():
    print(f"処理中: {speaker}さんのファイル {file_path}")
    result = model.transcribe(file_path, language="ja")
    
    for seg in result["segments"]:
        all_segments.append({
            "speaker": speaker,
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"]
        })

# 開始時間順にソート
all_segments.sort(key=lambda x: x["start"])

# ファイル出力
with open(output_file, "w", encoding="utf-8") as f:
    for seg in all_segments:
        line = f"[{seg['start']:.2f}s][{seg['speaker']}] {seg['text']}\n"
        f.write(line)

print(f"\n✅ 文字起こし結果を {output_file} に保存しました。")