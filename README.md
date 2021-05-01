# Tally lights for vMix

Python program implementing tally lights for vMix with Raspberry Pi Zero and PIMORONI Unicorn Hat Mini

# Before You Start

You should have a Raspberry Pi Zero WH with Raspberry Pi OS (the "lite" version is sufficient) that is already connected to the network by wifi. Make sure it is in the same IP address subnet like the PC running the vMix software.
Additionally, you will need a PIMORONI UNICORN HAT MINI connected to the GPIO pins of the Pi and install the corresponding software from PIMORONI - see instructions on the [PIMORONI website](https://learn.pimoroni.com/tutorial/hel/getting-started-with-unicorn-hat-mini).
Finally, you need to activate the web server of vMix under "Settings | Web Controller". 
The python program in this project will read the corresponding tally website generated by vMix, parse it and control the LEDs according to the current status of the camera input with the corresponding name, i.e. the colors used for the LEDs depend on the settings in vMix.

# Installation

1. Open the terminal on your Raspberry Pi

2. Clone this project

    ```
    git clone https://github.com/hobbymusician/vmix-tally-pi.git
    ```

3. Make the python script executable
   ```
    cd vmix-tally-pi/vmix-tally-pi/
    chmod 755 tally.py
    ```
4. The usage of the script is
    ```
    tally.py <camera input name> <ip address of vMix computer> [<port>] 
    ```
    If the port is omitted, it defaults to 8088.
    
    E.g. type the following to connect to the vMix PC IP address 192.168.1.1 to generate the tally light for the camera named "Camera1":
    ```
    ./tally.py Camera1 192.168.1.1
    ```
    Press Ctrl + C at any time to exit.

To start the phyhon script automatically when the Raspberry Pi is starting up, you may add it to rc.local:
```
sudo nano /etc/rc.local
```
Add the following line to rc.local (eventually modify the path if you were using a different one):
```
/etc/home/vmix-tally-pi/tally.py 192.168.1.1 8088 Camera1
```
That's it!
