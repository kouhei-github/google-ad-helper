FROM nginx:1.21-alpine

# ローカルのdefault.confをコンテナにコピー
COPY ./containers/nginx/conf.d/local/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
