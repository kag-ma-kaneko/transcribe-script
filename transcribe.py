#!/usr/bin/env python3

import os
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


def is_valid_segment(text):
    normalized = text.strip()
    # 文字起こしのフィルタリング条件
    # 意味のない単語や定型句（完全一致）
    if normalized in {
        "ん", "うん", "えー", "あー", "ですね", "はい",
        "お疲れさまでした", "ありがとうございました", "ご視聴ありがとうございました"
    }:
        return False
    
    # 特定フレーズを含むもの（部分一致）
    if any(kw in normalized for kw in [
        "ご視聴ありがとうございました",
        "1、2、3、4",
        "1", "2", "3", "4",  # 数字単体
        "あー", "うーん", "えー"  # あいづち
    ]):
        return False
    
    return True

def remove_repetitive_segments(segments):
    filtered = []
    prev_text = None
    for seg in segments:
        current_text = seg["text"].strip()
        if current_text != prev_text:
            filtered.append(seg)
        prev_text = current_text
    return filtered

def transcribe_file(model_path, file_path):
    import whisper  # 各スレッドで確実にインポート
    model = whisper.load_model(model_path)
    speaker = os.path.splitext(os.path.basename(file_path))[0]
    result = model.transcribe(file_path, language="ja")

    # 連続重複フィルタを適用
    cleaned_segments = remove_repetitive_segments(result["segments"])

    return [
        {
            "speaker": speaker,
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"]
        }
        for seg in cleaned_segments
        if is_valid_segment(seg["text"])
    ]

def get_audio_files(directory, extensions=(".flac", ".aac")):
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith(extensions)
    ]

def save_transcription(segments, output_file):
    segments.sort(key=lambda x: x["start"])
    with open(output_file, "w", encoding="utf-8") as f:
        for seg in segments:
            f.write(f"[{seg['start']:.2f}s][{seg['speaker']}] {seg['text']}\n")

def main():
    # 引数処理（--model オプションを追加）
    parser = argparse.ArgumentParser(description="Whisperを使った音声ファイルの文字起こし")
    parser.add_argument("--model", default="medium", choices=["tiny", "base", "small", "medium", "large"],
                        help="Whisperモデルの種類（デフォルト: medium）")
    args = parser.parse_args()

    start_time = datetime.now()
    print(f"🕒 処理開始: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    audio_dir = "target"
    output_file = "transcription_output.txt"
    max_workers = 2  # 並列数（CPUコア数や性能に応じて調整）

    audio_files = get_audio_files(audio_dir)
    all_segments = []

    print(f"🔁 文字起こし開始（{max_workers} スレッド） - モデル: {args.model}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(transcribe_file, args.model, file_path): file_path
            for file_path in audio_files
        }

        for future in as_completed(futures):
            file_path = futures[future]
            try:
                segments = future.result()
                all_segments.extend(segments)
                print(f"✅ 完了: {file_path}")
            except Exception as e:
                print(f"❌ 失敗: {file_path} → {e}")

    save_transcription(all_segments, output_file)
    print(f"\n📄 出力完了: {output_file}")

    end_time = datetime.now()
    print(f"🕒 処理終了: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️ 所要時間: {str(end_time - start_time)}")

if __name__ == "__main__":
    main()
