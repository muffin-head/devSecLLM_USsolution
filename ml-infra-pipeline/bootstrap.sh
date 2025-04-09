#!/bin/bash

# -------------------------------
# Bootstrap Script for Terraform Remote State
# -------------------------------

SUBSCRIPTION_ID="7e7097f9-0f49-482f-8dd8-85e7767e3ef8"
BOOTSTRAP_DIR="bootstrap"

echo "🔐 Logging into Azure..."
az login --use-device-code

echo "📋 Setting subscription to: $SUBSCRIPTION_ID"
az account set --subscription "$SUBSCRIPTION_ID"

echo "🚀 Bootstrapping Terraform remote state backend..."
cd $BOOTSTRAP_DIR

echo "📦 Initializing Terraform..."
terraform init

echo "🧠 Planning infrastructure..."
terraform plan -out=tfplan

echo "✅ Applying remote state backend infrastructure..."
terraform apply -auto-approve tfplan

echo "📦 Remote state backend created!"
