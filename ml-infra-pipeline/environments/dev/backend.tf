terraform {
  required_version = ">= 1.3.0"

  backend "azurerm" {
    resource_group_name   = "tfstate-rg"
    storage_account_name  = "mlterraformstate"
    container_name        = "tfstate"
    key                   = "ml-dev-infra.tfstate"
  }
}
