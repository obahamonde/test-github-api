IMAGE_NAME = $(shell basename $(PWD))

containers:
	python app.py build

prune:
	python app.py prune

build: containers
	docker build -t $(IMAGE_NAME) .

run: build
	docker run -d --net=host -p 8080:8080 -v $(PWD):/app $(IMAGE_NAME)

dev:
	gunicorn main:app --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker --workers 1 --threads 1 --timeout 0 --reload

# Define phony targets explicitly
.PHONY: containers prune build run dev do

# Default target
do: containers prune build run
IMAGE_NAME = $(shell basename $(PWD))

containers:
	python app.py build

prune:
	python app.py prune

build: containers
	docker build -t $(IMAGE_NAME) .

run: build
	docker run -d --net=host -p 8080:8080 -v $(PWD):/app $(IMAGE_NAME)

dev:
	gunicorn main:app --bind 0.0.0.0:8080 --worker-class aiohttp.GunicornWebWorker --workers 1 --threads 1 --timeout 0 --reload

# Define phony targets explicitly
.PHONY: containers prune build run dev do

# Default target
do: containers prune build run
