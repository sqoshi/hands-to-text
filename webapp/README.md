# webapp

![img](https://github.com/sqoshi/hands-to-text/blob/master/webapp/example.png)

## Introduction

This tool has been created for hard of hearing individuals, it is web application with camera and few button that allow to ask questions to ChatGPT, with ASL letters. And containered with docker, so everybody can download it and use it.

## Usage

It is required to generate openapikey from [page](https://platform.openai.com/).

```shellscript
    docker run --network host \
        --name htt --rm -it \
        -e CHATGPT_KEY=<KEY> \
        -e DISPLAY=${DISPLAY} \
        --device /dev/video0:/dev/video0 \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        ghcr.io/sqoshi/hands-to-text:0.1.1
```

0. Open localhost:8000
1. Start Camera
2. Use ASL to write sentence
3. Stop Camera
4. Correct Text
5. Send Chat
6. Read chat response, history of whole talk is saved

## Workflow

![img](https://github.com/sqoshi/hands-to-text/blob/master/webapp/plant.png)


## Openapi

Interactive api is available under `/docs` endpoint.

![img](https://github.com/sqoshi/hands-to-text/blob/master/webapp/openapi.yml)

## Technologies

Application has been fully written in `python` with framework `fastapi` to make web ui for every user, best practices consider to use `pydantic` models for error prune communication between backend api and frontend templates with `javascripts`. Application has somekind of secrets as `chatgpt` apikey, so `pydantic_models` has been used to hide secrets in injectable enviornment. `openai` library has been used for communication with ChatGPT either to answer the question or correct the text. For models managements package `hands-to-text` designed and created specially for this web application. Some of models require the hand detection, so for finding a box with hand we used `mediapipe`. Application has been deployed with modern `uvicorn`. And finally whole program is stored as a `docker` container, so everybody can run it on local machine, having just key for `chatgpt`.
