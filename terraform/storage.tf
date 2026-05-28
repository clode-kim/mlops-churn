resource "azurerm_storage_account" "main" {
  # Storage Account 이름: 전역 고유, 소문자+숫자, 3-24자
  name                     = "${var.prefix}${var.environment}${random_id.suffix.hex}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# MLflow artifact 저장용 컨테이너 (S3의 bucket과 같은 개념)
resource "azurerm_storage_container" "mlflow_artifacts" {
  name                  = "mlflow-artifacts"
  storage_account_id    = azurerm_storage_account.main.id
  container_access_type = "private"
}