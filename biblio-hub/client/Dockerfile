# build stage
# the first stage is responsible for building a production-ready artifact of our Vue.js app
FROM node:lts-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
RUN npm run build
# COPY ./nginx/default.conf /etc/nginx/nginx.conf

# production stage
# the second stage is responsible for serving such artifact using NGINX
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]