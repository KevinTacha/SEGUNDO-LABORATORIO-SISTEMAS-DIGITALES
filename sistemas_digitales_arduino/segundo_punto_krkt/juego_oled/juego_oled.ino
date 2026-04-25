#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_W 128
#define SCREEN_H  64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_W, SCREEN_H, &Wire, OLED_RESET);

// Personaje
const int CHAR_X   = 20;
const int SUELO_Y  = 54;
const int CHAR_H   = 8;
int charY          = SUELO_Y - CHAR_H;
int velY           = 0;
bool enSuelo       = true;

// Fisica
const int GRAVEDAD      =  1;
const int FUERZA_SALTO  = -25;

// Obstaculos
const int MAX_OBS      = 2;
int obsX[MAX_OBS];
int obsH[MAX_OBS];
const int OBS_W        = 6;
const int OBS_VEL_BASE = 3;
int obsVel             = OBS_VEL_BASE;

// Estado
int  puntos         = 0;
int  nivel          = 1;
bool gameOver       = false;
bool esperandoStart = true;
bool saltoPendiente = false;

// Timing
unsigned long ultimoFrame = 0;
const int FRAME_MS = 50;

void spawnObs(int i) {
  obsX[i] = SCREEN_W + random(20, 80);
  obsH[i] = random(10, 24);
}

void dibujarPersonaje(int x, int y) {
  display.fillRect(x+2, y,   4, 4, WHITE);
  display.fillRect(x+3, y+4, 2, 3, WHITE);
  int anim = (millis()/150) % 2;
  if (anim==0){ display.drawPixel(x+2,y+7,WHITE); display.drawPixel(x+4,y+6,WHITE); }
  else        { display.drawPixel(x+4,y+7,WHITE); display.drawPixel(x+2,y+6,WHITE); }
}

void pantallaInicio() {
  display.clearDisplay();
  display.setTextSize(2); display.setTextColor(WHITE);
  display.setCursor(10,4); display.print("ESQUIVA!");
  display.setTextSize(1);
  display.setCursor(4,26); display.print("Presiona ESPACIO");
  display.setCursor(22,36); display.print("para jugar");
  display.drawLine(0,SUELO_Y,SCREEN_W,SUELO_Y,WHITE);
  dibujarPersonaje(CHAR_X, SUELO_Y-CHAR_H);
  display.fillRect(80, SUELO_Y-16, OBS_W, 16, WHITE);
  display.display();
}

void pantallaGameOver() {
  display.clearDisplay();
  display.setTextSize(2); display.setTextColor(WHITE);
  display.setCursor(12,6); display.print("GAME OVER");
  display.setTextSize(1);
  display.setCursor(20,30); display.print("Puntos: "); display.print(puntos);
  display.setCursor(20,42); display.print("Nivel:  "); display.print(nivel);
  display.setCursor(4,54);  display.print("ESPACIO p/ reiniciar");
  display.display();
  Serial.print("GAMEOVER:"); Serial.print(puntos);
  Serial.print(":"); Serial.println(nivel);
}

void resetJuego() {
  charY=SUELO_Y-CHAR_H; velY=0; enSuelo=true;
  puntos=0; nivel=1; obsVel=OBS_VEL_BASE;
  gameOver=false; saltoPendiente=false;
  for(int i=0;i<MAX_OBS;i++){ obsX[i]=SCREEN_W+i*70; obsH[i]=random(10,24); }
  Serial.println("START");
}

void actualizarJuego() {
  if(saltoPendiente && enSuelo){ velY=FUERZA_SALTO; enSuelo=false; Serial.println("SALTO"); }
  saltoPendiente=false;
  velY+=GRAVEDAD; charY+=velY;
  if(charY>=SUELO_Y-CHAR_H){ charY=SUELO_Y-CHAR_H; velY=0; enSuelo=true; }
  if(charY<0){ charY=0; velY=0; }
  for(int i=0;i<MAX_OBS;i++){
    obsX[i]-=obsVel;
    if(obsX[i]+OBS_W<0){
      spawnObs(i); puntos++;
      Serial.print("PTS:"); Serial.println(puntos);
      if(puntos%5==0){ nivel++; obsVel=OBS_VEL_BASE+nivel-1; Serial.print("NIV:"); Serial.println(nivel); }
    }
    int px1=CHAR_X+2,py1=charY,px2=CHAR_X+6,py2=charY+CHAR_H-1;
    int ox1=obsX[i],oy1=SUELO_Y-obsH[i],ox2=obsX[i]+OBS_W,oy2=SUELO_Y;
    if(px2>ox1&&px1<ox2&&py2>oy1&&py1<oy2) gameOver=true;
  }
}

void dibujarJuego() {
  display.clearDisplay();
  display.drawLine(0,SUELO_Y,SCREEN_W,SUELO_Y,WHITE);
  dibujarPersonaje(CHAR_X,charY);
  for(int i=0;i<MAX_OBS;i++) display.fillRect(obsX[i],SUELO_Y-obsH[i],OBS_W,obsH[i],WHITE);
  display.setTextSize(1); display.setTextColor(WHITE);
  display.setCursor(0,0);  display.print("Pts:"); display.print(puntos);
  display.setCursor(68,0); display.print("Niv:"); display.print(nivel);
  display.display();
}

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(A0));
  if(!display.begin(SSD1306_SWITCHCAPVCC,0x3C)){ Serial.println("ERROR:OLED"); while(true); }
  display.clearDisplay(); display.display();
  for(int i=0;i<MAX_OBS;i++){ obsX[i]=SCREEN_W+i*70; obsH[i]=random(10,24); }
  Serial.println("LISTO");
}

void loop() {
  if(Serial.available()>0){
    char cmd=Serial.read();
    if(cmd=='J') saltoPendiente=true;
    if(cmd=='S'||cmd=='R'){ resetJuego(); esperandoStart=false; }
  }
  if(esperandoStart){ pantallaInicio(); return; }
  if(gameOver)      { pantallaGameOver(); return; }
  unsigned long ahora=millis();
  if(ahora-ultimoFrame<FRAME_MS) return;
  ultimoFrame=ahora;
  actualizarJuego();
  dibujarJuego();
}
