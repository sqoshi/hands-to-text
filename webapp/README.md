# webapp

![img](https://github.com/sqoshi/hands-to-text/blob/master/webapp/example.png)

## Introduction

This tool has been created for people that using ASL


## Usage

It is required to generate openapikey from [page](https://platform.openai.com/).

```shellscript
    docker run -e CHATGPT_KEY=<key>
```

0. Open localhost:8000
1. Start Camera
2. Use ASL to write sentence
3. Stop Camera
4. Correct Text
5. Send Chat
6. Read chat response, history of whole talk is saved

## Openapi

Interactive api is available under `/docs` endpoint.

![img](https://github.com/sqoshi/hands-to-text/blob/master/webapp/openapi.yml)
