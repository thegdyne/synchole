////////////////////////////////////////////////////////////
//
//      /////                          //              //
//     //                             //              //   
//    //     //   //  /////    ///// //////   /////  //    ////
//    ////  //   //  //   // //     //   // //   // //   //   //
//      // //   //  //   // //     //   // //   // //   //////
//     // //   //  //   // //     //   // //   // //   // 
// /////  //////  //   //  ///// //   //  /////   ///  //////
//           //
//          //  MIDI TO DIN SYNCH24 HUB
//     /////    hotchk155/2016 - Sixty-four pixels ltd.
//              Code for PIC12F1822 - Compiled with XC8
//
// This work is licensed under the Creative Commons license
// Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
// To view a copy of this license, please visit:
// https://creativecommons.org/licenses/by-nc/4.0/
//
// Full repository with hardware information:
// https://github.com/hotchk155/din-synch-hub
//
// Modified by thegdyne/2025 - Internal clock feature
// - Long press RUN button to toggle between external MIDI and internal clock modes
// - Internal clock generates fixed 120 BPM
// - Ported from SourceBoost C to XC8
//
// Firmware version 
// 1 19Nov15 Initial Version
// 2 12Dec15 New PCB - output pins switched
// 3 14Aug16 Initial release version - switch added
// 4 09Dec25 Internal clock feature added - XC8 port
//
////////////////////////////////////////////////////////////

// XC8 compiler includes
#include <xc.h>
#include <stdint.h>

#define _XTAL_FREQ 16000000  // 16MHz for __delay_ms()

#define FIRMWARE_VERSION 4

// Configuration words for XC8
// CONFIG1
#pragma config FOSC = INTOSC    // Oscillator Selection
#pragma config WDTE = OFF       // Watchdog Timer Enable
#pragma config PWRTE = OFF      // Power-up Timer Enable
#pragma config MCLRE = OFF      // MCLR Pin Function Select
#pragma config CP = OFF         // Flash Program Memory Code Protection
#pragma config CPD = OFF        // Data Memory Code Protection
#pragma config BOREN = ON       // Brown-out Reset Enable
#pragma config CLKOUTEN = OFF   // Clock Out Enable
#pragma config IESO = OFF       // Internal/External Switchover
#pragma config FCMEN = OFF      // Fail-Safe Clock Monitor Enable

// CONFIG2
#pragma config WRT = OFF        // Flash Memory Self-Write Protection
#pragma config PLLEN = OFF      // PLL Enable
#pragma config STVREN = ON      // Stack Overflow/Underflow Reset Enable
#pragma config BORV = LO        // Brown-out Reset Voltage Selection
#pragma config LVP = OFF        // Low-Voltage Programming Enable

typedef unsigned char byte;

// Define the I/O pins using XC8 bit field syntax
#define P_LED1		LATAbits.LATA4
#define P_LED2		LATAbits.LATA2
#define P_RUN		LATAbits.LATA1
#define P_CLK		LATAbits.LATA0
#define P_SWITCH	PORTAbits.RA3

// Timer settings
volatile byte timerTicked = 0;		// Timer ticked flag (tick once per ms)
#define TIMER_0_INIT_SCALAR		5	// Timer 0 is an 8 bit timer counting at 250kHz
#define MIDILED_HIGH_TIME 		1 // milliseconds
#define BEATLED_HIGH_TIME 		30 // milliseconds

// The pulse width is supposed to be at 50% duty cycle
#define DEFAULT_CLOCK_LENGTH_USECS 5000

// Switch debounce time
#define SWITCH_DEBOUNCE_MS	50

// Long press detection (2 seconds)
#define LONG_PRESS_TIME_MS 2000

// Internal clock mode settings
// 120 BPM = 120 beats/min = 2 beats/sec
// At 24 PPQN = 48 pulses/sec
// Period = 1000ms / 48 = 20.833ms per pulse
#define INTERNAL_CLOCK_PERIOD_MS 21

// Mode definitions
#define MODE_EXTERNAL_MIDI 0
#define MODE_INTERNAL_CLOCK 1

