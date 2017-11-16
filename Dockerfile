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
RUN         cp /srv/app/.config/nginx/mysite.conf /etc/nginx/sites-available/
RUN         rm -rf /etc/nginx/sites-enabled/*
RUN         ln -sf /etc/nginx/sites-available/mysite.conf \
                    /etc/nginx/sites-enabled/mysite.conf

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
