VERSION=$(or $(shell git describe --tags --always), latest)

ARTIFACTORY ?= ""

.ONESHELL:
.PHONY: run fmt prepare docker-build docker-run help

run: ## Run the application
	cd /application && poetry run python3 main.py

fmt: ## Format the code using pre-commit
	pre-commit run --all

prepare: ## Prepare the package and application dependencies
	cd /package && poetry install
	cd /application && poetry install

docker-build-httdataprep: ## Build the Docker image
	cd dataprep
	docker build \
	--build-arg http_proxy \
	--build-arg https_proxy \
	--build-arg no_proxy \
	-t ${ARTIFACTORY}sqoshi/httdataprep:latest \
	-t ${ARTIFACTORY}sqoshi/httdataprep:$(VERSION) \
	.

docker-build: ## Build the Docker image
	docker build \
	--build-arg http_proxy \
	--build-arg https_proxy \
	--build-arg no_proxy \
	-t ${ARTIFACTORY}sqoshi/hands-to-text:latest \
	-t ${ARTIFACTORY}sqoshi/hands-to-text:$(VERSION) \
	.

docker-run-httdataprep: ## Run the Docker container
	docker run --rm -it \
	-e DISPLAY=${DISPLAY} \
	--name httdataprep \
	--device /dev/video0:/dev/video0 \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	${ARTIFACTORY}sqoshi/httdataprep:latest

docker-run: docker-build  ## Run the Docker container
	docker run --rm -it \ 
	--name htt \
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