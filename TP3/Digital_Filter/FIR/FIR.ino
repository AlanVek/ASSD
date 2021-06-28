
/* Parámetros de pines y bits */
const int analogIn = 0;

const int bitValues[] = {128, 64, 32, 16, 8, 4, 2};
const int pinsOut[] = {6, 7, 9, 10, 11, 12, 13};

int analogBin = 0;
const int maxOut = pow(2, 8);

/* Respuesta impulsiva */
const int N = 22;
double h[N] = 
        { 0.44559,  0.07454, -0.03145,  0.01964, -0.01435,  0.01145,
       -0.0097 ,  0.00859, -0.00788,  0.00746, -0.00726,  0.00726,
       -0.00746,  0.00788, -0.00859,  0.0097 , -0.01145,  0.01435,
       -0.01964,  0.03145, -0.07454, -0.44559};


/* Variables */
int xn[N];
int i = 0;
double y = 0;

void setup() {
  // put your setup code here, to run once:
  for (i = 0; i < N; ++i) xn[i] = 0;
  for (i = 0; i < 7; ++i) pinMode(pinsOut[i], OUTPUT);
  
  noInterrupts();           // disable all interrupts

  TCCR1A = 0;

  TCCR1B = 0;

  TCNT1  = 0;


  OCR1A = 60;            // compare match register 16MHz/256/2Hz

  TCCR1B |= (1 << WGM12);   // CTC mode

  TCCR1B |= (1 << CS12);    // 256 prescaler 

  TIMSK1 |= (1 << OCIE1A);  // enable timer compare interrupt

  interrupts();             // enable all interrupts

}


double fir_filter(int input, int xn[N], double h[N]){

  double ytemp = h[0] * input;
  
  for (i = N-1; i > 0; --i){
    xn[i] = xn[i - 1];
    ytemp += h[i] * xn[i];
  }
  
  xn[0] = input;

  return ytemp;
  
}

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


ISR(TIMER1_COMPA_vect)          // timer compare interrupt service routine

{

  write_binary(uint8_t(y));
  analogBin = analogRead(analogIn) / 4 - 128;
  y = fir_filter(analogBin, xn, h) + 128;
}

void loop() {
  // put your main code here, to run repeatedly:
}
