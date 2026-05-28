data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "main" {
  # Key Vault 이름: 전역 고유, 3-24자
  name                      = "kv-${var.prefix}-${random_id.suffix.hex}"
  location                  = azurerm_resource_group.main.location
  resource_group_name       = azurerm_resource_group.main.name
  tenant_id                 = data.azurerm_client_config.current.tenant_id
  sku_name                  = "standard"
  soft_delete_retention_days = 7

  # dev 환경: purge protection 비활성화 (삭제 후 즉시 재생성 가능)
  purge_protection_enabled  = false
}

# 현재 로그인한 사용자에게 Key Vault 관리 권한 부여
resource "azurerm_role_assignment" "keyvault_admin" {
  scope                = azurerm_key_vault.main.id
  role_definition_name = "Key Vault Administrator"
  principal_id         = data.azurerm_client_config.current.object_id
}