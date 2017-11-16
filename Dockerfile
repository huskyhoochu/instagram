# 어느 이미지를 불러올까
FROM        lanark/base
# 유저 정보
MAINTAINER  dfg1499@gmail.com
# 언어 환경 설정
ENV         LANG C.UTF-8
# 현재 폴더 전체를 /srv/app에 복사
COPY        . /srv/app
# requirements 설치
# base애서 이미 설치했으므로 통과된다,
RUN         /root/.pyenv/versions/app/bin/pip install -r \
            /srv/app/requirements.txt

# pyenv 환경 설정
WORKDIR     /srv/app
RUN         pyenv local app

# Nginx
# nginx가 supervisor의 지배를 받도록 nginx.conf 수정한 것 붙여넣기
RUN         cp /srv/app/.config/nginx/nginx.conf \
                /etc/nginx/nginx.conf
# conf 파일 옮겨넣고 심볼릭 링크 작성
RUN         cp /srv/app/.config/nginx/mysite.conf /etc/nginx/sites-available/
RUN         ln -sf /etc/nginx/sites-available/mysite.conf \
                    /etc/nginx/sites-enabled/mysite.conf
# 기본 conf 삭제
RUN         rm -rf /etc/nginx/sites-enabled/*

# uWSGI
# 로그 폴더 만들기
# -p: 마지막 디렉터리를 만들 때 상위 디렉터리가 없다면 순서대로 생성해준다
RUN         mkdir -p /var/log/uwsgi/app

# mysqlite 사용할 경우
# WORKDIR   /srv/app/instagram
# 정적파일 수집
# RUN       /root/.pyenv/versions/app/python manage.py collectstatic --noinput
# sqlite3로 migrate
# RUN       /root/.pyenv/versions/app/python manage.py migrate --noinput

# supervisor
RUN         cp /srv/app/.config/supervisor/* \
                /etc/supervisor/conf.d/
CMD         supervisord -n

# port open
EXPOSE      80
