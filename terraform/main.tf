provider "azurerm" {
  features {}
}

resource "random_integer" "azure" {
  min = 1000
  max = 9999
}

resource "azurerm_resource_group" "azure" {
  name     = "azure-resources"
  location = "swedencentral"
}

resource "azurerm_storage_account" "azure" {
  name                     = "storage${random_integer.azure.result}"
  resource_group_name      = azurerm_resource_group.azure.name
  location                 = azurerm_resource_group.azure.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "azure" {
  name                = "app-service-plan${random_integer.azure.result}"
  resource_group_name = azurerm_resource_group.azure.name
  location            = azurerm_resource_group.azure.location
  os_type             = "Linux"
  sku_name            = "S1"
}

resource "azurerm_linux_function_app" "azure" {
  name                = "function-app${random_integer.azure.result}"
  resource_group_name = azurerm_resource_group.azure.name
  location            = azurerm_resource_group.azure.location

  storage_account_name       = azurerm_storage_account.azure.name
  storage_account_access_key = azurerm_storage_account.azure.primary_access_key
  service_plan_id            = azurerm_service_plan.azure.id

  site_config {}
}

resource "azurerm_storage_data_lake_gen2_filesystem" "azure" {
  name               = "azure"
  storage_account_id = azurerm_storage_account.azure.id
}

resource "azurerm_synapse_workspace" "azure" {
  name                                 = "synapse${random_integer.azure.result}"
  resource_group_name                  = azurerm_resource_group.azure.name
  location                             = azurerm_resource_group.azure.location
  storage_data_lake_gen2_filesystem_id = azurerm_storage_data_lake_gen2_filesystem.azure.id
  sql_administrator_login              = "sqladminuser"

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_databricks_workspace" "azure" {
  name                = "databricks-testp${random_integer.azure.result}"
  resource_group_name = azurerm_resource_group.azure.name
  location            = azurerm_resource_group.azure.location
  sku                 = "standard"
}