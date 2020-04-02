# PiRadio
Internet radio for raspberry pi

## Literature
* [docker on raspberry pi (german)](https://www.dahlen.org/2019/06/docker-und-raspbian-auf-einem-raspberry-pi/)


## Installation (Headless)
Download raspbian buster lite and flash it to SD card.

### Wifi
* https://desertbot.io/blog/headless-raspberry-pi-4-ssh-wifi-setup
```bash
sudo -i
cd /MY_VOLUMES
touch boot/ssh
```
Set WPA passphrase
```
country=DE
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="NETWORK-NAME"
    psk="NETWORK-PASSWORD"
}
```

### First login
After first boot, the device will run some actions like resize_fs, apt-get update, ... and so on, so don't mind, if it's a little bit slow after first boot.
**DO NOT** turn off or hard-reboot the device, until all processes are finished!

Default password for raspbian buster is *raspberry*
```
ssh pi@YOUR_PI_HOSTNAME
passwd
apt update
apt upgrade
rpi-update
raspi-config
```
In raspi-config, set things like timezone, extend filesystem, language and so on.

**NOTE:** If your network seems to get stuck during upgrade operation, wait until the i/o LED of the pi stops flashing and power off the device.
Then remove SD card and check for existence of ```ssh``` and ```wpa_supplicant.conf``` files in ```/boot```.
It seems, that some upgrade operations remove these files...


### Hifiberry amp
Follow instructions here:

* https://www.hifiberry.com/docs/software/mixing-different-audio-sources/
* https://www.hifiberry.com/docs/software/configuring-linux-3-18-x/



### Disable updates
TODO


### Install Docker

```
sudo -i
echo -n "$(head -n1 /boot/cmdline.txt) cgroup_enable=cpuset cgroup_enable=memory" | tee /boot/cmdline.txt
apt remove docker docker-engine docker.io  runc
curl -fsSL https://get.docker.com -o - | sh
usermod -aG docker pi
reboot

```


## Play Music
### Radio Streams
https://strobelstefan.org/?p=4262




