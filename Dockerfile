FROM bitnami/minideb:stretch

RUN install_packages \
	python3

ADD app /app

CMD app/main.py

