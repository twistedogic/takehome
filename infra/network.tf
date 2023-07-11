resource "aws_vpc" "main_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = "10.0.2.0/24"
  map_public_ip_on_launch = true

  depends_on = [aws_internet_gateway.public_gateway]
}

resource "aws_internet_gateway" "public_gateway" {
  vpc_id = aws_vpc.main_vpc.id
}

resource "aws_route_table" "route_table" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.public_gateway.id
  }
}

resource "aws_route_table_association" "subnet_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.route_table.id
}

