variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Prefix for all resource names"
  type        = string
  default     = "book-tracker"
}

variable "cluster_version" {
  description = "EKS Kubernetes version (check with: aws eks describe-cluster-versions)"
  type        = string
}

variable "node_instance_type" {
  description = "EC2 instance type for worker nodes"
  type        = string
  default     = "t3.large"
}

