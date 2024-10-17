import cv2
import numpy as np
import imageio

# GIF 파일 경로 설정
input_gif_path = "assets/"
output_gif_path = "result/"

# GIF 읽기 (imageio 사용)
gif_reader = imageio.get_reader(input_gif_path)
frames = []

# GIF 메타데이터에서 fps 가져오기 (없을 경우 기본값 10 설정)
meta_data = gif_reader.get_meta_data()
fps = meta_data.get('fps', 30)  # 기본값 10fps

for frame in gif_reader:
    # 이미지 크기 가져오기
    frame_array = np.array(frame)
    
    # 흑백으로 변환하여 실루엣 추출
    gray_frame = cv2.cvtColor(frame_array, cv2.COLOR_RGB2GRAY)
    
    # 임계값을 조정하여 더 민감하게 처리 (예: 50 이상만 실루엣으로 남기기)
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

# GIF로 저장
imageio.mimsave(output_gif_path, frames, fps=fps)

print(f"GIF saved to {output_gif_path}")
