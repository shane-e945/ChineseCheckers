#include <ax12.h>
#include <BioloidController.h>
#include "poses.h"

#include <Servo.h> 

BioloidController bioloid = BioloidController(1000000);

const int SERVOCOUNT = 5;
int id;
int pos;
boolean IDCheck;
boolean RunCheck;

Servo board;

void setup(){
   pinMode(0,OUTPUT);  
   
   //initialize variables 
   id = 1;
   pos = 0;
   IDCheck = 1;
   RunCheck = 0;
  //open serial port
   Serial.begin(9600);
   delay (500);   
    Serial.println("###########################");    
   Serial.println("Serial Communication Established.");    

  //Check Lipo Battery Voltage
  CheckVoltage();

  //Scan Servos, return position.
  ScanServo();
  
  MoveHome();
  
  MenuOptions();
 
  RunCheck = 1;
  
  board.attach(0);
  
  MoveBoardHome();
  //
}

void loop(){
  // read the sensor:
  
    int inByte = Serial.read();

    switch (inByte) {

    case '1':    
      ScanServo();
      break;

    case '2':    
      MoveCenter();
      break;
      
     case '3':    
      MoveHome();
      break;     

     case '4':    
      RelaxServos();
      break;     
      

    case 'h':
      MoveBoardHome();
      break;
    
     case 'r':
       MoveBoardReverse();
       break;
    
    case 'm':
      TurnOnMagnet();
      break;
      
    case 'x':
      TurnOffMagnet();
      break;
      
    case 'q':
      ArmOutOfTheWay();
      break;
      
    case 'J': {
      int x = Serial.read();
      while (x == -1) x = Serial.read();
      MoveToSquareHome(x-50);
      break; }
    
    case 'K': {
      int r = Serial.read();
      while (r == -1) r = Serial.read();
      MoveToSquareReverse(r-50);
      break; }
      
    case 'n':
      MoveDemo();
      break;
    }
}

void MoveDemo(){
  MoveHome();
  MoveBoardHome();
  int space1 = 0;
  int space2 = 0;
  delay(1000);
  MoveToSquareHome(space1);
  delay(1000);
  MoveHome();
  MoveBoardReverse();
  delay(500);
  MoveToSquareReverse(space2);
  delay(1000);
  MoveHome();
  delay(250);
  ArmOutOfTheWay();
}
  
  

void MoveToSquareReverse(int square){
  delay(100);
  bioloid.loadPose(ReversePoses[square]);
  bioloid.readPose();
  delay(1000);
  bioloid.interpolateSetup(1000);
  while(bioloid.interpolating > 0){
    bioloid.interpolateStep();
    delay(3);
  }
}

void MoveToSquareHome(int square){
  delay(100);
  bioloid.loadPose(HomePoses[square]);
  bioloid.readPose();
  delay(1000);
  bioloid.interpolateSetup(1000);
  while(bioloid.interpolating > 0){
    bioloid.interpolateStep();
    delay(3);
  }
}

void ArmOutOfTheWay(){
    delay(100);                    // recommended pause
    bioloid.loadPose(ArmOutOfTheWayPos);   // load the pose from FLASH, into the nextPose buffer   
    delay(1000);
    bioloid.interpolateSetup(1000); // setup for interpolation from current->next over 1/2 a second
    while(bioloid.interpolating > 0){  // do this while we have not reached our new pose
        bioloid.interpolateStep();     // move servos, if necessary. 
        delay(3);
    }
    if (RunCheck == 1){
      MenuOptions();
  }
}

void MoveBoardHome(){
  board.write(0);
}

void MoveBoardReverse(){
  board.write(180);
}

void TurnOnMagnet(){
  //code
}

void TurnOffMagnet(){
  //code
}