volatile byte bRunning = 0;				// clock running flag
volatile byte bBeatCount = 0;			// beat count (used to flash beat LED)	
volatile byte bMidiLEDCount = 0;		// ms before MIDI activity LED goes off
volatile byte bBeatLEDCount = 0;		// ms before beat LED goes off
volatile byte bClockMode = MODE_EXTERNAL_MIDI;  // current mode
volatile byte bInternalClockCounter = 0;  // counter for internal clock generation
volatile unsigned int bModeLEDCounter = 0;  // counter for mode indication LED pattern (CHANGED to unsigned int)

////////////////////////////////////////////////////////////
// GENERATE INTERNAL CLOCK PULSE
void generate_internal_clock_pulse(void)
{
	unsigned int usecsPulseLength;
	
	P_CLK = 1;	// send clock line high
	
	// Use default pulse length for internal clock
	usecsPulseLength = DEFAULT_CLOCK_LENGTH_USECS;
	
	// Schedule the end of the clock pulse
	CCPR1H = usecsPulseLength>>8;
	CCPR1L = (byte)usecsPulseLength;
	
	// reset the timer 1 and start it
	TMR1L = 0;
	TMR1H = 0;	
	T1CONbits.TMR1ON = 1; 
	
	// Ping the beat LED every 24 pulses
	if(++bBeatCount == 24) {
		bBeatCount = 0;
		bBeatLEDCount = BEATLED_HIGH_TIME;
	}
}

////////////////////////////////////////////////////////////
// INTERRUPT HANDLER 
void __interrupt() isr(void)
{
	unsigned int usecsSinceLastClock;
	unsigned int usecsPulseLength;

	// TIMER0 OVERFLOW
	// Timer 0 overflow is used to 
	// create a once per millisecond
	// signal for blinking LEDs etc
	if(INTCONbits.T0IF)  // FIXED: Was TMR0IF, should be T0IF
	{
		TMR0 = TIMER_0_INIT_SCALAR;
		timerTicked = 1;
		
		// Handle internal clock generation when in internal mode and running
		if(bClockMode == MODE_INTERNAL_CLOCK && bRunning) {
			if(++bInternalClockCounter >= INTERNAL_CLOCK_PERIOD_MS) {
				bInternalClockCounter = 0;
				generate_internal_clock_pulse();
			}
		}
		
		// Update mode indication LED pattern
		if(bClockMode == MODE_INTERNAL_CLOCK && !bRunning) {
			// Slow pulse pattern when in internal mode but not running
			if(++bModeLEDCounter >= 500) {
				bModeLEDCounter = 0;
			}
		}
		
		INTCONbits.T0IF = 0;  // FIXED: Was TMR0IF, should be T0IF
	}
	
	// COMPARE INTERRUPT
	// This interrupt fires when Timer1 matches CCPR1H:CCPR1L.
	// This is our signal to end the output clock pulse (at 50% duty)
	if(PIR1bits.CCP1IF) 
	{	
		// drive output clock low
		P_CLK = 0;
		PIR1bits.CCP1IF = 0;
	}
	
	// TIMER1 OVERFLOW
	// If Timer1 overflows this means that 
	// we will give up timing between MIDI
	// clock messages (very slow BPM) and 
	// will instead revert to default clock
	// pulse width
	if(PIR1bits.TMR1IF)
	{
		// drive the output clock low
		T1CONbits.TMR1ON = 0; // stop the timer
		PIR1bits.TMR1IF = 0;
	}
		
	// SERIAL PORT RECEIVE
	// Only process MIDI in external MIDI mode
	if(PIR1bits.RCIF)
	{
		// get the byte
		byte b = RCREG;
		
		// Only process MIDI clock messages in external MIDI mode
		if(bClockMode == MODE_EXTERNAL_MIDI)
		{		
			switch(b)
			{
				/////////////////////////////////////////////////////////////
				// MIDI CLOCK
				case 0xf8:	
					P_CLK = 1;	// send clock line high

					// the clock was not started, or it overflowed, so 
					// we need to use a default pulse length
					if(!T1CONbits.TMR1ON) {
						usecsPulseLength = DEFAULT_CLOCK_LENGTH_USECS;
					} else {
						T1CONbits.TMR1ON = 0; 
						// capture timer 1 value (microseconds since the last
						// MIDI tick)
						usecsSinceLastClock = (((unsigned int)TMR1H<<8)|TMR1L);
						
						// divide by 2 to get pulse width at 50% duty
						usecsPulseLength = usecsSinceLastClock / 2;
					}
											
					// Schedule the end of the clock pulse
					CCPR1H = usecsPulseLength>>8;
					CCPR1L = (byte)usecsPulseLength;
					
					// reset the timer 1 and start it
					TMR1L = 0;
					TMR1H = 0;	
					T1CONbits.TMR1ON = 1; 

					// Ping the beat LED every 24 pulses
					if(++bBeatCount == 24) {
						bBeatCount = 0;
						bBeatLEDCount = BEATLED_HIGH_TIME;
					}
					
					// Indicate MIDI activity
					bMidiLEDCount = MIDILED_HIGH_TIME;
					break;

				/////////////////////////////////////////////////////////////
				// MIDI CLOCK START / CONTINUE
				case 0xfa: // start
				case 0xfb: // continue
					P_RUN = 1;
					bBeatCount = 0;
					bRunning = 1;
					// ping the beat LED for the first beat
					bBeatLEDCount = BEATLED_HIGH_TIME;
					break;

				/////////////////////////////////////////////////////////////
				// MIDI CLOCK STOP
				case 0xfc: 
					P_RUN = 0;
					bRunning = 0;
					break;
			}	
		}
		PIR1bits.RCIF = 0;			
	}
}

