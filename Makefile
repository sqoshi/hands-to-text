VERSION=$(or $(shell git describe --tags --always), latest)

ARTIFACTORY ?=

.ONESHELL:
.PHONY: run fmt prepare docker-build docker-run help

run: ## Run the webapp
	webapp/.venv/bin/python3.12 webapp/httfe/main.py

test: ## Run tests
	export CHATGPT_KEY=11111111
	cd package && poetry run pytest tests ; cd ..
	cd webapp && poetry run pytest tests ; cd ..

fmt: ## Format the code using pre-commit
	pre-commit run --all

prepare: ## Prepare the package and webapp dependencies
	cd ./package && poetry update && poetry up && poetry install && cd ..
	cd ./webapp && poetry update && poetry up && poetry install && cd ..

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
