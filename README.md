https://github.com/Emincer15/pi2nmea
https://youtu.be/zwbGnCj7czU

Login and keyring on pi
Whoi1930
Hardware:
Raspberry pi 4 b
Serial shield-https://www.digikey.com/en/products/detail/pi-supply/PIS-1362/9975881?utm_adgroup=&utm_source=google&utm_medium=cpc&utm_campaign=PMax%20Shopping_Product_Low%20ROAS%20Categories&utm_term=&utm_content=&utm_id=go_cmp-20243063506_adg-_ad-__dev-c_ext-_prd-9975881_sig-CjwKCAjwoJa2BhBPEiwA0l0ImKGAW_Hsr3LgzE88S8Val8CGvhFHrg-Kthg3VNJG2SXT43Kf2hM6dBoC0lkQAvD_BwE&gad_source=1&gclid=CjwKCAjwoJa2BhBPEiwA0l0ImKGAW_Hsr3LgzE88S8Val8CGvhFHrg-Kthg3VNJG2SXT43Kf2hM6dBoC0lkQAvD_BwE
Garmin 742xs chartplotter.
 Sabrent rs232 adapter for using opencpn-https://sabrent.com/products/cb-rs232?srsltid=AfmBOoq4TRKr8IPFrC45u7-11XtOLTjUwVpHwGPb1cFPBl5jooQO856t
