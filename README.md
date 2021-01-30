#
## Connecting a Beosystem 3 to a non-B&amp;O TV

The Beosystem 3 is a wonderful media processor – especially if your speakers and rest of the system are Bang and Olufsen, though there is a problem in connecting the Beosystem 3 to other brands of TV.

This explains how you can actually do this using the Beosystem&#39;s Serial Port and HDMI CEC on the TV.

_Background_

The Beovision 4 monitors were designed to be used by the Beosystem 3, but the monitors themselves were Panasonic Professional Plasma Displays. The control of the display was handled by the Beosystem by sending commands via the Monitor serial port.

The command list can be found here – [https://panasonic.net/cns/prodisplays/support/rs232c\_commandlist\_prev.html](https://panasonic.net/cns/prodisplays/support/rs232c_commandlist_prev.html)

but basically, the only ones we are interested in is the power on and off.

The solution to allowing the Beosystem 3 to turn on and off the TV when the Beosystem itself turns on and off is detailed here:

Hardware Requirements

1. Raspberry Pi – most generations would be OK. You just need GPIO ports to connect a serial port connector to.
2. RS232 to TTL DB9 Serial Port connector – this has a 9-pin serial port and outputs the serial commands via wires that plug into the raspberry.

An example is shown here

[https://www.kiwi-electronics.nl/rs232-naar-ttl-seriele-poort-converter-met-db9-connector?lang=en](https://www.kiwi-electronics.nl/rs232-naar-ttl-seriele-poort-converter-met-db9-connector?lang=en)

They are also available on ebay.

1. Serial cable to connect the Beosystem 3 to the serial connector and HDMI cable to connect the raspberry to the TV.

Note the serial cable needs some pins shorted – pins 7&amp;8. 

I put the device into a hobby box so it would be tidy – there is, of course no need to do this. As an aside, you could short pins 7&amp;8 on this device rather than having to hack the serial cable.


Note you need the VCC connector to go to the 3v port on the raspberry – not the 5v as the GPIO pins of the raspberry only accept 3.3v – 5v could do some damage.

Connect the RXD and TXD, VCC (3.3v) and GND cables to the relevant ports on the raspberry.

Connect the HDMI cable from the raspberry to the TV. Note that you could put this in-line with the existing HDMI cable from the Beosystem 3 to the TV if you use a CEC injector – like the Pulse 8 CEC injector:

[https://www.pulse-eight.com/p/104/usb-hdmi-cec-adapter](https://www.pulse-eight.com/p/104/usb-hdmi-cec-adapter)

I&#39;ve tested both with and without this adaptor– but if you don&#39;t have this then you&#39;ll need to run two HDMI cables to the TV – one from the Raspberry and one from the Beosystem 3.

_Software Requirements_

For the Raspberry Pi, I used the Raspbian image – there are many tutorials on how to set this up in headless mode with ssh enabled – here&#39;s a good one:

[https://www.tomshardware.com/uk/reviews/raspberry-pi-headless-setup-how-to,6028.html](https://www.tomshardware.com/uk/reviews/raspberry-pi-headless-setup-how-to,6028.html)

Set up the Raspberry Pi to use the serial ports.

**Sudo raspi-config**

Choose:

5. Interfacing options

P6 Serial

No to the login shell but yes to have the serial port hardware enabled.

Then get the library that the python script uses to communicate with the serial port

**sudo apt install python-pip**

**python -m pip install pyserial**

You then need the HDMI-CEC libraries:

**sudo apt install cec-utils**

Download the ser.py code from this project and try it out. If you have some errors with missing libraries – just download those libraries and retry.

There are many guides on how to set up serial communication on the Raspberry – with some sample code to test – but you can see the communication between the Beosystem 3 and the raspberry if you set Debug = True in the ser.py code.

Note that the script switches the TV to HDMI1 – this is not necessary if you are using the Pulse-8 adaptor, but ensure that the port chosen is the one that the Beosystem 3 is connected to.

With that all working, you should see that when the Beosystem 3 is turned on, there will be a flurry of text going to the raspberry and what the script is looking for is

Power on: &quot;\x02PON\x03&quot;

Power off: &quot;\x02POF\x03&quot;

When it detects whichever one of those it receives, it sends the corresponding CEC command to the TV

Power on: os.system(&#39;echo &quot;on 0&quot;| cec-client -s \&gt; null&#39;)

Power off: os.system(&#39;echo &quot;standby 0&quot;| cec-client -s \&gt; null&#39;)
