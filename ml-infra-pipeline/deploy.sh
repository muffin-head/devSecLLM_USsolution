#!/bin/bash

# -----------------------------------
# Local Terraform Automation Script
# Azure Student Subscription: 7e7097f9-0f49-482f-8dd8-85e7767e3ef8
# -----------------------------------

SUBSCRIPTION_ID="7e7097f9-0f49-482f-8dd8-85e7767e3ef8"
ENV_DIR="environments/dev"

echo "🔐 Logging into Azure..."
az login --use-device-code

echo "📋 Setting subscription to: $SUBSCRIPTION_ID"
az account set --subscription "$SUBSCRIPTION_ID"

echo "📦 Initializing Terraform..."
cd $ENV_DIR
terraform init

echo "🔎 Validating configuration..."
terraform validate

echo "🧠 Generating plan..."
terraform plan -out=tfplan

echo "🚀 Applying changes..."
terraform apply -auto-approve tfplan

echo "✅ Deployment complete."
