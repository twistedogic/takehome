output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.take-me-home.public_ip
}

output "instance_public_url" {
  description = "Public URL of the EC2 instance"
  value       = aws_instance.take-me-home.public_dns
}
