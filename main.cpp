#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

int main() {
  Mat img = imread("roro.jpg");
  if (img.empty()) {
    printf("이미지 파일을 불러올 수 없습니다.\n");
    return -1;
  }
  Mat img_gray;
  cvtColor(img, img_gray, COLOR_BGR2GRAY);

  // 사이즈 변경
  resize(img, img, Size(img.cols, img.rows));
  resize(img_gray, img_gray, Size(img_gray.cols >> 1, img_gray.rows >> 1));

  putText(img,                    // 글자를 쓸 이미지
          "Hello, OpenCV!",       // 출력할 문자열
          Point(50, 100),         // 시작 좌표(왼쪽 아래 기준)
          FONT_HERSHEY_COMPLEX,   // 폰트 종류
          1.0,                    // 폰트 크기 (배율)
          Scalar(255, 255, 255),  // 색상 (B, G, R) - 흰색
          2,                      // 두께
          LINE_AA                 // 선 타입 (안티앨리어싱)
  );

  imshow("image original", img);
  imshow("image gray", img_gray);
  moveWindow("image gray", img.cols, 0);

  waitKey(0);
  return 0;
}