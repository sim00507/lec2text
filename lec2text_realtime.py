import os
import subprocess
import whisper
import math
from pydub import AudioSegment

# 🔧 세그먼트 분할 설정
SEGMENT_DURATION = 15  # 초 단위

# 🎞 mp4 파일 목록 가져오기
mp4_files = [f for f in os.listdir() if f.endswith(".mp4")]
if not mp4_files:
    print("❌ 현재 디렉터리에 .mp4 파일이 없습니다.")
    exit()

print("변환할 .mp4 파일을 선택하세요:")
for i, file in enumerate(mp4_files):
    print(f"{i + 1}. {file}")
choice = int(input("번호 입력: ")) - 1

input_video = mp4_files[choice]
base_name = os.path.splitext(input_video)[0]
save_dir = os.path.join("result", base_name)
os.makedirs(save_dir, exist_ok=True)

output_mp3 = os.path.join(save_dir, f"{base_name}.mp3")
output_txt = os.path.join(save_dir, f"{base_name}.txt")

# 🔄 MP4 → MP3 변환
print(f"\n🔄 '{input_video}' → '{output_mp3}' 변환 중...")
subprocess.run([
    "ffmpeg", "-i", input_video, "-q:a", "0", "-map", "a", output_mp3
], check=True)

# 🧠 Whisper 모델 로드 (GPU)
print("🧠 Whisper 모델 로딩 중 (GPU)...")
model = whisper.load_model("medium", device="cuda")

# 🚀 방식 선택
print("\n원하는 변환 방식을 선택하세요:")
print("1. 전체 파일을 한 번에 처리 (transcribe)")
print("2. 15초 단위 세그먼트로 나눠서 처리 (진행 상황 확인 가능)")
mode = input("번호 입력: ")

# ===================================
# ✅ MODE 1: 한 번에 전체 변환
# ===================================
if mode == "1":
    print("🎧 음성 텍스트화 진행 중...")
    result = model.transcribe(output_mp3, language="ko", fp16=True)
    
    for i, segment in enumerate(result["segments"]):
        print(f"[{i+1}] ({segment['start']:.2f}s ~ {segment['end']:.2f}s): {segment['text']}")

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(result["text"])

# ===================================
# ✅ MODE 2: 세그먼트 실시간 출력
# ===================================
elif mode == "2":
    print("✂️ 오디오 분할 및 실시간 출력 시작...\n")
    audio = AudioSegment.from_file(output_mp3)
    total_duration = math.ceil(len(audio) / 1000)
    full_text = ""

    for i, start in enumerate(range(0, total_duration, SEGMENT_DURATION)):
        end = min(start + SEGMENT_DURATION, total_duration)
        segment_audio = audio[start * 1000:end * 1000]
        temp_path = os.path.join(save_dir, f"temp_{i}.mp3")
        segment_audio.export(temp_path, format="mp3")

        result = model.transcribe(temp_path, language="ko", fp16=True)
        print(f"[{i+1}] ({start}s ~ {end}s): {result['text']}")
        full_text += result["text"] + "\n"

        os.remove(temp_path)

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write(full_text)

else:
    print("❌ 잘못된 입력입니다. 프로그램을 종료합니다.")
    exit()

print(f"\n✅ 변환 완료! 결과 텍스트는 '{output_txt}'에 저장되었습니다.")
