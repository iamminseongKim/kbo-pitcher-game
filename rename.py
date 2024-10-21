import os
import uuid
import csv

def rename_files_and_create_csv():
    original_folder = 'original'
    result_folder = 'result'
    csv_filename = 'file_info.csv'

    file_info = []

    # original 폴더 처리
    for filename in os.listdir(original_folder):
        if filename.endswith('.mp4'):
            team_code, name, _ = filename.split('_')
            new_filename = f"{uuid.uuid4()}.mp4"
            old_path = os.path.join(original_folder, filename)
            new_path = os.path.join(original_folder, new_filename)
            os.rename(old_path, new_path)
            file_info.append([team_code, name.split('.')[0], new_filename, ''])

    # result 폴더 처리
    for filename in os.listdir(result_folder):
        if filename.endswith('.mp4'):
            team_code, name = filename.split('_')
            new_filename = f"{uuid.uuid4()}.mp4"
            old_path = os.path.join(result_folder, filename)
            new_path = os.path.join(result_folder, new_filename)
            os.rename(old_path, new_path)
            
            # original 파일 정보 업데이트
            for item in file_info:
                if item[0] == team_code and item[1] == name.split('.')[0]:
                    item[3] = new_filename
                    break

    # CSV 파일 작성
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['team', 'name', 'original_file_name', 'result_file_name'])
        csv_writer.writerows(file_info)

    print(f"파일 이름 변경 및 CSV 파일 생성이 완료되었습니다. CSV 파일명: {csv_filename}")

rename_files_and_create_csv()

