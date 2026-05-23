#include <Arduino.h>
#include <Servo.h>
#include <ArduinoJson.h> // 1. 안전한 JSON 라이브러리 로드

Servo servoX;

const int pinJoyX = A0;

unsigned long lastSendTime = 0;
const unsigned long sendInterval = 100;

void setup() {
  Serial.begin(9600);
  servoX.attach(9);
  servoX.write(90);
}

void loop() {
  unsigned long currentTime = millis();

  // [송신부] 아두이노 -> PC (이건 문자열 조립도 괜찮지만, 일관성을 유지)
  if (currentTime - lastSendTime >= sendInterval) {
    int rawX = analogRead(pinJoyX);

    String jsonStr = "{";
    jsonStr += "\"mcu_timestamp\":" + String(currentTime) + ",";
    jsonStr += "\"joystick_x\":" + String(rawX) + ",";
    jsonStr += "\"device_id\":\"UNO_ROBOT_02\"";
    jsonStr += "}";
    
    Serial.println(jsonStr);
    lastSendTime = currentTime;
  }

  // [수신부] PC -> 아두이노 (★ 정석 JSON 파싱 구조로 변경)
  if (Serial.available() > 0) {
    String rcvData = Serial.readStringUntil('\n');
    rcvData.trim();

    // 메모리 풀(Doc) 생성 (아두이노 사양에 맞게 크기 지정)
    JsonDocument doc;

    // 역직렬화 (문자열을 깨끗한 JSON 객체로 파싱)
    DeserializationError error = deserializeJson(doc, rcvData);

    // 만약 파이썬이 준 JSON 데이터가 깨졌거나 공백 때문에 이상하면 패스(안전장치)
    if (error) {
      return; 
    }

    // 파이썬 딕셔너리 쓰듯이 키 값으로 안전하게 데이터 추출!
    // 공백이 있든, 순서가 바뀌든 키 이름만 맞으면 정확하게 찾아옵니다.
    if (doc.containsKey("angle_x")) {
      int angleX = doc["angle_x"];

      
      // 구동 범위 제한 제어
      angleX = constrain(angleX,30,150);
      servoX.write(angleX);
    }
  }
}