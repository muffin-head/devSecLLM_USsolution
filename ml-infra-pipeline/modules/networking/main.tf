resource "azurerm_virtual_network" "this" {
    name= var.name
    address_space=var.address_space
    location=var.location
    resource_group_name=var.resource_group_name
    tags=var.tags
}

resource "azurerm_subnet" "aks" {
    name= "aks-subnet"
    resource_group_name=var.resource_group_name
    virtual_network_name=azurerm_virtual_network.this.name
    address_prefixes= ["10.0.1.0/24"]
}