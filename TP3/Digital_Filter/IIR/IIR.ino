/* Parámetros de pines y bits */
/****************************************************************************/
const int analogIn = 0;

const int bitValues[] = {128, 64, 32, 16, 8, 4, 2};
const int pinsOut[] = {6, 7, 9, 10, 11, 12, 13};
int analogBin = 0;
/****************************************************************************/


/* Respuesta impulsiva */
/****************************************************************************/

#include "coefs.h"

/****************************************************************************/


/* Variables */
/****************************************************************************/
double xn[Nb];
double yn[Na];

int i = 0;
double y = 0;
/****************************************************************************/

/* Clock */
/****************************************************************************/
void setup() {
  // put your setup code here, to run once:
  for (i = 0; i < Nb; ++i) xn[i] = 0;
  for (i = 0; i < Na; ++i) yn[i] = 0;
  for (i = 0; i < 7; ++i) pinMode(pinsOut[i], OUTPUT);
  
  noInterrupts();           // disable all interrupts

  TCCR1A = 0;

  TCCR1B = 0;

  TCNT1  = 0;


  OCR1A = 60;            // compare match register 16MHz/256/60 Hz

  TCCR1B |= (1 << WGM12);   // CTC mode

  TCCR1B |= (1 << CS12);    // 256 prescaler 

  TIMSK1 |= (1 << OCIE1A);  // enable timer compare interrupt

  interrupts();             // enable all interrupts

}
/****************************************************************************/

/* Filtrado IIR */
/****************************************************************************/

double iir_filter(int input, double xn[Nb], double yn[Na], const double num[Nb], const double den[Na]){

  double ytemp = num[0] * input;
  
  for (i = max(Nb, Na) - 1; i > 0; --i){
    if (i < Nb){
      xn[i] = xn[i - 1];
      ytemp += num[i] * xn[i];
    }

    if (i < Na){
      yn[i] = yn[i - 1];
      ytemp -= den[i] * yn[i];
    }
    
  }

  ytemp /= den[0];
  xn[0] = input;
  yn[0] = ytemp;

  return ytemp;
  
}
/****************************************************************************/


/* Output en bits */
/****************************************************************************/

void write_binary(int value){
  for (i = 0; i < 7; ++i){
    if (value >= bitValues[i]){
        value -= bitValues[i];
        digitalWrite(pinsOut[i], HIGH);
    }
      
    else{
      digitalWrite(pinsOut[i], LOW);
    }
  }
}
/****************************************************************************/

/* Interrupción para muestreado y filtrado */
/****************************************************************************/

ISR(TIMER1_COMPA_vect)          // timer compare interrupt service routine

{

  write_binary(uint8_t(y));
  analogBin = analogRead(analogIn) / 4 - 128;
  y = iir_filter(analogBin, xn, yn, num, den) + 128;
}
/****************************************************************************/

void loop() {
  // put your main code here, to run repeatedly:
}
