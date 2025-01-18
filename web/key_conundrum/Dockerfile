FROM node:lts-alpine
ENV NODE_ENV=production
WORKDIR /usr/src/app
COPY ["./source/package.json", "./source/package-lock.json*", "npm-shrinkwrap.json*", "./"]
RUN npm install --production --silent && mv node_modules ../
COPY ./source .
EXPOSE 1337
RUN chown -R node /usr/src/app
USER node
CMD ["node", "index.js"]
