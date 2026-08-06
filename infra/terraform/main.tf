data "oci_identity_availability_domains" "ads" {
  compartment_id = var.compartment_id
}

# RED
#--------------------------------------

resource "oci_core_vcn" "vcn" {
  compartment_id = var.compartment_id
  cidr_blocks    = ["10.0.0.0/16"]
  display_name   = "VCN-EnergiAI"
  dns_label      = "vcnenergiai"
}

resource "oci_core_internet_gateway" "igw" {
  compartment_id = var.compartment_id
  vcn_id         = oci_core_vcn.vcn.id
  display_name   = "Internet gateway-VCN-EnergiAI"
  enabled        = true
}

resource "oci_core_default_route_table" "default_rt" {
  manage_default_resource_id = oci_core_vcn.vcn.default_route_table_id

  route_rules {
    destination       = "0.0.0.0/0"
    network_entity_id = oci_core_internet_gateway.igw.id
  }
}

resource "oci_core_default_security_list" "default_sl" {
  manage_default_resource_id = oci_core_vcn.vcn.default_security_list_id

  egress_security_rules {
    destination = "0.0.0.0/0"
    protocol    = "all"
  }

  ingress_security_rules {
    protocol = "6"
    source   = "0.0.0.0/0"
    tcp_options {
      min = 22
      max = 22
    }
  }

  ingress_security_rules {
    protocol = "1"
    source   = "0.0.0.0/0"
    icmp_options {
      type = 3
      code = 4
    }
  }

  ingress_security_rules {
    protocol = "1"
    source   = "10.0.0.0/16"
    icmp_options {
      type = 3
    }
  }

  ingress_security_rules {
    protocol    = "6"
    source      = "0.0.0.0/0"
    description = "Permitir tráfico público a la API REST de EnergiAI"
    tcp_options {
      min = var.app_port
      max = var.app_port
    }
  }
}

resource "oci_core_subnet" "public_subnet" {
  compartment_id             = var.compartment_id
  vcn_id                     = oci_core_vcn.vcn.id
  cidr_block                 = "10.0.0.0/24"
  display_name               = "public subnet-VCN-EnergiAI"
  dns_label                  = "sub07210737080"
  route_table_id             = oci_core_default_route_table.default_rt.id
  security_list_ids          = [oci_core_default_security_list.default_sl.id]
  prohibit_public_ip_on_vnic = false
} 

#ARM image
#---------------------------------------------

data "oci_core_images" "ubuntu_arm" {
  compartment_id           = var.compartment_id
  operating_system         = "Canonical Ubuntu"
  operating_system_version = "22.04"
  shape                    = "VM.Standard.A1.Flex"
  sort_by                  = "TIMECREATED"
  sort_order                = "DESC"
}

# VM
#---------------------------------------------

resource "oci_core_instance" "backend_vm" {
  compartment_id      = var.compartment_id
  availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
  display_name        = "${var.project_name}-vm"
  shape                = "VM.Standard.A1.Flex"

  shape_config {
    ocpus         = var.instance_ocpus
    memory_in_gbs = var.instance_memory_gb
  }

  source_details {
    source_type             = "image"
    source_id                = data.oci_core_images.ubuntu_arm.images[0].id
    boot_volume_size_in_gbs = var.boot_volume_size_gb
  }

  create_vnic_details {
    subnet_id        = oci_core_subnet.public_subnet.id
    assign_public_ip = true
  }

  metadata = {
    ssh_authorized_keys = var.ssh_public_key
  }
}

# ---------- Object Storage ----------

data "oci_objectstorage_namespace" "ns" {
  compartment_id = var.compartment_id
}

resource "oci_objectstorage_bucket" "assets" {
  compartment_id = var.compartment_id
  namespace      = data.oci_objectstorage_namespace.ns.namespace
  name           = "${var.project_name}-assets"
  access_type    = "NoPublicAccess"
}

# ---------- OCI Container Registry ----------

resource "oci_artifacts_container_repository" "backend_repo" {
  compartment_id = var.compartment_id
  display_name   = "${var.project_name}/backend"
  is_public      = false
}
