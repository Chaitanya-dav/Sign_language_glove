// Arduino UNO compatible version
// Note: UNO has only A0..A5, so Y and Z are set to 0 here.

const int flexPin1 = A0;
const int flexPin2 = A1;
const int flexPin3 = A2;
const int flexPin4 = A3;
const int flexPin5 = A4;

const int xpin = A5;   // only 1 accel axis available without extra hardware
const int pinx = 12;   // contact 1
const int piny = 8;    // contact 2
const int pinz = 10;   // contact 3 (stop flag in your Python code)

void setup() {
  Serial.begin(9600);

  pinMode(pinx, INPUT_PULLUP);
  pinMode(piny, INPUT_PULLUP);
  pinMode(pinz, INPUT_PULLUP);

  // If using PLX-DAQ, uncomment these:
  // Serial.println("CLEARDATA");
  // Serial.println("LABEL,F1,F2,F3,F4,F5,X,Y,Z,C1,C2,C3");
}

void loop() {
  int f1 = analogRead(flexPin1);
  int f2 = analogRead(flexPin2);
  int f3 = analogRead(flexPin3);
  int f4 = analogRead(flexPin4);
  int f5 = analogRead(flexPin5);

  int xRaw = analogRead(xpin);
  int xVal = map(xRaw, 0, 1023, 0, 255);

  // UNO analog limit workaround
  int yVal = 0;
  int zVal = 0;

  int c1 = digitalRead(pinx);
  int c2 = digitalRead(piny);
  int c3 = digitalRead(pinz);

  // Output for Python parser: 11 comma-separated integers
  Serial.print(f1); Serial.print(",");
  Serial.print(f2); Serial.print(",");
  Serial.print(f3); Serial.print(",");
  Serial.print(f4); Serial.print(",");
  // Serial.print(f5); Serial.print(",");
  // Serial.print(xVal); Serial.print(",");
  // Serial.print(yVal); Serial.print(",");
  // Serial.print(zVal); Serial.print(",");
  // Serial.print(c1); Serial.print(",");
  // Serial.print(c2); Serial.print(",");
  Serial.println(c3);

  delay(500);
}
