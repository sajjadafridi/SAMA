# Build React app
FROM node:18 as build

WORKDIR /app
COPY . .
RUN npm install
RUN npm run build

# Serve React with nginx
FROM nginx:alpine

# Copy built React files to nginx's web root
COPY --from=build /app/build /usr/share/nginx/html

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off