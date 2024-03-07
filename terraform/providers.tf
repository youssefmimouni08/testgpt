terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  tenant_id       = "28d1eaf4-0022-4840-8257-173c1bd0de0f"
  subscription_id = "d3d5fa99-f6ff-4d6a-aa53-5a0f9ad278cb"
  client_id       = "ecf5183d-af39-4885-8276-c5b1bba34105"
  client_secret   = "gAG8Q~3LHLp7YIclx98JId1fZoddWq4KMZaxpbB3"
  skip_provider_registration = "true"
  features {
    key_vault {
      purge_soft_deleted_certificates_on_destroy = true
      recover_soft_deleted_certificates          = true
    }
  }
  
} 