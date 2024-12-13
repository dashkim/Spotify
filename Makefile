
IMAGE_NAME = spotify-project
CONTAINER_NAME = spotify-container
PORT = 5000

all: build run

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -p $(PORT):5000 --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

clean: stop
	docker rmi $(IMAGE_NAME)

install:
	pip install -r requirements.txt

run_local:
	python app.py