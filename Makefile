
all: image


image:
	docker build --force-rm --rm --tag piradio_mpd --file Dockerfile.mpd .
	docker build --force-rm --rm --tag piradio_web --file Dockerfile.web .
	
clean:
	rm -f piradio.tgz
	docker rmi piradio_mpd
	docker rmi piradio_web
	docker image prune -f


save:
	docker image save --output piradio.tgz piradio_mpd piradio_web piradio_nginx

