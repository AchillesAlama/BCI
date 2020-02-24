/*
 * File: fwMod_eventEncodingInAux.ino
 * Date: 19-02-2020
 * Author: Ludwig von Feilitzen
 * Description:
 *  This firmware mod adds the event/image encoding to the samples being sent. Encoding 0 is used for indicating  
 *  that the samples don't belong to any particular event. It is assumed that the Cyton board pins D11, D12, D13 and D18
 *  are connected correctly to some external encoder (currently using Arduino Nano and a USB to TTL chip). D18 is MSB.
 *  
 *  Notes:
 *  Setting useAccel to false modifies the stop byte of each sample (see Cyton data format on OpenBCI website) 
 *  which can cause the PC side code to give errors instead of parsing
 *  incoming data to samples. Therefore the expected end byte must be changed, or we must subclass the OpenBCICyton 
 *  object and overwrite the function that verifies the end byte. Which strategy to go with is not chosen as of the moment
 *  of writing.
 *  
 *  This file can be uploaded to the Cyton board in order to modify its functionality. The file is based on the default 
 *  code which runs on the board when shipped from factory. All our additions are marked by:
 *  "######################## OUR ADDITION ############################". Don't change anything that is not within these 
 *  markers.
 *  
 *  For further instructions on how to program the Cyton board, please find a guide here: https://docs.openbci.com/docs/02Cyton/CytonProgram.
 *  

*/

#include <DSPI.h>
#include <OBCI32_SD.h>
#include <EEPROM.h>
#include <OpenBCI_Wifi_Master_Definitions.h>
#include <OpenBCI_Wifi_Master.h>
#include <OpenBCI_32bit_Library.h>
#include <OpenBCI_32bit_Library_Definitions.h>

#include <Time.h>

// Booleans Required for SD_Card_Stuff.ino
boolean addAccelToSD = false; // On writeDataToSDcard() call adds Accel data to SD card write
boolean addAuxToSD = false; // On writeDataToSDCard() call adds Aux data to SD card write
boolean SDfileOpen = false; // Set true by SD_Card_Stuff.ino on successful file open

//######################## OUR ADDITION ############################
int d17 = 17;
int d12 = 12;
int d11 = 11;
//######################## OUR ADDITION END ########################

void setup() {
  // Bring up the OpenBCI Board
  board.begin();

  //######################## OUR ADDITION ############################
  board.useAccel(false);
  //######################## OUR ADDITION END ########################
  
  // Bring up wifi
  wifi.begin(true, true);

  //######################## OUR ADDITION ############################
  //pinMode(d17, INPUT);
  //pinMode(d12, INPUT);
  //pinMode(d11, INPUT);
  //######################## OUR ADDITION END ########################
}

void loop() {
  if (board.streaming) {
    if (board.channelDataAvailable) {
      // Read from the ADS(s), store data, set channelDataAvailable flag to false
      board.updateChannelData();

      //######################## OUR ADDITION ############################
      int d17_state = digitalRead(d17);
      int d12_state = digitalRead(d12);
      int d11_state = digitalRead(d11);
      board.auxData[0] = 0x00 | (d17_state << 2) | (d12_state << 1) | (d11_state); 
      //######################## OUR ADDITION END ########################
      
      // Check to see if accel has new data
      if (board.curAccelMode == board.ACCEL_MODE_ON) {
        if(board.accelHasNewData()) {
          // Get new accel data
          board.accelUpdateAxisData();

          // Tell the SD_Card_Stuff.ino to add accel data in the next write to SD
          addAccelToSD = true; // Set false after writeDataToSDcard()
        }
      } else {
        addAuxToSD = true;
      }

      // Verify the SD file is open
      if(SDfileOpen) {
        // Write to the SD card, writes aux data
        writeDataToSDcard(board.sampleCounter);
      }

      board.sendChannelData();
    }
  }

  // Check serial 0 for new data
  if (board.hasDataSerial0()) {
    // Read one char from the serial 0 port
    char newChar = board.getCharSerial0();

    // Send to the sd library for processing
    sdProcessChar(newChar);

    // Send to the board library
    board.processChar(newChar);
  }

  if (board.hasDataSerial1()) {
    // Read one char from the serial 1 port
    char newChar = board.getCharSerial1();

    // Send to the sd library for processing
    sdProcessChar(newChar);

    // Read one char and process it
    board.processChar(newChar);
  }

  // Call the loop function on the board
  board.loop();

  // Call to wifi loop
  wifi.loop();

  if (wifi.hasData()) {
    // Read one char from the wifi shield
    char newChar = wifi.getChar();

    // Send to the sd library for processing
    sdProcessChar(newChar);

    // Send to the board library
    board.processCharWifi(newChar);
  }

  if (!wifi.sentGains) {
    if(wifi.present && wifi.tx) {
      wifi.sendGains(board.numChannels, board.getGains());
    }
  }
}
