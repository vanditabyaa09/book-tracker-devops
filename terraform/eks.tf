module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "${var.project_name}-eks"
  cluster_version = var.cluster_version

  cluster_endpoint_public_access           = true # so kubectl on your laptop can reach it
  enable_cluster_creator_admin_permissions = true # gives YOUR IAM identity cluster-admin

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets # worker nodes live in private subnets

  eks_managed_node_groups = {
    default = {
      instance_types = [var.node_instance_type]
      min_size       = 2
      max_size       = 3
      desired_size   = 2
    }
  }
}