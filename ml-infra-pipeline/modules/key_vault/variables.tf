variable "name" {
  description = "Name of the Key Vault"
  type        = string
}

variable "location" {
  description = "Azure region where the Key Vault will be created"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group in which to create the Key Vault"
  type        = string
}

variable "tags" {
  description = "Tags to apply to the Key Vault"
  type        = map(string)
}