////////////////////////////////////////////////////////////
// INITIALISE SERIAL PORT FOR MIDI
void init_usart()
{
	PIR1bits.TXIF = 1;		//TXIF 		
	PIR1bits.RCIF = 0;		//RCIF
	
	PIE1bits.TXIE = 0;		//TXIE 		no interrupts
	PIE1bits.RCIE = 1;		//RCIE 		enable
	
	BAUDCONbits.SCKP = 0;	// SCKP		synchronous bit polarity 
	BAUDCONbits.BRG16 = 1;	// BRG16	enable 16 bit brg
	BAUDCONbits.WUE = 0;	// WUE		wake up enable off
	BAUDCONbits.ABDEN = 0;	// ABDEN	auto baud detect
		
	TXSTAbits.TX9 = 0;		// TX9		8 bit transmission
	TXSTAbits.TXEN = 0;		// TXEN		transmit disable
	TXSTAbits.SYNC = 0;		// SYNC		async mode
	TXSTAbits.SENDB = 0;	// SENDB	break character
	TXSTAbits.BRGH = 0;		// BRGH		high baudrate 
	TXSTAbits.TX9D = 0;		// TX9D		bit 9

	RCSTAbits.SPEN = 1;		// SPEN 	serial port enable
	RCSTAbits.RX9 = 0;		// RX9 		8 bit operation
	RCSTAbits.SREN = 1;		// SREN 	enable receiver
	RCSTAbits.CREN = 1;		// CREN 	continuous receive enable
		
	SPBRGH = 0;				// brg high byte
	SPBRG = 31;				// brg low byte (31250)		
}

