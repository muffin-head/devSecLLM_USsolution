variable "name" {}
variable "location" {}
variable "resource_group_name" {}
variable "dns_prefix" {}
variable "vm_size" {}
variable "node_count" {
  type = number
}
variable "subnet_id" {}
variable "tags" {
  type = map(string)
}
