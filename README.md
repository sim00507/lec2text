# Whisper + FFmpeg 기반 음성 텍스트 변환 도구
개인적으로 사용하려고 만든 간단한 툴

`.mp4` 영상 파일에서 음성을 추출한 후, Whisper를 통해 텍스트로 변환함.  

## 요구 사항
- Python 3.8 이상
- openai-whisper
- FFmpeg
- CUDA 지원 GPU 환경 권장 (Whisper GPU 사용 기준)

## 설치
1. Whisper 설치
```bash
pip install -U openai-whisper
```

2. FFmpeg 설치
[FFmpeg 공식 홈페이지](https://ffmpeg.org/download.html)에서 설치하거나, Windows의 경우 Chocolatey 사용:
```bash
choco install ffmpeg
```

3. 설치 확인
```bash
ffmpeg -version
```

## 사용
스크립트 실행 후, 현재 디렉토리에 있는 `.mp4` 파일 목록이 출력됨.
변환할 파일을 선택하면 다음과 같은 순서로 동작함:

1. 선택한 mp4 → mp3로 변환 (FFmpeg 사용)
2. Whisper로 음성 인식 (medium 모델 + GPU + fp16 사용)
3. 세그먼트 단위로 결과 출력
4. 전체 텍스트를 `.txt` 파일로 저장

## 출력 경로
변환 결과는 `result/영상파일명/디렉토리`에 저장됨:
- 추출된 오디오: `영상파일명.mp3`
- 텍스트 파일: `영상파일명.txt`

## 예시
```bash
python lec2text.py
```
```bash
🎞 변환할 .mp4 파일을 선택하세요:
1. interview.mp4
2. lecture_clip.mp4
번호 입력: 1

🔄 'interview.mp4' → 'result/interview/interview.mp3' 변환 중...
🧠 Whisper 모델 로딩 중 (GPU)...
🎧 음성 텍스트화 진행 중(세그먼트 출력 중)...
[1] (0.00s ~ 4.32s): 안녕하세요. 반갑습니다.
[2] (4.32s ~ 9.01s): 오늘은 Whisper에 대해 소개드리겠습니다.
...
✅ 변환 완료! 결과 텍스트는 'result/interview/interview.txt'에 저장되었습니다.
```