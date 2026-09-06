// Differential Drive Motor Controller
// Receives serial commands: "L<speed> R<speed>\n"
// Speed range: -255 to 255

#define ENA 9
#define IN1 8
#define IN2 7
#define ENB 10
#define IN3 6
#define IN4 5

String inputString = "";
bool stringComplete = false;

unsigned long lastCommandTime = 0;
const unsigned long TIMEOUT_MS = 1000;

void setup() {
  Serial.begin(115200);
  inputString.reserve(50);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopMotors();
  Serial.println("Ready");
}

void loop() {
  if (millis() - lastCommandTime > TIMEOUT_MS && lastCommandTime != 0) {
    stopMotors();
  }

  if (stringComplete) {
    parseCommand(inputString);
    inputString = "";
    stringComplete = false;
    lastCommandTime = millis();
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}

void parseCommand(String cmd) {
  int lIndex = cmd.indexOf('L');
  int rIndex = cmd.indexOf('R');

  if (lIndex == -1 || rIndex == -1) return;

  int leftSpeed = cmd.substring(lIndex + 1, rIndex).toInt();
  int rightSpeed = cmd.substring(rIndex + 1).toInt();

  leftSpeed = constrain(leftSpeed, -255, 255);
  rightSpeed = constrain(rightSpeed, -255, 255);

  setMotor(leftSpeed, ENA, IN1, IN2);
  setMotor(rightSpeed, ENB, IN3, IN4);
}

void setMotor(int speed, int enPin, int in1Pin, int in2Pin) {
  if (speed > 0) {
    digitalWrite(in1Pin, HIGH);
    digitalWrite(in2Pin, LOW);
    analogWrite(enPin, speed);
  } else if (speed < 0) {
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, HIGH);
    analogWrite(enPin, -speed);
  } else {
    digitalWrite(in1Pin, LOW);
    digitalWrite(in2Pin, LOW);
    analogWrite(enPin, 0);
  }
}

void stopMotors() {
  setMotor(0, ENA, IN1, IN2);
  setMotor(0, ENB, IN3, IN4);
}
