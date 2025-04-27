#include <cmath>  // for std::round
#include <fstream>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <string>
#include <vector>
using namespace cv;
using namespace std;

// LUT 파일을 로드하는 함수
std::vector<int> loadLUT(const std::string& filename) {
  std::vector<int> lut;
  std::ifstream file(filename);
  if (!file.is_open()) {
    std::cerr << "Error: LUT 파일을 열 수 없습니다: " << filename << std::endl;
    return lut;  // 빈 벡터 반환
  }

  int value;
  while (file >> value) {
    lut.push_back(value);
  }

  if (lut.size() != 256) {
    std::cerr << "Warning: LUT 파일의 크기가 예상(256)과 다릅니다. 크기: "
              << lut.size() << std::endl;
    // 크기가 달라도 일단 진행하거나, 여기서 빈 벡터를 반환하여 오류 처리 가능
  }

  file.close();
  return lut;
}

int main() {
  // --- 설정값 ---
  const std::string lut_filepath = "scripts/reference/Consolas_LUT.txt";
  const std::string image_filepath = "roro.jpg";  // 처리할 이미지 파일 경로
  const int base_width = 11;                      // 기본 셀 너비
  const int base_height = 19;                     // 기본 셀 높이
  const double scale_factor =
      1.0;  // 셀 크기 조절 인자 (1.0 = 11x19, 2.0 = 22x38 등)
  // --- 설정값 끝 ---

  // LUT 로드
  std::vector<int> lut = loadLUT(lut_filepath);
  if (lut.empty() || lut.size() != 256) {  // LUT 로드 실패 또는 크기 오류 확인
    std::cerr
        << "LUT 로드 실패 또는 형식이 올바르지 않아 프로그램을 종료합니다."
        << std::endl;
    return -1;
  }

  // 이미지 로드
  cv::Mat img = cv::imread(image_filepath);
  if (img.empty()) {
    std::cerr << "이미지 파일을 불러올 수 없습니다: " << image_filepath
              << std::endl;
    return -1;
  }

  // 그레이스케일 변환
  cv::Mat img_gray;
  cv::cvtColor(img, img_gray, cv::COLOR_BGR2GRAY);

  // 스케일 팩터를 적용한 실제 셀 크기 계산 (최소 1x1 보장)
  int cell_width =
      std::max(1, static_cast<int>(std::round(base_width * scale_factor)));
  int cell_height =
      std::max(1, static_cast<int>(std::round(base_height * scale_factor)));

  std::cout << "입력 이미지 크기: " << img.cols << "x" << img.rows << std::endl;
  std::cout << "사용될 셀 크기: " << cell_width << "x" << cell_height
            << std::endl;
  std::cout << "ASCII 아트 생성 시작..." << std::endl;
  std::cout << "------------------------------------" << std::endl;

  // 이미지를 셀 단위로 순회하며 ASCII 문자로 변환
  for (int y = 0; y < img_gray.rows; y += cell_height) {
    for (int x = 0; x < img_gray.cols; x += cell_width) {
      // 현재 셀의 ROI(Region of Interest) 정의 (이미지 경계 처리 포함)
      cv::Rect roi(x, y, std::min(cell_width, img_gray.cols - x),
                   std::min(cell_height, img_gray.rows - y));

      // ROI 영역 추출
      cv::Mat cell = img_gray(roi);

      // 셀의 평균 밝기 계산
      cv::Scalar avg_scalar = cv::mean(cell);
      double avg_brightness =
          avg_scalar[0];  // 그레이스케일이므로 첫 번째 채널 값 사용

      // 평균 밝기를 0-255 범위로 제한하고 정수형 인덱스로 변환
      int lut_index = static_cast<int>(
          std::round(std::max(0.0, std::min(255.0, avg_brightness))));

      // LUT에서 해당 밝기에 매핑되는 문자 인덱스 가져오기
      int char_index = lut[lut_index];  // lut_index는 0~255 범위이므로 유효

      // 문자 인덱스를 실제 ASCII 문자로 변환 (인덱스 + 32)
      char ascii_char = static_cast<char>(char_index + 32);

      // 변환된 ASCII 문자 출력
      std::cout << ascii_char;
    }
    // 한 행 출력이 끝나면 줄바꿈
    std::cout << std::endl;
  }
  std::cout << "------------------------------------" << std::endl;
  std::cout << "ASCII 아트 생성 완료." << std::endl;

  // (선택 사항) 원본 및 그레이스케일 이미지 표시 - 필요 없으면 주석 처리
  // cv::imshow("Original Image", img);
  // cv::imshow("Grayscale Image", img_gray);
  // cv::waitKey(0);

  waitKey(0);
  return 0;
}