
data "azurerm_resource_group" "shared_rg" {
  name                = var.resource_group_name
}

data "azurerm_virtual_network" "shared_vnet" {
  name                = var.shared_virtual_network_name
  resource_group_name = var.resource_group_name
}
# Create a subnet
resource "azurerm_subnet" "chatgpt_subnet" {
  name                 = "chatgpt-subnet"
  resource_group_name  = data.azurerm_resource_group.shared_rg.name
  virtual_network_name = data.azurerm_virtual_network.shared_vnet.name
  address_prefixes     = ["10.1.2.0/24"]

  delegation {
    name = "ACIdelegation"

    service_delegation {
      name    = "Microsoft.ContainerInstance/containerGroups"
      actions = ["Microsoft.Network/virtualNetworks/subnets/join/action", "Microsoft.Network/virtualNetworks/subnets/prepareNetworkPolicies/action"]
    }
  }
}


# Create a container instance
resource "azurerm_container_group" "cg" {
  name                = var.container_name
  resource_group_name = data.azurerm_resource_group.shared_rg.name
  location            = data.azurerm_resource_group.shared_rg.location
  os_type             = "Linux"
  ip_address_type     = "Private"
  restart_policy      = "OnFailure"
  subnet_ids          = [azurerm_subnet.chatgpt_subnet.id]

  container {
    name   = var.container_name
    image  = "${var.acr_name}.azurecr.io/${var.container_image}:${var.image_tag}"
    cpu    = "1.0"
    memory = "2.0"

    ports {
      port     = 3000
      protocol = "TCP"
    }

    ports {
      port     = 80
      protocol = "TCP"
    }

    ports {
      port     = 443
      protocol = "TCP"
    }
  }

  image_registry_credential {
    server   = "${var.acr_name}.azurecr.io"
    username = var.acr_name
    password = var.acr_password
  }
}
                                                           
