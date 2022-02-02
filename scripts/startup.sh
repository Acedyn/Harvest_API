#!/bin/sh

# Migrate the database
npx prisma db push --accept-data-loss
  
# Start the prisma service
yarn prod
