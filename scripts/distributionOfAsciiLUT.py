import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import os # os 모듈 추가

# --- 데이터 로드 ---
data_filepath = "scripts/reference/Consolas_LUT.txt"
data = []

try:
    # 파일 경로가 존재하는지 확인
    if not os.path.exists(data_filepath):
        raise FileNotFoundError(f"Error: 파일을 찾을 수 없습니다 - {data_filepath}")

    with open(data_filepath, "r") as f:
        for line in f:
            # 각 줄을 정수로 변환하여 리스트에 추가 (빈 줄이나 공백 무시)
            try:
                value = int(line.strip())
                data.append(value)
            except ValueError:
                print(f"Warning: 정수로 변환할 수 없는 줄 건너뜀: '{line.strip()}'")

    # 데이터를 NumPy 배열로 변환 (선택 사항이지만 권장)
    data = np.array(data)
    print(f"데이터 로드 성공: {len(data)}개 항목 로드됨.")

except FileNotFoundError as e:
    print(e)
    exit()  # 파일 없으면 종료
except Exception as e:
    print(f"Error: 데이터 로드 중 오류 발생 - {e}")
    exit()  # 기타 오류 시 종료
    
# 각 ASCII 코드의 빈도수 계산
counter = Counter(data)

# 빈도수를 기준으로 내림차순 정렬
sorted_counts = sorted(counter.items(), key=lambda x: x[1], reverse=True)

# 그래프 그리기를 위해 키와 값 분리
ascii_codes, frequencies = zip(*sorted_counts)

# macOS에서 한글 폰트 설정
# 'AppleGothic'은 macOS의 기본 한글 폰트입니다
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# ASCII 코드를 문자로 변환하여 x축 레이블 생성
ascii_labels = [f"{code}({chr(code)})" for code in ascii_codes]

# 그래프 그리기
plt.figure(figsize=(15, 7))
bars = plt.bar(range(len(ascii_codes)), frequencies)

# x축 레이블 설정 (ASCII 코드와 해당 문자) - 회전 없이 정면으로 표시
plt.xticks(range(len(ascii_codes)), ascii_labels, rotation=90, fontsize=10)

# 그래프 제목 및 축 레이블 설정
plt.title('LUT 값에서 ASCII 코드의 빈도수 (내림차순)')
plt.xlabel('ASCII 코드(문자)')
plt.ylabel('빈도수')

# 그래프 레이아웃 조정
plt.tight_layout()

# 그래프 표시
plt.show()
