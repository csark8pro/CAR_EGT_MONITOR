/*Sourcecode_Abgastemperaturanzeige*/

/* Digital Display Modell 5641AS
 * 7seg-pinout-annotated_1500.jpg
 * Zur Steuerung benutze ich eine schon existierende Bibliothek
 * https://github.com/DeanIsMe/SevSeg
 * 
 * Draufsicht!
 * Zahl auswahl von links nach Rechts(8.8.8.8.):
 * 1. Segment Pin 12 links oben Masse(low) -> Board Pin 31
 * 2. Segment Pin 9 3. von rechts oben Masse(low) -> Board Pin 32
 * 3. Segment Pin 8 2. von rechts oben Masse(low) -> Board Pin 33
 * 4. Segment Pin 6 rechts unten Masse(low) -> Board Pin 34
 * 
 * Segment der Zahl auswahl 8.:
 * Der Punkt (.) Pin 3 von links unten Plus(high) -> Board Pin 41
 * Horizontalstrich unten Pin 2 2. von links unten -> Board Pin 42
 * Horizontalstrich mitte Pin 5 2. von rechts unten -> Board Pin 43
 * Horizontalstrich oben Pin 11 2. von links oben -> Board Pin 44
 * Vertikalstrich links unten Pin 1 1. von links unten -> Board Pin 45
 * Vertikalstrich rechts unten Pin 4 4. von links unten -> Board Pin 46
 * Vertikalstrich links oben Pin 10 3. von links oben -> Board Pin 47
 * Vertikalstrich rechts oben Pin 7 rechts oben -> Board Pin 48
 */

#include "SevSeg.h"
#include "max6675.h"
#include "stdlib.h"

//Display init
SevSeg sevseg;

//Display stuff
//pin belegung
byte numDigits = 4;
byte digitPins[] = {31, 32, 33, 34};
byte segmentPins[] = {44 ,48, 46, 42, 45, 47, 43, 41};


//flags
bool resistorsOnSegments = false; //wichtig, false = resistor 330ohm an den Masse(low)digit(position) punkten, true = segment(zahlschnipsel) Plus(high) sonst schaden an der Platine möglich !
byte hardwareConfig = COMMON_CATHODE;//wichtig anode oder cathode beachten ! andere schaltung in der Anzeige
bool updateWithDelays = false;
bool leadingZeros = false;
bool disableDecPoint = false;


//Thermo stuff max6675
//Cylinder 1 pinout
int cylinder_1_so = 4;
int cylinder_1_cs = 3;
int cylinder_1_sck = 2;

//Cylinder 2 pinout
int cylinder_2_so = 7;
int cylinder_2_cs = 5;
int cylinder_2_sck = 6;

//Cylinder 3 pinout
int cylinder_3_so = 10;
int cylinder_3_cs = 9;
int cylinder_3_sck = 8;

//Cylinder 4 pinout
int cylinder_4_so = 13;
int cylinder_4_cs = 12;
int cylinder_4_sck = 11;

//Cylinder 5 pinout
int cylinder_5_so = 52;
int cylinder_5_cs = 51;
int cylinder_5_sck = 50;

//Cylinder 6 pinout
int cylinder_6_so = 26;
int cylinder_6_cs = 24;
int cylinder_6_sck = 22;


//module init 
//Cylinder 1
MAX6675 thermo_modul_cylinder_1(cylinder_1_sck, cylinder_1_cs,cylinder_1_so );
//Cylinder 2
MAX6675 thermo_modul_cylinder_2(cylinder_2_sck, cylinder_2_cs,cylinder_2_so );
//Cylinder 3
MAX6675 thermo_modul_cylinder_3(cylinder_3_sck, cylinder_3_cs,cylinder_3_so );
//Cylinder 4
MAX6675 thermo_modul_cylinder_4(cylinder_4_sck, cylinder_4_cs,cylinder_4_so );
//Cylinder 5
MAX6675 thermo_modul_cylinder_5(cylinder_5_sck, cylinder_5_cs,cylinder_5_so );
//Cylinder 6
MAX6675 thermo_modul_cylinder_6(cylinder_6_sck, cylinder_6_cs,cylinder_6_so );
//readout timing counter
int mscount = 0;


void setup() {
  sevseg.begin(hardwareConfig, numDigits, digitPins, segmentPins, resistorsOnSegments, updateWithDelays, leadingZeros, disableDecPoint);
  Serial.begin(9600);
  delay(500);
}
void loop() {
  delay(1);
  mscount++;
  if(mscount == 800){
      int temp_cyl_1, temp_cyl_2, temp_cyl_3, temp_cyl_4, temp_cyl_5, temp_cyl_6;
      //Serial.print("Cyl_1(");
      Serial.print(temp_cyl_1 = thermo_modul_cylinder_1.readCelsius());
      //Serial.print(") ");
      //Serial.print("Cyl_2(");
      Serial.print(temp_cyl_2 = thermo_modul_cylinder_2.readCelsius());
      //Serial.print(") ");
      //Serial.print("Cyl_3(");
      Serial.print(temp_cyl_3 = thermo_modul_cylinder_3.readCelsius());
      //Serial.print(") ");
      //Serial.print("Cyl_4(");
      Serial.print(temp_cyl_4 = thermo_modul_cylinder_4.readCelsius());
      //Serial.print(") ");
      //Serial.print("Cyl_5(");
      Serial.print(temp_cyl_5 = thermo_modul_cylinder_5.readCelsius());
      //Serial.print(") ");
      //Serial.print("Cyl_6(");
      Serial.print(temp_cyl_6 = thermo_modul_cylinder_6.readCelsius());
      //Serial.print(") ");
      sevseg.setNumber(temp_cyl_1);
      mscount = 0;
    }
  sevseg.refreshDisplay();
  
  /* sevseg.setNumber(4444,0);
   sevseg.refreshDisplay();*/
  /* sevseg.setChars("1.956");
   sevseg.refreshDisplay();*/
}
