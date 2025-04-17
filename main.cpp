#include <opencv2/opencv.hpp>
using namespace cv;

int main() {
    Mat img = imread("roro.jpg");
    if(img.empty()) {
        printf("이미지 파일을 불러올 수 없습니다.\n");
        return -1;
    }
    imshow("image", img);
    waitKey(0);
    return 0;
}