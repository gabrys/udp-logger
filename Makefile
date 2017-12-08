LOG_DIR = /var/log/udp-logger
LISTEN_HOST = 127.0.0.1
LISTEN_PORT = 10000

.PHONY: run
run:
	sudo docker build -t udp-logger -f ./Dockerfile .
	sudo docker run --rm \
		--publish $(LISTEN_HOST):$(LISTEN_PORT):10000/udp \
		--volume $(LOG_DIR):/data \
		udp-logger
