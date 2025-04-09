variable "name" {}
variable "location" {}
variable "resource_group_name" {}
variable "sku" {
  default = "Basic"
}
variable "admin_enabled" {
  type    = bool
  default = true
}
variable "tags" {
  type = map(string)
}
