# Under Development! Please wait for initial release!
### This version of Pi Fusion is not really working and not released yet.
### This site is still a construction site. Work in progress...
-------------------------------------------------------------
# Pi Fusion
...

## Status:
Pi Fusion is still in the development stage and some things are still not working or flawed. Some things are dotted with the hot needle or quick and dirty programmed. Pi Fusion is constantly being expanded and improved

## Features:
....

### Screenshots:
...

## Requirements:

- Hardware: Raspberry Pi
  - Tested with: Raspberry Pi 4B (4GB)
- Operating system: Raspbian GNU Linux
  - Tested with: Rasbian GNU Linux Buster (Kernel 4.19)
- Software packages:
  - Python 3.7.3+
    - Python package: pysimplegui (4.19.0+)
    - Python package: psutil (5.7.0+)

## Installation:

### Install necessary packages

```
sudo apt-get update && sudo apt-get dist-upgrade
sudo apt-get install -y python3-gpiozero git python3-picamera
pip3 install pysimplegui
pip3 install psutil
cd ~
git clone https://github.com/ElectroDrome/raspberry-pi-fusion.git
```
#### Upgrade Python packages (if necessary)
```
python3 -m pip install --upgrade pysimplegui
python3 -m pip install --upgrade psutil
```
## Update:

### Automatically
 Update:
Go in Pi Fusion to the settings. Here is automatically checked if a new version is present. If a new version is available you can click **Install update**.
### Manual
```
cd ~
cd raspberry-pi-fusion
git pull https://github.com/ElectroDrome/raspberry-pi-fusion.git master
```
## Start Pi Fusion
```
cd ~
cd raspberry-pi-fusion
python3 pifusion.py
```