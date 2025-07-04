FROM node:18 AS builder

WORKDIR /app

COPY ./frontend-app/package*.json ./
RUN npm install

COPY ./frontend-app ./
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
