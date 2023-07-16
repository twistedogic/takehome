provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_security_group" "ssh_access" {
  name   = "ssh_access"
  vpc_id = aws_vpc.main_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "api_access" {
  name   = "api_access"
  vpc_id = aws_vpc.main_vpc.id

  ingress {
    from_port   = 3000
    to_port     = 3000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_key_pair" "ssh_key" {
  key_name   = "take_home_key"
  public_key = file("${var.pub_key_file}")
}

resource "aws_instance" "take-me-home" {
  ami                         = "ami-043b9c6b33cd6fff8" # Rocky 9.2 x86_64
  instance_type               = "t2.micro"
  key_name                    = aws_key_pair.ssh_key.key_name
  security_groups             = [aws_security_group.ssh_access.id, aws_security_group.api_access.id]
  subnet_id                   = aws_subnet.public_subnet.id
  associate_public_ip_address = true
  user_data                   = file("setup.sh")
}
