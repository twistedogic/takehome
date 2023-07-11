# Take me home

## Infrastructure setup

### Prerequisites

* Install `terraform` following [here](https://developer.hashicorp.com/terraform/downloads)
* In order to provision AWS asset, `AWS` account with correct permission needs to
be configured. Keys and token should set as environment variable as below:
````
$ export AWS_ACCESS_KEY_ID=(your access key id)
$ export AWS_SECRET_ACCESS_KEY=(your secret access key)
````

### Initialize Infrastructure

```
$ cd infra
$ terraform Init 
$ terraform apply
```

### See current infrastructure diff

```
$ cd infra
$ terraform plan
```
