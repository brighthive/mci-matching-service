#!/bin/bash

# ----------------------------------------------------------------------------
# ecr_build.sh - Build the image and push it to Docker  
#
# ----------------------------------------------------------------------------

CONTAINER_VERSION=1.0.0
CONTAINER_NAME=brighthive/mci-matching-service
ECR_BASE=396527728813.dkr.ecr.us-east-2.amazonaws.com

# Build the Container
docker build -t $CONTAINER_NAME:$CONTAINER_VERSION .
docker tag $CONTAINER_NAME:$CONTAINER_VERSION $CONTAINER_NAME:latest

# Tag the Containers
docker tag $CONTAINER_NAME:$CONTAINER_VERSION $ECR_BASE/$CONTAINER_NAME:$CONTAINER_VERSION
docker tag $CONTAINER_NAME:latest $ECR_BASE/$CONTAINER_NAME:latest

# Login to ECR
$(aws ecr get-login --no-include-email --region us-east-2)

# Push to ECR
docker push $ECR_BASE/$CONTAINER_NAME:$CONTAINER_VERSION
docker push $ECR_BASE/$CONTAINER_NAME:latest