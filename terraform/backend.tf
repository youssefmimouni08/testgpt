terraform {
  backend "azurerm" {
    resource_group_name  = "adragos_rg"
    storage_account_name = "adragosstorage"
    container_name       = "chatgpttfstate"
    key                  = "terraform.tfstate" # Unique key for the materialkosten project
    access_key           = "KB9GNgEFExWpDX5Imdb5kSnIw66tV/Mj7kbEogXIFp5zEGyMdt7R1w47u18axvbattSe8BlD7uEB+AStzmQsbw=="
  }
}

