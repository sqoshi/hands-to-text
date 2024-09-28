VERSION=$(or $(shell git describe --tags --always), latest)

ARTIFACTORY ?=

.ONESHELL:
.PHONY: run fmt prepare docker-build docker-run help

run: ## Run the webapp
	webapp/.venv/bin/python3  uvicorn main:app --reload

test: ## Run tests
	package/.venv/bin/python3 -m pytest package/tests

fmt: ## Format the code using pre-commit
	pre-commit run --all

prepare: ## Prepare the package and webapp dependencies
	cd ./package && poetry install && cd ..
	cd ./webapp && poetry install && cd ..

docker-build: ## Build the Docker image
	docker build \
	--build-arg http_proxy \
	--build-arg https_proxy \
	--build-arg no_proxy \
	-t ${ARTIFACTORY}sqoshi/hands-to-text:latest \
	-t ${ARTIFACTORY}sqoshi/hands-to-text:$(VERSION) \
	.

docker-run: docker-build ## Run the Docker container
	docker run --network host \
	--name htt --rm -it \
	--name httdataprep \
	-e DISPLAY=${DISPLAY} \
	--device /dev/video0:/dev/video0 \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	${ARTIFACTORY}sqoshi/hands-to-text:latest

help: ## Print help with command name and comment for each target
	@echo "Available targets:"
	@awk '/^[a-zA-Z\-_0-9]+:/ { \
		helpMessage = match(lastLine, /^# (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 1, length($$1)-1); \
			helpComment = substr(lastLine, RSTART + 2, RLENGTH - 2); \
			printf "  %-20s %s\n", helpCommand, helpComment; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
