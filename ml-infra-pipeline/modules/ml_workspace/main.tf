resource "azurerm_machine_learning_workspace" "this" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name

  friendly_name       = var.name

  # Optional integrations
  application_insights_id = var.app_insights_id != null ? var.app_insights_id : null
  key_vault_id            = var.key_vault_id != null ? var.key_vault_id : null
  storage_account_id      = var.storage_account_id
  container_registry_id   = var.container_registry_id

  identity {
    type = "SystemAssigned"
  }

  public_network_access_enabled = true

  tags = var.tags
}
