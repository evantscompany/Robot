// servo test

// #include <Arduino.h>
// #include <Servo.h>

// Servo myServo;

// void setup() {
//   Serial.begin(9600); // PC와 대화 준비
//   myServo.attach(9);
//   myServo.write(90);  // 초기 위치 90도 고정
//   Serial.println("Enter angle (0-180):");
// }

// void loop() {
//   if (Serial.available() > 0) {
//     // 숫자를 입력받으면 그 각도로 이동 후 정지
//     int angle = Serial.parseInt(); 
//     if (angle >= 0 && angle <= 180) {
//       myServo.write(angle);
//       Serial.print("Moved to: ");
//       Serial.println(angle);
//     }
//   }
// }


// DHT_test

// #include <Arduino.h>
// #include <DHT.h>

// #define DHTPIN 2     // 센서 데이터 핀
// #define DHTTYPE DHT11 // 센서 종류 설정

// DHT dht(DHTPIN, DHTTYPE);

// void setup() {
//   Serial.begin(9600);
//   Serial.println("DHT11 Smart Farm Test Start!");
//   dht.begin();
// }

// void loop() {
//   delay(2000); // 센서 읽기 간격 (최소 2초 권장)

//   float h = dht.readHumidity();    // 습도 읽기
//   float t = dht.readTemperature(); // 온도 읽기

//   if (isnan(h) || isnan(t)) {
//     Serial.println("Failed to read from DHT sensor!");
//     return;
//   }

//   Serial.print("Humidity: ");
//   Serial.print(h);
//   Serial.print("%  |  Temperature: ");
//   Serial.print(t);
//   Serial.println("°C");
// }


// 스마트 팜 자동 환기 시스템

// 논리 => 온도가 28도 이상으로 올라가면, 서보모터를 90도로 열고, 온도가 낮아지면 다시 0도로 닫기

#include <Arduino.h>
#include <Servo.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
Servo myServo;

// 셋업 - 전원이 켜질때 딱 한번만 실행되는 설정
void setup() {
  Serial.begin(9600);   //컴퓨터와 대화할 통로(시리얼) 열기. 속도 9600
  dht.begin();          //온습도 센서에 "이제 측정 시작" 라고 명령
  myServo.attach(9);     //서보모터는 9번 구멍에 연결되었다고 선언
  myServo.write(0);      //시작할 때 모터 각도를 0으로 맞춤

  Serial.println("Smart Farm System Online!"); // 컴퓨터 화면에 시작 메시지 띄우기
}

// 루프 - 전원이 켜져 있는 동안 위에서 아래로 계속 무한 반복 실행
void loop(){
  // 1. 센서가 측정할 시간 (2초)
  delay(2000);

  // 2. 센서로부터 현재 온도 읽어서 temp에 담기
  float temp = dht.readTemperature();

  // 3. 만약 센서 값을 못읽었다면, 이번차례 건너뛰기(에러방지)
  if (isnan(temp)){
    Serial.println("Sensor Error : Could not read temperature.");
    return; // 아래 코드 실행하지 않고, loop 시작점으로 이동
  }

  // 4. 현재 온도를 컴퓨터 화면(시리얼 모니터에 보여주기)
  Serial.print("Current Temperature: ");
  Serial.print(temp);
  Serial.print("C");

  // 5. 판단로직 - 온도가 28도 이상인지 확인하기.
  if (temp>=31.0){
    Serial.println("Too HOT! Opening the window (90 degrees)");
    myServo.write(90);    // 서보모터 각도 90도
  }
  else{
    // 온도가 28도 미만인경우
    Serial.println("Temperature OK. Closing the window (0 degree)");
    myServo.write(0);
  }
}