Raspberry pi settings:
Enable serial port
sudo raspi-config and find serial in the Interfaces menu.
Answer NO to the question about login shell.
Answer YES to the question about serial hardware port.
For rabbitmq connection in the lab the pi needs to be on i54 field guests or eduroam wifi
Lab Chartplotter settings:
manuals-tempe™ | Garmin Customer Support
Wiring-
GPSMAP 702/902 Series - Power/NMEA 0183 Cable
Ignore orange and yellow wires
blue(tx+) to port two on pi serial(rx, I have as blue)
brown(rx+ to port three on pi serial(tx, I have as brown)
black(ground) to port five on pi serial(ground, I have as black). NMEA 0183 uses rs422 which has a tx-(gray) and rx-(violet). Connect those to ground. And ground from the power adapter should be connected to ground. So five different wires connected to ground.
red(power) to power from power adapter
Make sure it is on nmea 0183 high speed: Home-settings-communications-nmea 0183 setup-port types-nmea input-nmea high speed
Make sure aton is on: open the chart-menu-layers-chart-navaid-aton GPSMAP Owner's Manual - AIS Aids to Navigation
If you want to update the lab's version of chartplotter, sd card size needs to be under 32 gb due to our chartplotter model, use the Garmin express app on the computer. New exFAT Support on Garmin Marine Chartplotters
virtual environments:
Virtual environments are internal to the computer. So if you want to edit the code on a different computer you can’t use the virtual environment from the pi. This is because if you place the venv in a directory on a new computer, the actual address stays as the old computer which makes it not usable on the new computer. So the best way to create a new virtual environment is to do  pip freeze > requirements.txt when you change the virtual environment. This will automatically make a file that lists all the libraries in the virtual environment. On the new computer you are editing on you create a new virtual environment. Then in that one you do pip install -r requirements.txt to install the libraries. When you create the virtual environment on the new computer, it shouldn't be in the project directory. (note: in the git there are currently two virtual environments. .venv which is from my mac when I was doing the programming originally and .venvpi which is what the pi uses. If you want to edit and run code on your own computer, this new virtual environment doesn’t need to be added to the project directory. You can make it outside and activate it and download necessary files to it using instructions above)
Transferring venv to a different computer. : r/learnpython
NMEA 0183 messages
NMEA 2000 is the newer software, but the boats we are going to be talking to initially use NMEA 0183. Also, since there are converters from the old software to new but not the other way around, it makes more sense to code it with NMEA 0183.
The way these messages are formatted is a start delimiter($ or !), two letter talker id, a three letter type code, and then the message. Then there is a checksum which is the 8-bit XOR of all characters in the sentence, excluding the "$", "I", or "*" characters; but including all "," and "^". It is encoded as two hexadecimal characters (0-9, A-F), the most-significant-nibble being sent first. Sentences are terminated by a <CR><LF> sequence.
I am sending a AIS type 21 message through NMEA
Here are the other types of NMEA messages I was considering
Start delimiter-maybe AG for autopilot? This has a comprehensive list. NMEA Revealed
Type code: 
TLL-a “target’s” lat and lon
TTM-a message for a tracked target 
RSD-radar system data
TLB-target label (maybe if new whale shows up)
TLL-target latitude and longitude
TTM-tracked target message
ZDL-time and distance to variable point
Library for encoding NMEA messages(I don’t use this because the AIS library I have does this automatically) https://github.com/Knio/pynmea2/tree/master. Here are the types the library supports pynmea2/pynmea2/types/talker.py at master · Knio/pynmea2 · GitHub
This has everything about NMEA message formats and types NMEA Revealed
Here is some other info: NMEA-0183 Sentences for GPS Receivers, https://github.com/Knio/pynmea2/blob/master/NMEA0183.pdf, https://w3.cs.jmu.edu/bernstdh/web/common/help/nmea-sentences.php, http://lefebure.com/articles/nmea/, The NMEA 0183 Information sheet | Actisense, 
My problem with traditional NMEA messages(not AIS) was that chartplotter seemed to accept them, but I didn’t see anything show up on screen. With AIS that was fixed.
Ais messages(show special one with whale, mention binary message)
Comprehensive guide: AIVDM/AIVDO protocol decoding
Python library-GitHub - M0r13n/pyais: AIS message decoding and encoding in Python (AIVDM/AIVDO)
!AIVDM-from another station !AIVDO from own ship. I don’t think it matters which one we send.
AIS is traditionally broadcast over RF and picked up by an AIS receiver which is then written through NMEA to chartplotter. The Raspberry pi instead creates these AIS messages based on whale data and simulates it as if it's coming off an AIS receiver.
How AIS messages are formatted. The python library does all this
Here is a typical AIVDM data packet: !AIVDM,1,1,,B,177KQJ5000G?tO`K>RA1wUbN0TKH,0*5C
Field 1, !AIVDM, identifies this as an AIVDM packet.
Field 2 (1 in this example) is the count of fragments in the currently accumulating message. The payload size of each sentence is limited by NMEA 0183’s 82-character maximum, so it is sometimes required to split a payload over several fragment sentences.(for us it is only going to be one packet. We aren’t sending a lot of info)
Field 3 (1 in this example) is the fragment number of this sentence. It will be one-based. A sentence with a fragment count of 1 and a fragment number of 1 is complete in itself.
Field 4 (empty in this example) is a sequential message ID for multi-sentence messages. (this is empty for us)
Field 5 (B in this example) is a radio channel code. AIS uses the high side of the duplex from two VHF radio channels: AIS Channel A is 161.975Mhz (87B); AIS Channel B is 162.025Mhz (88B). In the wild, channel codes '1' and '2' may also be encountered; the standards do not prescribe an interpretation of these but it’s obvious enough.(this doesn’t matter for us because we aren’t actually using radio)
Field 6 (177KQJ5000G?tO`K>RA1wUbN0TKH in this example) is the data payload. (This is dependent on the type of AIS message
Field 7 (0) is the number of fill bits requires to pad the data payload to a 6 bit boundary, ranging from 0 to 5. 
The *-separated suffix (\*5C) is the NMEA 0183 data-integrity checksum for the sentence, preceded by "*". It is computed on the entire sentence including the AIVDM tag but excluding the leading "!".
Field six
Field 6 is encoded in a weird way. If you are interested, look at the first AIS link I sent. The library encodes it for you though. 
How to use the library-
Choose message you want(I am using message 21)
Make a dictionary with the fields corresponding to the values. You can find the fields here: https://github.com/M0r13n/pyais/blob/master/docs/messages.rst
Use the encode_dict method to create message
There are 27 types of AIS messages. Here are the ones I was considering:
21-Aid to navigation report(ATON)-this is what I’m using. This plots on the map as if there would be a buoy or something like it. So I am plotting on the map that there is a danger buoy where the whale is. You specify the AID type.
1-position report, class A(not using because this makes it seem as if there is a ship)
14-safety related broadcast message-sends text, but no location so doesn’t show up on map-not using
6/8-binary addressed/broadcast message.(I have a lot to say on this because this seemed promising but it didn’t work for me)
All the other types of messages have specific sections of information to fill out. You can see this in the python library. But types 6 and 8 were created to send even more types of data. So although it seems there are only 27 types, types 6 and 8 all have these very specific types that you can send within them. The thing is, there are so many different types and some are very niche, the chartplotter software doesn’t seem to know how to decode them. The python library doesn’t know how to encode/decode them. It just has an open space for data where you are supposed to enter in this data already encoded into bytes.
This extra data field is filled out based on a DAC (designated area code) and FID (Functional ID) pair. The  sections to fill out for this data field are different corresponding to the DAC/FID pair. That’s why I’m not sure if chartplotters even know all this info because different AIS databases have/lack certain DAC/FID pairs and the library for encoding/decoding AIS doesn’t have any info for creating this data section. The library wants it all already encoded. 
“Although shipborne AIS equipments are capable of receiving AIS Application-Specific Messages, they may not be properly processed and displayed. [SN.1/Circ.[…] provides general Guidance for the presentation and display of AIS Application-Specific Messages.] “Ref. T2-OSS/2.7.1 SN.1/Circ.289 2 June 2010 GUIDANCE ON THE USE OF AIS APPLICATION-SPECIFIC MESSAGES 1 The Maritime Safety Commi “2.2 The display capability of AIS Application-Specific Messages is not part of the mandatory functions of the Minimum Keyboard and Display (MKD). The display of the information transmitted by AIS Application-Specific Messages requires external hardware and dedicated software in addition to the AIS equipment. “
Here are the interesting types of binary messages that seemed relevant
This is the specific type 6/8 message:IMO289-Ref. T2-OSS/2.7.1 SN.1/Circ.289 2 June 2010 GUIDANCE ON THE USE OF AIS APPLICATION-SPECIFIC MESSAGES 1 The Maritime Safety Commi
DAC=1 (international)
FID=23
This message is for an “Area Notice.” these are some of the options of what could be in the area:
Caution Area: Marine mammals habitat
Caution Area: Marine mammals in area - reduce speed
Caution Area: Marine mammals in area - stay clear
Caution Area: Marine mammals in area - report sightings
Below I explain how I created this message even without the library having these fields
This is the specific type 8 message that supposedly corresponds to “whalenotice”: AIS Message Definition - Human Readable Form(even in the note it says that it is an LNG terminal project. This doesn't seem to be actually a thing yet)
The DAC is 366 for the US and the FID is 63.
I didn’t actually play around with this since the one above didn’t work and this seemed more novel
Here is a longer list of DAC/FID pairs for binary payloads-Binary AIS Message Decoding Status
How I encoded binary payloads
Created my own message class based on the format of the classes for the types in the pyais library. I called this file BinaryMessageTypes.py. Right now I only have a class for IMO289.
For the default values, I just entered all the values I wanted. 
Then to encode this to bits, I looked through the pyais library and looked how they did it for the other types of messages. This is with two lines of code that you can see that I wrote in type6.py and type8.py files
Then I encoded the binary message type as bytes as a field for MessageType6 the way you would enter any field.
I was trying to replicate this example of IMO289 to make sure my code worked. https://arundaleais.github.io/docs/ais/binary_1_22.gif
In an AIS message when you are specifying location, lat and lon need to be formatted in a weird way(minutes/1000). But the library does this for you. In the lat and lon sections you enter regular decimal degrees.
For each of the AIS messages, there is a field for an MMSI. this is the unique identifier of the radio the AIS message is being sent from(since AIS is sent over radio). I have found it doesn’t matter for our purposes what MMSI we write. The chartplotter will display it no matter what. But here is info on MMSIs in case it does matter
Each MMSI is 9 characters long. 3 of those characters are the MID which is the country that it is coming from. This website has a comprehensive list of MIDs Vessel flag codes | Spire Maritime Documentation
Depending on where the MID is in the MMSI, it specifies what kind of radio the message is coming from
the one the starts with 99 looks relevant for message 21
According to this website, ATONs(message 21) can be sent starting from 993 also. The website also says messages 6 and 8 can be sent starting from 993 or from base stations. Types Of Automatic Identification Systems (Per ITU-R M.1371 And IEC Standards) | Navigation Center
Opencpn-Used this originally to simulate chartplotter
Basic User Manual [OpenCPN]
Download maps to make it look more realistic-Instructions for this at beginning of manual
To set up serial connection
Settings-connections-add connection-select right port, make sure baud is 38400. This baud rate is bad on the computer, for me only ⅓ messages went through clearly but it is what chartplotter takes so the code on pi outputs this baud. Make sure protocol is NMEA 0183
To see messages received in settings-connections-click show NMEA debug window
To test out messages internally without using serial
Download NmeaConverter_pi from extensions.
To send a message. Click on it in extensions, go to preferences, click new, paste the message you want, click send every second.
Serial connection on mac
It was hard to find the correct driver for rs232. For me it was the prolific driver, but not the one on the web because that doesn’t work for ARM macs. You need to download it from the Mac app store. It’s called PL2303
Supervisord settings
In repo
Rabbit_mq
In the sending that Fox gave me, three lines need to be included for python to not throw error:
null=None
true=True
false=False
Code comments
More comprehensive code comments on repo
3d printed design
case:https://a360.co/3X7oz1R
Raspberry pi for reference: https://a360.co/4fTRRsi
If you need to edit the case, let me know what email I should give editing permissions to.
Next steps
Nmea 2000
There is an adapter that takes NMEA 1083 serial connection on one end and the other end is a NMEA 2000 connector. The adapter has internal code to transfer the message to a NMEA 2000 message. https://www.yachtd.com/products/nmea0183_gateway.html?gad_source=1&gclid=Cj0KCQjwiOy1BhDCARIsADGvQnBv3XaakEoZaG8gzBLb-ZPZSOROd64vRonO9EPniyK4suohR9ODDPcaAp1yEALw_wcB
There is also this one where you can add your own python code in it. Doesn’t make sense to buy. https://www.yachtd.com/products/python_gateway.html. For this python one they even have an example python code of converting type 1, 2, 3, and 14 AIS messages from NMEA 1083 to 2000. For type 21 would need to modify this code. But I don’t think this is even necessary because the non-python one says it does AIS conversion of certain types automatically(at the bottom of the manual it lists the types and type 21 is included) whereas with the python you would have to code it yourself.
You could also try to code it yourself without using an adapter. But then you would have to find a way for py to connect to the NMEA 2000 connector which I don’t think there is a shield for. I think the first adapter is the best betI found this NMEA2000 library in C++. NMEA2000 Library: List of supported NMEA2000 PGNs
More info on virtual atons, very relevant for next three ideas:https://www.e-navigation.nl/sites/default/files/1081%20Virtual%20AtoN.pdf
To show multiple whales-
incorporate whale id info in MMSI to keep track of whales to update positions of ATON to track the whale so it moves
When you have the same MMSI and you change the position, it deletes the previous one and moves it elsewhere.(this could be a solution to the next problem. Maybe move any no longer tracked whales to a spot in the middle of nowhere)
Right now markers stay indefinitely. After looking through the web, I can't find out how to remove markers. I think it's dependent on chartplotter software.
A possible makeshift solution is to move any longer tracked whales to a irrelevant location like a island in the middle of nowhere or lat 0 lon 0
Here's some websites i was looking through to try to solve this problem:
This website basically says that it is up to chartplotter for when they disappear-https://www.e-navigation.nl/sites/default/files/1081%20Virtual%20AtoN.pdf
https://www.navcen.uscg.gov/ais-aton-report
https://www.navcen.uscg.gov/sites/default/files/pdf/AIS/iec62288(Ed3)%3DAnnex_L_AtonStatusBits.pdf
https://www.cds.ca/resource/en/57
https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-5-201402-I!!PDF-E.pdf
https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-1-200108-S!!PDF-E.pdf
More mmsi info: How legal is this/how should we make our mmsi?
The mmsi number represents the virtual aton itself, not the transmitting source. -https://www.e-navigation.nl/sites/default/files/1081%20Virtual%20AtoN.pdf
https://www.navcen.uscg.gov/mmsis-for-ais-private-aids-to-navigation
This looks like how we’re supposed to format mmsi-https://www.navcen.uscg.gov/mmsis-for-ais-private-aids-to-navigatio
APPLYING FOR A LICENSE for private virtual aton-need to do by country(i don’t know if we need a license since it is all internal anyway, but I guess its good to have it official
This is for the US:
Note, AIS ATON stations operated in the U.S., other than by the U.S. Coast Guard, require Federal Communications Commission (FCC) or National Telecommunication Information Agency (NTIA) radio type-certification and proper licensing, which they will not grant without prior consultation with the U.S. Coast Guard. Requests for approvals to use AIS as or on a Private ATON may be directed to  cgnav@uscg.mil, and must include either a CG Form 2554 or 4143 following these instructions. For a listing of FCC type-certified AIS ATON devices, search Equipment Class--AIS at FCC OET Equipment Authorization Search Form.
For further information on AIS ATON and their uses, please refer to the various IALA Guidelines and Recommendations (i.e., G1062, Establishment of AIS as an AtoN).
Canada:
https://ised-isde.canada.ca/site/spectrum-management-telecommunications/en/form-g-ais-aids-navigation-aton
