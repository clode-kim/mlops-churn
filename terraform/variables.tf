variable "subscription_id" {
  description = "Azure 구독 ID"
  type        = string
}

variable "location" {
  description = "Azure 리전"
  type        = string
  default     = "koreacentral"
}

variable "prefix" {
  description = "리소스 이름 접두어"
  type        = string
  default     = "mlchurn"
}

variable "environment" {
  description = "배포 환경"
  type        = string
  default     = "dev"
}

variable "postgres_admin_password" {
  description = "PostgreSQL 관리자 비밀번호 (최소 8자, 대소문자+숫자+특수문자 포함)"
  type        = string
  sensitive   = true
}