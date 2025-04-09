variable "name" {}
variable "location" {}
variable "resource_group_name" {}

variable "app_insights_id" {
  description = "The ID of the Application Insights resource. Set to null if not used."
  type        = string
  default     = null
}

variable "key_vault_id" {}
variable "storage_account_id" {}
variable "container_registry_id" {}

variable "tags" {
  type = map(string)
}
