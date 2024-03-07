variable "location" {
  description = "The Azure region to deploy the resources"
  default     = "germanywestcentral"
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "adragos_rg"
}
variable "shared_azure_vault_name" {
  description = "The name of the resource group"
  type        = string
  default     = "adragos-shared-vault"
}

variable "shared_virtual_network_name" {
  description = "The name of the resource group"
  type        = string
  default     = "adragos-shared-vnet"
}
variable "acr_name" {
  description = "The name of the Azure Container Registry"
  type        = string
  default     = "adragosregistry"
}

variable "acr_password" {
  description = "The password of the Azure Container Registry"
  type        = string
  default     = ""
}
variable "container_image" {
  description = "The name of the docker image to be pushed to the registry"
  type        = string
  default     = "adragos-chatgpt"
}

variable "container_name" {
  description = "The name of the container instance"
  type        = string
  default     = "adragos-chatgpt"
}


variable "image_tag" {
  description = "The tag of the container image to be pushed to the registry"
  type        = string
  default     = "latest"
}





