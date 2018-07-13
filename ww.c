#include <wiringPi.h>
int main (void)
 {
 int x=0;
 wiringPiSetupPhys () ;
 pinMode (7, OUTPUT) ; 
for (x=0;x<=20;x++)
 { digitalWrite (7, HIGH) ; delay (500) ; 
digitalWrite (7, LOW) ; delay (500) ;
}
return 0 ;
}
