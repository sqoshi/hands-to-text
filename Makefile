VERSION=$(or $(shell git describe --tags --always), latest)


.PHONY:	run-application  

.ONESHELL:
fmt:
	pre-commit run --all

build-package-python:
	cd package
	rm -rf ../application/dist
	poetry update
	poetry build --output ../application/dist

build-app-docker: build-package-python
	cd application
	docker build \
	-t ${ARTIFACTORY}sqoshi/hands-to-text:latest \
	-t ${ARTIFACTORY}sqoshi/hands-to-text:$(VERSION) \
	-f Dockerfile \
	.

run-app-docker:
	docker run --rm -it --network host hands-to-text:latest 