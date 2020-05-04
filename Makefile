
PI_HOST := piradio

all: image


image:
	docker build --force-rm --rm --tag piradio_mpd --file Dockerfile.mpd .
	docker build --force-rm --rm --tag piradio_web --file Dockerfile.web --target web .
	docker build --force-rm --rm --tag piradio_nginx --file Dockerfile.web --target nginx .
	
clean:
	rm -f piradio.tgz
	docker rmi piradio_mpd
	docker rmi piradio_web
	docker rmi piradio_nginx
	docker image prune -f


save:
	docker image save --output piradio.tgz piradio_mpd piradio_web piradio_nginx


deploy:
	scp piradio.tgz pi@$(PI_HOST):~
	rm -f piradio.tgz

install-remote:
	ssh pi@$(PI_HOST) docker load --input /home/pi/piradio.tgz


load:
	docker load --input ~/piradio.tgz
	docker image prune -f

full-deploy: image save deploy install-remote

web-deploy:
	docker build --force-rm --rm --tag piradio_web --file Dockerfile.web --target web .
	docker image save --output piradio.tgz piradio_web
	scp piradio.tgz pi@$(PI_HOST):~
	ssh pi@$(PI_HOST) docker load --input /home/pi/piradio.tgz
	rm -f piradio.tgz
