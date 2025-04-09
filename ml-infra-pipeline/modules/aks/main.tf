resource "azurerm_kubernetes_cluster" "this" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = var.dns_prefix

  default_node_pool {
    name       = "default"
    vm_size    = var.vm_size
    node_count = var.node_count
    vnet_subnet_id = var.subnet_id
  }

  

  identity {
    type = "SystemAssigned"
  }

network_profile {
  network_plugin = "azure"
  service_cidr   = "10.1.0.0/16"
  dns_service_ip = "10.1.0.10"
}


  tags = var.tags
}
