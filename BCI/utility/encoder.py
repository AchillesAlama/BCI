import serial
import serial.tools.list_ports as listports

def clearEncoding(serConnection):
    """Sets the current output of the encoder to zero"""
    serConnection.write(b'0\n')

def setEncoding(serConnection, eventCode):
    """Sets the corresponding pins on the encoder matching the given eventCode.
    Eventcode should be between 1-15, 0 signalizes no event. Newline must be sent
    to indicate end of transmission."""

    serConnection.write((str(eventCode) + "\n").encode())

def connectToEncoder():
    """Finds the correct COM port for the USB to UART chip to which the encoder
    is connected and returns a serial connection to this chip."""

    comPort = findComPort()

    #Set communication params, make sure that it is same as in encoder
    baudrate = 115200
    parity = serial.PARITY_NONE
    wordlength = serial.EIGHTBITS
    stopbits = serial.STOPBITS_ONE
    
    try:
        return serial.Serial(comPort, baudrate, wordlength, parity, stopbits)
    except Exception:
        return None

def findComPort():
    """Finds the COM port of the currently plugged in USB to UART chip.
    @returns(string): E.g. 'COM4' """
    descriptionPart = "USB to UART Bridge" #Part of current USB to Uart chip description
                                        #will need to change if you change device
    for port in listports.comports():
        if (descriptionPart in port.description):
            return port.device

def closeEncoder(serConnection):
    clearEncoding(serConnection)
    serConnection.close()