import os
import subprocess
import whisper

# 현재 디렉터리에서 mp4 파일 목록 가져오기
mp4_files = [f for f in os.listdir() if f.endswith(".mp4")]

# mp4 파일이 없으면 종료
if not mp4_files:
    print("❌ 현재 디렉터리에 .mp4 파일이 없습니다.")
    exit()

# 목록 보여주기
print("🎞 변환할 .mp4 파일을 선택하세요:")
for i, file in enumerate(mp4_files):
    print(f"{i + 1}. {file}")

# 사용자 선택
choice = int(input("번호 입력: ")) - 1
input_video = mp4_files[choice]

# 파일명에서 확장자 제거
base_name = os.path.splitext(input_video)[0]

# 저장할 디렉터리 생성
save_dir = os.path.join("result", base_name)
os.makedirs(save_dir, exist_ok=True)

# 자동 생성 파일명
# output_audio = f"{base_name}.mp3"
# output_text = f"{base_name}.txt"
output_audio = os.path.join(save_dir, f"{base_name}.mp3")
output_text = os.path.join(save_dir, f"{base_name}.txt")



# 1. MP4 → MP3 변환
print(f"\n🔄 '{input_video}' → '{output_audio}' 변환 중...")
subprocess.run([
    "ffmpeg", "-i", input_video, "-q:a", "0", "-map", "a", output_audio
], check=True)

# 2. Whisper 모델 로드 (GPU)
print("🧠 Whisper 모델 로딩 중 (GPU)...")
model = whisper.load_model("medium", device="cuda")

# 3. 음성 인식 (Whisper GPU + fp16)
print("🎧 음성 텍스트화 진행 중(세그먼트 출력 중)...")
result = model.transcribe(output_audio, language="ko", fp16=True)

# 세그먼트별로 출력
for i, segment in enumerate(result["segments"]):
    print(f"[{i+1}] ({segment['start']:.2f}s ~ {segment['end']:.2f}s): {segment['text']}")

# 4. 텍스트 저장
with open(output_text, "w", encoding="utf-8") as f:
    f.write(result["text"])

print(f"\n✅ 변환 완료! 결과 텍스트는 '{output_text}'에 저장되었습니다.")
