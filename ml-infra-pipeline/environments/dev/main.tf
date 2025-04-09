provider "azurerm" {
  features {}

  subscription_id = "7e7097f9-0f49-482f-8dd8-85e7767e3ef8"
}


resource "random_integer" "unique" {
  min = 10000
  max = 99999
}

# 1. Resource Group
module "rg" {
  source   = "../../modules/resource_group"
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

# 2. Virtual Network + Subnet
module "network" {
  source              = "../../modules/networking"
  name                = "ml-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = module.rg.name
  tags                = var.tags
}

# 3. Key Vault
module "kv" {
  source              = "../../modules/key_vault"
  name                = "ml-kv-${random_integer.unique.result}"
  location            = var.location
  resource_group_name = module.rg.name
  tags                = var.tags
}

# 4. Container Registry
module "acr" {
  source              = "../../modules/container_registry"
  name                = "mlacr${random_integer.unique.result}"
  location            = var.location
  resource_group_name = module.rg.name
  tags                = var.tags
}

# 5. Storage Account (for ML Workspace default store)
module "storage" {
  source              = "../../modules/storage_account"
  name                = "mlstore${random_integer.unique.result}"
  location            = var.location
  resource_group_name = module.rg.name
  tags                = var.tags
}

# 6. Application Insights
module "app_insights" {
  source              = "../../modules/app_insights"
  name                = "ml-insights"
  location            = var.location
  resource_group_name = module.rg.name
  tags                = var.tags
}


# 7. Azure ML Workspace
module "mlws" {
  source                = "../../modules/ml_workspace"
  name                  = "ml-ws"
  location              = var.location
  resource_group_name   = module.rg.name
  app_insights_id       =  module.app_insights.id 
  key_vault_id          = module.kv.id
  storage_account_id    = module.storage.id
  container_registry_id = module.acr.id
  tags                  = var.tags
}

# 8. AKS Cluster
module "aks" {
  source              = "../../modules/aks"
  name                = "ml-aks"
  location            = var.location
  resource_group_name = module.rg.name
  dns_prefix          = "mlaks"
  vm_size             = "Standard_DS2_v2"
  node_count          = 1
  subnet_id           = module.network.aks_subnet_id
  tags                = var.tags
}
