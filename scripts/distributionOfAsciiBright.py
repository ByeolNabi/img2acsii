# 각 문자들이 해당하는 밝기가 어떻게 분포되어있는지
import matplotlib.pyplot as plt
import numpy as np
import os  # os 모듈 추가

# --- 데이터 로드 ---
data_filepath = "scripts/reference/Consolas_GrayScale.txt"
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

# 데이터가 성공적으로 로드되었는지 확인
if len(data) == 0:
    print("Error: 파일에서 데이터를 로드하지 못했거나 데이터가 없습니다.")
    exit()

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Histogram - distribution of values
bins = np.arange(0, 256, 10)  # Create bins from 0 to 255 with step 10
ax1.hist(data, bins=bins, color="skyblue", edgecolor="black", alpha=0.7)
ax1.set_title("Distribution of Values (Histogram)", fontsize=16)
ax1.set_xlabel("Value (0-255)", fontsize=12)
ax1.set_ylabel("Frequency", fontsize=12)
ax1.grid(axis="y", linestyle="--", alpha=0.7)
ax1.set_xlim(0, 255)

# Add some statistics
mean_val = np.mean(data)
median_val = np.median(data)
min_val = min(data)
max_val = max(data)
std_val = np.std(data)

stats_text = f"Mean: {mean_val:.2f}\nMedian: {median_val:.2f}\nMin: {min_val}\nMax: {max_val}\nStd Dev: {std_val:.2f}"
ax1.text(
    0.02,
    0.95,
    stats_text,
    transform=ax1.transAxes,
    fontsize=12,
    verticalalignment="top",
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.5),
)

# Line plot with markers showing the actual distribution
sorted_data = sorted(data)
ax2.plot(range(len(data)), sorted_data, "o-", markersize=5, color="blue")
ax2.set_title("Values in Ascending Order", fontsize=16)
ax2.set_xlabel("Index", fontsize=12)
ax2.set_ylabel("Value (0-255)", fontsize=12)
ax2.grid(True, linestyle="--", alpha=0.7)
ax2.set_ylim(0, 255)

# Add horizontal lines showing quartiles
q1 = np.percentile(data, 25)
q3 = np.percentile(data, 75)
ax2.axhline(y=q1, color="red", linestyle="--", alpha=0.7, label=f"Q1: {q1:.2f}")
ax2.axhline(
    y=median_val,
    color="green",
    linestyle="--",
    alpha=0.7,
    label=f"Median: {median_val:.2f}",
)
ax2.axhline(y=q3, color="purple", linestyle="--", alpha=0.7, label=f"Q3: {q3:.2f}")
ax2.axhline(
    y=mean_val, color="orange", linestyle="--", alpha=0.7, label=f"Mean: {mean_val:.2f}"
)
ax2.legend()

# KDE (Kernel Density Estimation) plot
from scipy.stats import gaussian_kde

ax3 = ax1.twinx()
kde = gaussian_kde(data)
x_vals = np.linspace(0, 255, 1000)
ax3.plot(x_vals, kde(x_vals), "r-", linewidth=2)
ax3.set_ylabel("Density", color="r", fontsize=12)
ax3.tick_params(axis="y", labelcolor="r")
ax3.set_ylim(bottom=0)

plt.tight_layout()
plt.show()

# Create a value count visualization
plt.figure(figsize=(14, 6))
unique_vals, counts = np.unique(data, return_counts=True)
plt.bar(unique_vals, counts, width=3, color="skyblue", edgecolor="black", alpha=0.7)
plt.title("Count of Each Unique Value", fontsize=16)
plt.xlabel("Value (0-255)", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.xlim(0, 255)
plt.tight_layout()
plt.show()
