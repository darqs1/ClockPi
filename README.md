# ClockPi
Simple clock build with Raspberry Pi Zero W and 8 matrix led 8x8.
It display clock with seconds and date (day and month)

## What You need
- Raspberry Pi  (tested on RPi Zero and RPi 3B)
- 8 modules of matrix lex 8x8 connected serially with MAX7219

## How to connect?
|LED PIN|RPi PIN|Description|
|:-----:|:-----:|-----------|
|VCC|04|5V|
|GND|06|Ground|
|DIN|19|GPIO10 (SPI_MOSI)|
|CS|24|GPIO08 (SPI_CE0_N)|
|CLK|23|GPIO11 (SPI_CLK)|

## Permission problems
Library luma.core uses the spi interface. You have to add an user to spi group:
>sudo usermod -aG spi username

GPIO uses gpiomem device. You have to add an user to gpio group
>sudo usermod -aG gpio username

## Run Problems

If you get error:
```
libopenjp2.so.7: cannot open shared object file: No such file or directory
```
You need install
>sudo apt-get install libopenjp2-7

If you get error:
```
libtiff.so.5: cannot open shared object file: No such file or directory
```
You need install
>sudo apt install libtiff5

## Autostart with system
Add service file:
>sudo nano /etc/systemd/system/clockpi.service
```bash
[Unit]
Description=Clock on matrix led
After=multi-user.target

[Service]
Type=simple
Restart=always
KillSignal=SIGINT
User=<username>
ExecStart=/usr/bin/python3 /home/<username>/ClockPi/main.py

[Install]
WantedBy=multi-user.target
```
Replace `<username>` with Yours user

Reload the daemon
>sudo systemctl daemon-reload

Enable mocremote service at startup
>sudo systemctl enable clockpi.service

Start our service
>sudo systemctl start clockpi.service