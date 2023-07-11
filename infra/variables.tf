variable "pub_key_file" {
  description = "SSH public key file path for EC2 instance access"
  type        = string

  validation {
    condition     = length(var.pub_key_file) > 0
    error_message = "File path for SSH public key not provided"
  }
}
