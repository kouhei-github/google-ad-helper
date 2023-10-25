FROM node:18-alpine as builder

WORKDIR /var/www/html

COPY ./nextjs /var/www/html
COPY --chmod=777 ./containers/nextjs/entrypoint.sh /tmp/entrypoint.sh

RUN chmod +x /tmp/entrypoint.sh
RUN yarn install

RUN yarn build

EXPOSE 3000

CMD ["sh", "/tmp/entrypoint.sh"]
