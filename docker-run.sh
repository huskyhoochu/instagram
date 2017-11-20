#!/bin/bash
# 도커 베이스 파일 만들기
docker build -t base -f Dockerfile.base .
# 베이스 파일에 기반한 도커 파일 만들기
docker builtd -t instagram .
# 인스타그램 도커 실행
docker run --rm -it -p 8013:80 imstagram
