FROM node:18

WORKDIR /app

COPY ./frontend-app/package*.json ./
RUN npm install

COPY ./frontend-app ./

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
