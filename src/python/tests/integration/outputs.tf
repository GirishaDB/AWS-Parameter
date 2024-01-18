# Specify the outputs of the code
# Refer https://developer.hashicorp.com/terraform/language/values/outputs
# For e.g.  
# output name {

# }

output "name" {
  value = "value is ${var.source_region}"

}
