# Use the official Node.js 18 image as the base
FROM node:18-alpine AS base

WORKDIR /usr/src/app

COPY source/package.json source/package-lock.json ./

# Install dependencies in a separate stage for caching
FROM base AS dependencies

# Install production dependencies
RUN npm ci --only=production

COPY source/. .
RUN npm ci

RUN npm run build

# Create a minimal image for serving the app
FROM node:18-alpine AS production

WORKDIR /usr/src/app

# Copy only the necessary files from the build stage
COPY --from=dependencies /usr/src/app/package.json /usr/src/app/package-lock.json ./
COPY --from=dependencies /usr/src/app/.next ./.next
COPY --from=dependencies /usr/src/app/node_modules ./node_modules
COPY --from=dependencies /usr/src/app/public ./public

ENV PORT=1337

EXPOSE 1337

CMD ["npm", "run", "start"]
