# PolicyStack Marketplace
**A curated marketplace of production-ready PolicyStack configurations for OpenShift**

[Contributing](#contributing) | [CLI Tool](https://github.com/PolicyStack/cli)

---

## 🎯 Overview

PolicyStack Marketplace is a centralized repository of reusable, versioned, and battle-tested configuration templates for managing OpenShift clusters using Red Hat Advanced Cluster Management (ACM) policies. Each template is:

- ✅ **Production-Ready**: Tested across multiple OpenShift versions
- ✅ **Versioned**: Semantic versioning with clear upgrade paths
- ✅ **Documented**: Comprehensive guides with examples
- ✅ **Compliant**: Aligned with security standards (NIST, CIS, PCI DSS)
- ✅ **GitOps-Ready**: Designed for ACM and ArgoCD integration

## 🚀 Quick Start

### Using Templates Manually

1. **Browse** the available templates below
2. **Choose** a template and version that fits your needs
3. **Copy** the template files to your PolicyStack repository
4. **Customize** the values.yaml for your environment
5. **Deploy** using your existing PolicyStack workflow

### Using the CLI

```bash
# Search for templates
policystack search logging

# Get template info
policystack info openshift-logging

# Install template
policystack install openshift-logging --version 1.1.0

# Initialize with template
policystack init my-cluster --template openshift-logging
```

## 🔍 Finding Templates

### By Tags

Search templates by functionality:
- `production-ready`: Battle-tested in production
- `gitops`: GitOps-optimized
- `compliance`: Security standard alignment
- `multi-tenant`: Multi-tenancy support
- `ha`: High availability configurations

### By Requirements

Filter by your environment:
- OpenShift version (4.11, 4.12, 4.13, 4.14)
- ACM version (2.8, 2.9, 2.10)
- PolicyStack library version

## 📋 Template Metadata

Each template includes rich metadata:

```yaml
name: openshift-logging
displayName: "OpenShift Logging Stack"
description: "Production-ready logging with..."
author:
  name: "PolicyStack Team"
  github: "@policystack"
categories:
  primary: observability
  secondary: [logging, elasticsearch]
tags: [production-ready, elasticsearch, kibana]
version:
  latest: 1.1.0
  supported: [1.1.0, 1.0.0]
versions:
  "1.1.0":
    date: "2025-01-20"
    openshift: ">=4.12.0"
    acm: ">=2.9.0"
    changes: ["Added feature X", "Fixed bug Y"]
    breaking: false
```

## 🛠️ Development

### Building the Registry

The registry index is automatically generated from template metadata:

```bash
# Build registry index
python scripts/build-registry.py

# Validate all templates
python scripts/validate-template.py --all

# Validate specific template
python scripts/validate-template.py templates/openshift-logging
```

### Manual Updates

Until CI/CD is implemented, follow these steps:

1. Add/update your template in `templates/<name>/`
2. Run validation: `python scripts/validate-template.py templates/<name>`
3. Build registry: `python scripts/build-registry.py`
4. Commit all changes including the updated `registry.yaml`

## 🤝 Contributing

We welcome contributions! To add a new template:

1. **Fork** this repository
2. **Create** your template following the structure above
3. **Validate** using the provided scripts
4. **Document** thoroughly with examples
5. **Test** on multiple OpenShift versions
6. **Submit** a pull request

### Template Requirements

- [ ] Complete metadata.yaml with all required fields
- [ ] Comprehensive README with examples
- [ ] At least one working version
- [ ] Minimal, standard, and advanced examples
- [ ] Tested on supported OpenShift versions
- [ ] Passes validation script

### Quality Standards

Templates must meet these criteria:
- **Idempotent**: Can be applied multiple times safely
- **Configurable**: Key parameters exposed in values.yaml
- **Secure**: Follow security best practices
- **Documented**: Clear descriptions for all parameters
- **Versioned**: Semantic versioning with changelogs

## 📚 Resources

- [PolicyStack Chart Library](https://github.com/PolicyStack/PolicyStack-chart)
- [ACM Policy Framework](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes)

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE.md) file for details.

## 🏆 Contributors

- Asa Moore (@asmoorerh)

---

**Need help?** Open an [issue](https://github.com/PolicyStack/marketplace/issues)
