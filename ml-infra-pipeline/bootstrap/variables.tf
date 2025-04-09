variable "resource_group_name" {
  default     = "tfstate-rg"
  description = "Resource group for remote state backend"
}

variable "location" {
  default     = "eastus"
  description = "Location for the resources"
}

variable "storage_account_name" {
  default     = "mlterraformstate"
  description = "Globally unique storage account name"
}

variable "container_name" {
  default     = "tfstate"
  description = "Blob container name to store tfstate files"
}

variable "tags" {
  type = map(string)
  default = {
    owner       = "mlops-team"
    environment = "bootstrap"
  }
}
