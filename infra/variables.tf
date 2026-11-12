variable "region" {
  default = "us-east-1"
}

variable "replica_count" {
  type        = number
  description = "Number of replicas; must be at least one."
  default     = -1

  validation {
    condition     = var.replica_count >= 1
    error_message = "replica_count must be at least one."
  }
}