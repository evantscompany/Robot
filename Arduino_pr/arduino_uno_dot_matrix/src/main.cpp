
// [1] 기본 전체 껐다켰다 실습

// #include <Arduino.h>
// #include <LedControl.h>

// // 핀설정 (DIN = 11, CLK = 13, CS = 10)
// // 마지막 인자 1은 연결된 도트 메트릭스 모듈의 개수
// LedControl lc = LedControl(11,13,10,1);

// void setup(){
//   // 절전모드 해제(기본적으로 칩이 잠들어 있다고 함)
//   lc.shutdown(0,false);

//   // 밝기 설정(0~15 사이, 처음엔 4로 시작)
//   lc.setIntensity(0,4);

//   // 화면 깨끗하게 비우기
//   lc.clearDisplay(0);
// }

// void loop(){
//   // 1단계: 64개 LED 전체 다 켜기
//   for (int row = 0; row<8; row++){
//     for (int col =0; col<8; col++){
//       lc.setLed(0,row,col,true);
//     }
//   }
//   delay(1000); // 1초 대기

//   //2단계 : 64개 LED 전체 다 끄기
//   lc.clearDisplay(0);
//   delay(1000); // 1초 대기

// }

// [2] 기본 아두이노 스마일 예제

// #include <Arduino.h>
// #include <LedControl.h>

// LedControl lc = LedControl(11, 13, 10, 1);

// void setup() {
//   lc.shutdown(0, false);
//   lc.setIntensity(0, 3); // 눈 아프지 않게 밝기 조절
//   lc.clearDisplay(0);

//   // 스마일 모양 만들기 (1이 불이 켜지는 곳, 0이 꺼지는 곳)
//   lc.setRow(0, 0, B00111100); //   ####  
//   lc.setRow(0, 1, B01000010); //  #    # 
//   lc.setRow(0, 2, B10100101); // # #  # # (눈)
//   lc.setRow(0, 3, B10000001); // #      #
//   lc.setRow(0, 4, B10100101); // # #  # # (입 시작)
//   lc.setRow(0, 5, B10011001); // #  ##  #
//   lc.setRow(0, 6, B01000010); //  #    # 
//   lc.setRow(0, 7, B00111100); //   ####  
// }

// void loop() {
//   // 모양만 띄워놓을 거라 loop는 비워둡니다.
// }


// [3] 3초 카운트 다운 예제

#include <Arduino.h>
#include <LedControl.h>

LedControl lc = LedControl(11, 13, 10, 1);

const byte number3[8] = { B00111100, B01000010, B00000010, B00011100, B00000010, B00000010, B01000010, B00111100 };
const byte number2[8] = { B00111100, B01000010, B00000010, B00001100, B00110000, B01000000, B01000010, B01111110 };
const byte number1[8] = { B00001100, B00011100, B00001100, B00001100, B00001100, B00001100, B00001100, B00011110 };

void displayPattern(const byte pattern[8]) {
  for (int row = 0; row < 8; row++) { lc.setRow(0, row, pattern[row]); }
}

// JSON 데이터를 시리얼로 전송하는 함수
void sendJsonData(String status, int displayVal) {
  unsigned long runTime = millis(); // 아두이노가 켜진 후 흘러간 시간 (밀리초, 클럭 대용 순서 보장)
  
  // JSON 문자열 조립
  String jsonStr = "{";
  jsonStr += "\"mcu_timestamp\":" + String(runTime) + ",";
  jsonStr += "\"status\":\"" + status + "\",";
  jsonStr += "\"display_value\":" + String(displayVal) + ",";
  jsonStr += "\"device_id\":\"UNO_BOARD_01\"";
  jsonStr += "}";
  
  Serial.println(jsonStr); // 파이썬이 읽을 수 있게 한 줄로 전송
}

void setup() {
  lc.shutdown(0, false);
  lc.setIntensity(0, 5);
  lc.clearDisplay(0);
  Serial.begin(9600);
}

void loop() {
  displayPattern(number3);
  sendJsonData("COUNTDOWN", 3);
  delay(1000);

  displayPattern(number2);
  sendJsonData("COUNTDOWN", 2);
  delay(1000);

  displayPattern(number1);
  sendJsonData("COUNTDOWN", 1);
  delay(1000);

  lc.clearDisplay(0);
  sendJsonData("ACTION_GO", 0);
  
  for (int row = 0; row < 8; row++) { lc.setRow(0, row, B11111111); }
  delay(500);

  lc.clearDisplay(0);
  delay(1500);
}
