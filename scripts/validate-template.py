#!/usr/bin/env python3
"""
PolicyStack Marketplace Template Validator

Validates template structure and metadata.
"""

import os
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

class TemplateValidator:
    def __init__(self, template_path: str):
        self.template_path = Path(template_path)
        self.errors = []
        self.warnings = []
        self.info = []
    
    def validate(self) -> bool:
        """Run all validation checks"""
        print(f"🔍 Validating template: {self.template_path}")
        
        # Check directory structure
        self.validate_structure()
        
        # Validate metadata.yaml
        if (self.template_path / "metadata.yaml").exists():
            self.validate_metadata()
        
        # Validate versions
        self.validate_versions()
        
        # Validate examples
        self.validate_examples()
        
        # Print results
        self.print_results()
        
        return len(self.errors) == 0
    
    def validate_structure(self):
        """Validate directory structure"""
        required_files = ["metadata.yaml", "README.md"]
        required_dirs = ["versions", "examples"]
        
        for file in required_files:
            if not (self.template_path / file).exists():
                self.errors.append(f"Missing required file: {file}")
        
        for dir in required_dirs:
            if not (self.template_path / dir).exists():
                self.errors.append(f"Missing required directory: {dir}")
    
    def validate_metadata(self):
        """Validate metadata.yaml content"""
        metadata_file = self.template_path / "metadata.yaml"
        
        try:
            with open(metadata_file, 'r') as f:
                metadata = yaml.safe_load(f)
            
            # Required fields
            required_fields = [
                "name", "displayName", "description", "author",
                "categories", "version", "versions"
            ]
            
            for field in required_fields:
                if field not in metadata:
                    self.errors.append(f"metadata.yaml missing required field: {field}")
            
            # Validate author
            if "author" in metadata:
                if not isinstance(metadata["author"], dict):
                    self.errors.append("author must be a dictionary")
                elif "name" not in metadata["author"]:
                    self.errors.append("author must have a name field")
            
            # Validate categories
            if "categories" in metadata:
                if "primary" not in metadata["categories"]:
                    self.errors.append("categories must have a primary category")
            
            # Validate version info
            if "version" in metadata:
                latest = metadata["version"].get("latest")
                if not latest:
                    self.errors.append("version must specify latest")
                
                # Check that latest version exists in versions
                if "versions" in metadata and latest not in metadata["versions"]:
                    self.errors.append(f"Latest version {latest} not found in versions")
            
            # Validate each version entry
            if "versions" in metadata:
                for version, details in metadata["versions"].items():
                    if not isinstance(details, dict):
                        self.errors.append(f"Version {version} must have details")
                        continue
                    
                    required_version_fields = ["date", "policyLibrary", "openshift", "acm", "changes"]
                    for field in required_version_fields:
                        if field not in details:
                            self.warnings.append(f"Version {version} missing field: {field}")
            
            # Check for recommended fields
            recommended_fields = ["tags", "features", "requirements", "complexity"]
            for field in recommended_fields:
                if field not in metadata:
                    self.warnings.append(f"Consider adding recommended field: {field}")
            
            self.info.append(f"Template name: {metadata.get('name')}")
            self.info.append(f"Latest version: {metadata.get('version', {}).get('latest')}")
            self.info.append(f"Total versions: {len(metadata.get('versions', {}))}")
            
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in metadata.yaml: {e}")
        except Exception as e:
            self.errors.append(f"Error reading metadata.yaml: {e}")
    
    def validate_versions(self):
        """Validate version directories"""
        versions_dir = self.template_path / "versions"
        
        if not versions_dir.exists():
            return
        
        version_dirs = [d for d in versions_dir.iterdir() if d.is_dir()]
        
        if not version_dirs:
            self.errors.append("No version directories found in versions/")
            return
        
        for version_dir in version_dirs:
            version = version_dir.name
            
            # Check for required files in each version
            required_files = ["Chart.yaml", "values.yaml"]
            for file in required_files:
                if not (version_dir / file).exists():
                    self.errors.append(f"Version {version} missing required file: {file}")
            
            # Validate Chart.yaml
            chart_file = version_dir / "Chart.yaml"
            if chart_file.exists():
                try:
                    with open(chart_file, 'r') as f:
                        chart = yaml.safe_load(f)
                    
                    if "dependencies" not in chart:
                        self.warnings.append(f"Version {version}: Chart.yaml missing dependencies")
                    else:
                        # Check for policy-library dependency
                        has_policy_lib = any(
                            dep.get("name") == "policy-library" 
                            for dep in chart.get("dependencies", [])
                        )
                        if not has_policy_lib:
                            self.errors.append(f"Version {version}: Missing policy-library dependency")
                    
                except Exception as e:
                    self.errors.append(f"Version {version}: Invalid Chart.yaml: {e}")
            
            # Check for converters directory
            if not (version_dir / "converters").exists():
                self.warnings.append(f"Version {version}: No converters directory")
            
            self.info.append(f"Found version: {version}")
    
    def validate_examples(self):
        """Validate example files"""
        examples_dir = self.template_path / "examples"
        
        if not examples_dir.exists():
            return
        
        example_files = list(examples_dir.glob("*.yaml")) + list(examples_dir.glob("*.yml"))
        
        if not example_files:
            self.warnings.append("No example files found in examples/")
            return
        
        for example_file in example_files:
            try:
                with open(example_file, 'r') as f:
                    example = yaml.safe_load(f)
                
                # Basic validation - check if it has the stack structure
                if not isinstance(example, dict):
                    self.errors.append(f"Example {example_file.name}: Not a valid YAML dictionary")
                elif "stack" not in example:
                    self.warnings.append(f"Example {example_file.name}: Missing 'stack' key")
                
                self.info.append(f"Found example: {example_file.name}")
                
            except yaml.YAMLError as e:
                self.errors.append(f"Example {example_file.name}: Invalid YAML: {e}")
            except Exception as e:
                self.errors.append(f"Example {example_file.name}: Error reading file: {e}")
    
    def print_results(self):
        """Print validation results"""
        print("\n" + "="*60)
        print("VALIDATION RESULTS")
        print("="*60)
        
        if self.info:
            print("\n📋 Info:")
            for msg in self.info:
                print(f"  ℹ️  {msg}")
        
        if self.warnings:
            print("\n⚠️  Warnings:")
            for msg in self.warnings:
                print(f"  ⚠️  {msg}")
        
        if self.errors:
            print("\n❌ Errors:")
            for msg in self.errors:
                print(f"  ❌ {msg}")
            print(f"\n🔴 Validation FAILED with {len(self.errors)} error(s)")
        else:
            print("\n✅ Validation PASSED")


def validate_all_templates(templates_dir: str = "templates") -> bool:
    """Validate all templates in directory"""
    templates_path = Path(templates_dir)
    
    if not templates_path.exists():
        print(f"❌ Templates directory not found: {templates_dir}")
        return False
    
    all_valid = True
    template_dirs = [d for d in templates_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    if not template_dirs:
        print(f"⚠️  No templates found in {templates_dir}")
        return True
    
    print(f"🔍 Validating {len(template_dirs)} template(s)...\n")
    
    for template_dir in template_dirs:
        validator = TemplateValidator(template_dir)
        if not validator.validate():
            all_valid = False
        print("")  # Empty line between templates
    
    return all_valid


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate PolicyStack Marketplace templates")
    parser.add_argument(
        "template",
        nargs="?",
        help="Path to specific template directory to validate"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all templates in the templates directory"
    )
    parser.add_argument(
        "--templates-dir",
        default="templates",
        help="Directory containing templates (default: templates)"
    )
    
    args = parser.parse_args()
    
    if args.all or not args.template:
        # Validate all templates
        success = validate_all_templates(args.templates_dir)
    else:
        # Validate specific template
        validator = TemplateValidator(args.template)
        success = validator.validate()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
