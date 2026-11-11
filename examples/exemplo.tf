# exemplo.tf — recurso Terraform simples incorporado na documentação.
resource "local_file" "exemplo" {
  filename = "${path.module}/exemplo-output.txt"
  content  = "Gerado pelo exemplo Terraform da documentação."
}
