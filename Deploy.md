# Deploy PiRadio

To deploy this app to a raspberry Pi device, make sure *git* is installed
```bash
sudo apt install git
```

## Checkout latest piradio
```bash
git clone https://github.com/ujac81/PiRadio.git
```
or if already checked out
```bash
cd ~/PiRadio
git pull
```


## Check Environment
```bash
cp .env.example .env
```
and change to your local settings.


## Remote-Build
On your developer machine run
```bash
make image save
scp piremote.tgz pi@RASPBERRY_NAME:~
```
