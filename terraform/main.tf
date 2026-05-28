terraform {
  required_version = ">= 1.5"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

# Storage Account, Key Vault 등 전역 고유 이름이 필요한 리소스에 붙일 suffix
resource "random_id" "suffix" {
  byte_length = 4
}