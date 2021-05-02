# Tally lights for vMix

Python program implementing tally lights for vMix with Raspberry Pi Zero and PIMORONI Unicorn Hat Mini

# Before You Start

You should have a Raspberry Pi Zero WH with Raspberry Pi OS (the "lite" version is sufficient) that is already connected to the network by wifi. Make sure it is in the same IP address subnet like the PC running the vMix software.
Additionally, you will need a PIMORONI UNICORN HAT MINI connected to the GPIO pins of the Pi and install the corresponding software from PIMORONI - see instructions on the [PIMORONI website](https://learn.pimoroni.com/tutorial/hel/getting-started-with-unicorn-hat-mini).
Finally, you need to activate the web server of vMix under "Settings | Web Controller". 
The python program in this project will read the corresponding tally website generated by vMix, parse it and control the LEDs according to the current status of the camera input with the corresponding name, i.e. the colors used for the LEDs depend on the settings in vMix.

# Installation

1. Open the terminal on your Raspberry Pi
2. Install pip, git and the dependencies for pycurl (pycurl is used for parsing the web site generated by vMix)
    ```
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install python-pip
    sudo apt-get install git
    sudo apt install libcurl4-openssl-dev libssl-dev
    ```
3. Install some dependencies for the PIMORONI stuff which are not avaliable on a Raspberry Pi OS Lite
    ```
    sudo apt-get install python-pil
    ```
4. Install pycurl
    ```
    pip install pycurl
    ```
    If the above installation procedure should not work, there might be an updated installation procedure [here](http://pycurl.io/docs/latest/install.html#install)
5. Clone this project

    ```
    cd
    git clone https://github.com/hobbymusician/vmix-tally-pi.git
    ```
6. Make the python script executable
   ```
    cd vmix-tally-pi/vmix-tally-pi/
    chmod 755 tally.py
    ```
    The usage of the script is
    ```
    tally.py <camera input name> <ip address of vMix computer> [<port>] 
    ```
    If the port is omitted, it defaults to 8088.
    
    E.g. type the following to connect to the vMix PC IP address 192.168.1.1 to generate the tally light for the camera named "Camera 1":
    ```
    ./tally.py "Camera 1" 192.168.1.1
    ```
    If you would use port 12345 isntead of 8088, you would type
    ```
    ./tally.py "Camera 1" 192.168.1.1 12345
    ```
    Press Ctrl + C at any time to exit.

To start the phyhon script automatically when the Raspberry Pi is starting up, you may add it to rc.local:
```
sudo nano /etc/rc.local
```
Add the following line to rc.local just before the final "exit 0" (eventually modify the path if you were using a different one) and save the file using ^O (Ctrl-O):
```
sudo -H -u pi /home/pi/vmix-tally-pi/vmix-tally-pi/tally.py "Camera 1" 192.168.1.1
```
That's it!
After a
```
sudo reboot
```
the Raspberry Pi shoult automatically start the tally light (initially, there might be an error message saying that it could not connect, but as soon as the vMix PC is found, the tally light should light up with the colour shown in vMix.
