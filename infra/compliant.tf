variable "environment" {
  type        = string
  description = "Deployment environment: test or production."
  default     = "test"

  validation {
    condition     = contains(["test", "production"], var.environment)
    error_message = "environment must be test or production."
  }
}