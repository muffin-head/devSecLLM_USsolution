variable "name" {
  description = "Name of the Application Insights resource"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group where App Insights will be deployed"
  type        = string
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
}
