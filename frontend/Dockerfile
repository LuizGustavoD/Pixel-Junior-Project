FROM node:20-alpine AS builder

WORKDIR /app

COPY pixel-driver/package*.json ./

RUN npm ci

COPY pixel-driver/ ./

RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx/config/nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx/error_pages/ /usr/share/nginx/html/error_pages/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
