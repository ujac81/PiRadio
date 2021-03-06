# Developer Notes for PiRadio

## Requirements
You'll need standard docker environment up and running.

### Installation
To run docker images on your x86_64 developer machine, install qemu-static
```bash
sudo apt-get install qemu-user qemu-user-static binfmt-support
```

## Build
Just build the docker files for *mpd* and *web* by running
```
make
```

## Run
Create environment
```bash
cp .env.example .env
```
and edit to appropriate settings. Start up docker-compose with development override:
```bash
docker-compose -f docker-compose.yml -f docker-compose-development.yml up web
```
open http://localhost:8000 to see result.