////////////////////////////////////////////////////////////
// ENTRY POINT
void main()
{ 
	// osc control / 16MHz / internal
	OSCCON = 0b01111010;

	APFCON0bits.RXDTSEL = 1; // RX on RA5
	APFCON0bits.TXCKSEL = 1; // TX on RA4
		
	// configure io
	TRISA = 0b00100000;              	
	ANSELA = 0b00000000;
	PORTA = 0;
	
	// Configure timer 0 (controls systemticks)
	// 	timer 0 runs at 4MHz
	// 	prescaled 1/16 = 250kHz
	// 	rollover at 250 = 1kHz
	// 	1ms per rollover	
	OPTION_REGbits.TMR0CS = 0; // timer 0 driven from instruction cycle clock
	OPTION_REGbits.PSA = 0;    // timer 0 is prescaled
	OPTION_REGbits.PS = 0b011; // 1/16 prescaler
	INTCONbits.TMR0IE = 1;     // FIXED: Was TMR0IE, should be T0IE
	INTCONbits.T0IF = 0;       // FIXED: Was TMR0IF, should be T0IF

	// configure Timer 1 (controls clock pulses)
	// to count at 1MHz and interrupt on overflow
	T1CONbits.TMR1CS = 0b00;   // instruction clock source (Fosc/4)
	T1CONbits.T1CKPS = 0b10;   // prescaler 1:4 (gives us 1MHz with 4MHz Fosc/4)
	T1CONbits.nT1SYNC = 0;     // synch off
	TMR1L = 0;	               // reset timer
	TMR1H = 0;
	PIR1bits.TMR1IF = 0;       // clear timer interrupt flag
	PIE1bits.TMR1IE = 1;       // Enable timer overflow interrupt
	T1CONbits.TMR1ON = 1;      // Timer1 starts enabled

	// Configure Compare module 1 to interrupt
	// on a match between TMR1H:TMR1L and CCPR1H:CCPR1L
	CCP1CONbits.CCP1M = 0b1010; // Generate software interrupt from compare module
	PIE1bits.CCP1IE = 1;        // enable interrupt 

	// enable interrupts
	INTCONbits.GIE = 1;  // global interrupt enable
	INTCONbits.PEIE = 1; // peripheral interrupt enable
			
	// initialise USART
	init_usart();

	// Flash MIDI activity LED on startup
	P_LED1=1; P_LED2=1; __delay_ms(250);
	P_LED1=0; P_LED2=0; __delay_ms(250);
	P_LED1=1; P_LED2=1; __delay_ms(250);
	P_LED1=0; P_LED2=0; 

	int debounce = 0;
	int longPressCounter = 0;
	byte switchWasPressed = 0;
	
	// loop forever		
	while(1)
	{
		// once per ms this flag is set...
		if(timerTicked) {
			timerTicked = 0;

			// refresh LEDs
			// In external MIDI mode, LED1 blinks with MIDI activity
			// In internal clock mode, LED1 pulses slowly when stopped
			if(bClockMode == MODE_EXTERNAL_MIDI) {
				P_LED1 = !!bMidiLEDCount;
			} else {
				// Internal clock mode - show slow pulse when stopped
				if(!bRunning) {
					P_LED1 = (bModeLEDCounter < 250);  // slow pulse
				} else {
					P_LED1 = 0;  // off when running in internal mode
				}
			}
			
			if(bRunning) {
				P_LED2= !!bBeatLEDCount;
			}
			else {
				P_LED2= 0;
			}		
			if(bMidiLEDCount)
				--bMidiLEDCount;
			if(bBeatLEDCount)
				--bBeatLEDCount;
			
			// Switch handling with long press detection
			// FIXED: Switch is active LOW (pressed = 0, released = 1)
			if(!P_SWITCH) {
				// Switch is pressed (active LOW)
				if(!switchWasPressed) {
					// New press detected
					switchWasPressed = 1;
					longPressCounter = 0;
					debounce = SWITCH_DEBOUNCE_MS;
				}
				else if(debounce > 0) {
					// Debouncing
					--debounce;
				}
				else {
					// Switch is held down after debounce
					++longPressCounter;
					
					// Check for long press (2 seconds)
					if(longPressCounter >= LONG_PRESS_TIME_MS) {
						// Long press detected - toggle mode
						if(bClockMode == MODE_EXTERNAL_MIDI) {
							bClockMode = MODE_INTERNAL_CLOCK;
							// Flash both LEDs to indicate mode change
							P_LED1 = 1;
							P_LED2 = 1;
						} else {
							bClockMode = MODE_EXTERNAL_MIDI;
							// Flash both LEDs to indicate mode change
							P_LED1 = 1;
							P_LED2 = 1;
						}
						
						// Reset counters
						bInternalClockCounter = 0;
						bModeLEDCounter = 0;
						
						// Wait for release
						longPressCounter = LONG_PRESS_TIME_MS + 1000;  // prevent re-trigger
					}
				}
			}
			else {
				// Switch is released (active LOW, so P_SWITCH = 1 when released)
				if(switchWasPressed && longPressCounter < LONG_PRESS_TIME_MS && debounce == 0) {
					// Short press detected - toggle run/stop
					if(bRunning) {
						P_RUN = 0;					
						bRunning = 0;
						bInternalClockCounter = 0;  // reset internal clock counter
					}
					else {
						P_RUN = 1;					
						bRunning = 1;
						bBeatCount = 0;
						bBeatLEDCount = BEATLED_HIGH_TIME;
						bInternalClockCounter = 0;  // reset internal clock counter
					}
				}
				switchWasPressed = 0;
				longPressCounter = 0;
			}
		}
	}
}