void ScanServo(){
  id = 0;  
  Serial.println("###########################");
  Serial.println("Starting Servo Scanning Test.");
  Serial.println("###########################");
  
  Serial.println("Board: ");
  id = board.read();
  Serial.println(id);
  id = 0;
  while (id <= SERVOCOUNT){
  pos =  ax12GetRegister(id, 36, 2);
  Serial.print("Servo ID: ");
  Serial.println(id);
  Serial.print("Servo Position: ");
  Serial.println(pos);
  
  if (pos <= 0){
  Serial.println("###########################");
  Serial.print("ERROR! Servo ID: ");
  Serial.print(id);
  Serial.println(" not found. Please check connection and verify correct ID is set.");
  Serial.println("###########################"); 
  IDCheck = 0;
  }
  
  id = (id++)%SERVOCOUNT;
  }
  if (IDCheck == 0){
    Serial.println("###########################");
    Serial.println("ERROR! Servo ID(s) are missing from Scan. Please check connection and verify correct ID is set.");
    Serial.println("###########################");  
  }
  else{
  Serial.println("All servo IDs present.");
  }
    if (RunCheck == 1){
    MenuOptions();
  }

}



void CheckVoltage(){  
   // wait, then check the voltage (LiPO safety)
  float voltage = (ax12GetRegister (1, AX_PRESENT_VOLTAGE, 1)) / 10.0;
  Serial.println("###########################");   
  Serial.print ("System Voltage: ");
  Serial.print (voltage);
  Serial.println (" volts.");
  if (voltage < 10.0){
    Serial.println("Voltage levels below 10v, please charge battery.");
    while(1);
  }  
  if (voltage > 10.0){
  Serial.println("Voltage levels nominal.");
  }
    if (RunCheck == 1){
      MenuOptions();
  }
      Serial.println("###########################"); 
}

void MoveCenter(){
    delay(100);                    // recommended pause
    bioloid.loadPose(Center);   // load the pose from FLASH, into the nextPose buffer
    bioloid.readPose();            // read in current servo positions to the curPose buffer
    Serial.println("###########################");
    Serial.println("Moving servos to centered position");
    Serial.println("###########################");    
    delay(1000);
    bioloid.interpolateSetup(1000); // setup for interpolation from current->next over 1/2 a second
    while(bioloid.interpolating > 0){  // do this while we have not reached our new pose
        bioloid.interpolateStep();     // move servos, if necessary. 
        delay(3);
    }
    if (RunCheck == 1){
      MenuOptions();
  }
}


void MoveHome(){
    delay(100);                    // recommended pause
    bioloid.loadPose(Home);   // load the pose from FLASH, into the nextPose buffer
    bioloid.readPose();            // read in current servo positions to the curPose buffer
    Serial.println("###########################");
    Serial.println("Moving servos to Home position");
    Serial.println("###########################");    
    delay(1000);
    bioloid.interpolateSetup(1000); // setup for interpolation from current->next over 1/2 a second
    while(bioloid.interpolating > 0){  // do this while we have not reached our new pose
        bioloid.interpolateStep();     // move servos, if necessary. 
        delay(3);
    }
    if (RunCheck == 1){
      MenuOptions();
  }
}




void MenuOptions(){
  
    Serial.println("###########################"); 
    Serial.println("Please enter option 1-5 to run individual tests again.");     
    Serial.println("1) Servo Scanning Test");        
    Serial.println("2) Move Servos to Center"); 
    Serial.println("3) Move Servos to Home");     
    Serial.println("4) Relax Servos");            
    Serial.println("5) Perform Movement Sign Test");                
    Serial.println("6) Check System Voltage");   
    Serial.println("7) Perform LED Test");       
    Serial.println("###########################"); 
}

void RelaxServos(){
  id = 1;
  Serial.println("###########################");
  Serial.println("Relaxing Servos.");
  Serial.println("###########################");    
  while(id <= SERVOCOUNT){
    Relax(id);
    id = (id++)%SERVOCOUNT;
    delay(50);
  }
   if (RunCheck == 1){
      MenuOptions();
  }
}

void LEDTest(){
    id = 1;
  Serial.println("###########################");
  Serial.println("Running LED Test");
  Serial.println("###########################");    
  while(id <= SERVOCOUNT){
    ax12SetRegister(id, 25, 1);
    Serial.print("LED ON - Servo ID: ");
    Serial.println(id);
    delay(3000);
    ax12SetRegister(id, 25, 0);  
    Serial.print("LED OFF - Servo ID: ");
    Serial.println(id);    
    delay(3000);    
    id = id++;
  }
  
   if (RunCheck == 1){
      MenuOptions();
  }
}
