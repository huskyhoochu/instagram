# 실행할 쉘 환경설정
#!/usr/bin/env bash
# 베이스 도커 파일 생성
docker build -t base -f Dockerfile.base .
# 도커허브에 태그 생성 (커밋과 같음)
docker tag base lanark/base
# 도커허브에 베이스 이미지를 푸시
docker push lanark/base