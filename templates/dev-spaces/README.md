# Dev Spaces

Configuration for Dev Spaces

## Overview

This PolicyStack template provides configuration for Dev Spaces.

## Requirements

### Required
- OpenShift Container Platform 4.11.0+
- Red Hat Advanced Cluster Management 2.8.0+
- PolicyStack library chart 1.1.0+

### Optional
- Additional requirements as needed

## Installation

```bash
# Install using PolicyStack CLI
policystack install dev-spaces --version 1.0.0

# Or manually copy to your stack
cp -r versions/1.0.0/* /path/to/your/stack/dev-spaces/
```

## Configuration

Key configuration options in `values.yaml`:

```yaml
stack:
  devSpaces:
    enable: true
    # Add configuration details here
```

## Examples

See the `examples/` directory for sample configurations:

- `minimal.yaml` - Basic configuration with minimal settings
- `standard.yaml` - Standard production configuration
- `production.yaml` - Full production configuration with HA

## Changelog

### 1.0.0 - 2025-10-11
- Initial release

## Support

For issues and questions, please open an issue in the PolicyStack marketplace repository.

## License

Apache License 2.0
