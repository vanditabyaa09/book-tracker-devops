output "cluster_name" {
  value = module.eks.cluster_name
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "configure_kubectl" {
  value = "aws eks update-kubeconfig --region ${var.region} --name ${module.eks.cluster_name}"
}