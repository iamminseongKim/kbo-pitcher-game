import cv2
import numpy as np
import imageio
import os
import shutil
import imageio_ffmpeg

def process_gif_to_mp4(input_path, output_path):
    # GIF 읽기 (imageio 사용)
    gif_reader = imageio.get_reader(input_path)
    frames = []

    # GIF 메타데이터에서 fps 가져오기 (없을 경우 기본값 30 설정)
    meta_data = gif_reader.get_meta_data()
    fps = meta_data.get('fps', 30)

    for frame in gif_reader:
        # 이미지 크기 가져오기
        frame_array = np.array(frame)
        
        # 흑백으로 변환하여 실루엣 추출
        gray_frame = cv2.cvtColor(frame_array, cv2.COLOR_RGB2GRAY)
        
        # 임계값을 조정하여 더 민감하게 처리 (예: 2 이상만 실루엣으로 남기기)
        _, mask = cv2.threshold(gray_frame, 2, 255, cv2.THRESH_BINARY)
        
        # 잡음 제거를 위한 모폴로지 연산 적용 (작은 잡음 제거 및 실루엣 강화)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # 작은 잡음 제거 (opening)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) # 실루엣 구멍 채우기 (closing)
        
        # 미디언 블러로 작은 노이즈 제거
        mask = cv2.medianBlur(mask, 5)
        
        # 초록색 실루엣 생성 (RGB에서 G만 활성화)
        green_silhouette = cv2.merge([np.zeros_like(mask), mask, np.zeros_like(mask)])
        
        # 프레임 리스트에 저장
        frames.append(green_silhouette)

    # MP4로 저장
    writer = imageio.get_writer(output_path, fps=fps, codec='libx264', quality=7)
    for frame in frames:
        writer.append_data(frame)
    writer.close()

# 폴더 경로 설정
input_folder = "assets/"
output_folder = "result/"
original_folder = "original/"

# 필요한 폴더들이 없으면 생성
for folder in [output_folder, original_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# 입력 폴더의 모든 GIF 파일 처리
for filename in os.listdir(input_folder):
    if filename.lower().endswith('.gif'):
        input_path = os.path.join(input_folder, filename)
        output_filename = os.path.splitext(filename)[0] + "_out.mp4"
        output_path = os.path.join(output_folder, output_filename)
        original_path = os.path.join(original_folder, filename)
        
        # GIF를 MP4로 처리
        process_gif_to_mp4(input_path, output_path)
        print(f"Processed: {filename} -> {output_filename}")
        
        # 원본 파일을 original 폴더로 이동
        shutil.move(input_path, original_path)
        print(f"Moved original file to: {original_path}")

print("All GIFs have been processed to MP4, saved in the result folder, and originals moved to the original folder.")