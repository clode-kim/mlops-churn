resource "azurerm_kubernetes_cluster" "main" {
  name                = "aks-${var.prefix}-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "${var.prefix}-${var.environment}"

  default_node_pool {
    name       = "system"
    node_count = 1
    vm_size    = "Standard_B2als_v2"

    upgrade_settings {
      max_surge = "10%"
    }
  }

  # Managed Identity: AKS가 ACR 접근 등 Azure 리소스를 사용할 때 필요한 ID
  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "kubenet"
  }
}