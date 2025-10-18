#!/usr/bin/env python3
"""
PolicyStack Marketplace Registry Builder

Scans all templates and builds a searchable registry index.
"""

import os
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class RegistryBuilder:
    def __init__(self, templates_dir: str = "templates", output_file: str = "registry.yaml"):
        self.templates_dir = Path(templates_dir)
        self.output_file = Path(output_file)
        self.registry = {
            "version": "1.0.0",
            "generated": datetime.now().isoformat(),
            "templates": [],
            "categories": {},
            "tags": {},
            "stats": {
                "total_templates": 0,
                "total_versions": 0,
                "authors": set()
            }
        }
    
    def scan_templates(self):
        """Scan templates directory for metadata files"""
        print(f"📂 Scanning {self.templates_dir}...")
        
        for template_path in self.templates_dir.iterdir():
            if template_path.is_dir() and not template_path.name.startswith('.'):
                metadata_file = template_path / "metadata.yaml"
                
                if metadata_file.exists():
                    print(f"  ✓ Found template: {template_path.name}")
                    self.process_template(metadata_file)
                else:
                    print(f"  ⚠ No metadata.yaml in {template_path.name}")
    
    def process_template(self, metadata_file: Path):
        """Process a single template metadata file"""
        try:
            with open(metadata_file, 'r') as f:
                metadata = yaml.safe_load(f)
            
            # Add template to registry
            template_entry = {
                "name": metadata.get("name"),
                "displayName": metadata.get("displayName"),
                "description": metadata.get("description"),
                "author": metadata.get("author"),
                "categories": metadata.get("categories"),
                "tags": metadata.get("tags", []),
                "version": metadata.get("version"),
                "versions": metadata.get("versions"),
                "features": len(metadata.get("features", [])),
                "requirements": metadata.get("requirements"),
                "complexity": metadata.get("complexity"),
                "path": f"templates/{metadata.get('name')}"
            }
            
            self.registry["templates"].append(template_entry)
            
            # Update category index
            primary_cat = metadata.get("categories", {}).get("primary")
            if primary_cat:
                if primary_cat not in self.registry["categories"]:
                    self.registry["categories"][primary_cat] = []
                self.registry["categories"][primary_cat].append(metadata.get("name"))
            
            # Update tag index
            for tag in metadata.get("tags", []):
                if tag not in self.registry["tags"]:
                    self.registry["tags"][tag] = []
                self.registry["tags"][tag].append(metadata.get("name"))
            
            # Update stats
            self.registry["stats"]["total_templates"] += 1
            self.registry["stats"]["total_versions"] += len(metadata.get("versions", {}))
            
            author_name = metadata.get("author", {}).get("name")
            if author_name:
                self.registry["stats"]["authors"].add(author_name)
            
        except Exception as e:
            print(f"  ❌ Error processing {metadata_file}: {e}")
    
    def build_index(self):
        """Build searchable indexes"""
        print("\n🔨 Building indexes...")
        
        # Sort templates by name
        self.registry["templates"].sort(key=lambda x: x["name"])
        
        # Sort category and tag lists
        for cat in self.registry["categories"]:
            self.registry["categories"][cat].sort()
        
        for tag in self.registry["tags"]:
            self.registry["tags"][tag].sort()
        
        # Convert authors set to sorted list
        self.registry["stats"]["authors"] = sorted(list(self.registry["stats"]["authors"]))
        
        print(f"  📊 Total templates: {self.registry['stats']['total_templates']}")
        print(f"  📊 Total versions: {self.registry['stats']['total_versions']}")
        print(f"  📊 Categories: {len(self.registry['categories'])}")
        print(f"  📊 Tags: {len(self.registry['tags'])}")
    
    def write_registry(self):
        """Write registry to file"""
        print(f"\n💾 Writing registry to {self.output_file}...")
        
        with open(self.output_file, 'w') as f:
            yaml.dump(self.registry, f, default_flow_style=False, sort_keys=False)
        
        # Also create a JSON version for easier consumption by CLI
        json_file = self.output_file.with_suffix('.json')
        with open(json_file, 'w') as f:
            # Convert any remaining sets to lists for JSON serialization
            registry_json = json.loads(json.dumps(self.registry, default=list))
            json.dump(registry_json, f, indent=2)
        
        print(f"  ✓ YAML registry: {self.output_file}")
        print(f"  ✓ JSON registry: {json_file}")
    
    def generate_readme_snippet(self):
        """Generate README snippet with template list"""
        print("\n📝 Generating README snippet...")
        
        snippet = ["## Available Templates\n"]
        snippet.append(f"*Last updated: {datetime.now().strftime('%Y-%m-%d')}*\n")
        snippet.append(f"\nTotal templates: **{self.registry['stats']['total_templates']}** | ")
        snippet.append(f"Total versions: **{self.registry['stats']['total_versions']}**\n")
        
        # Group by category
        snippet.append("\n### By Category\n")
        for category, templates in sorted(self.registry["categories"].items()):
            snippet.append(f"\n#### {category.title()}\n")
            for template_name in templates:
                # Find template details
                template = next(t for t in self.registry["templates"] if t["name"] == template_name)
                snippet.append(f"- **[{template['displayName']}](templates/{template_name}/)** - {template['description']}\n")
        
        # Popular tags
        snippet.append("\n### Popular Tags\n")
        popular_tags = sorted(self.registry["tags"].items(), key=lambda x: len(x[1]), reverse=True)[:10]
        tag_list = [f"`{tag}` ({len(templates)})" for tag, templates in popular_tags]
        snippet.append(" | ".join(tag_list))
        
        return "".join(snippet)
    
    def run(self):
        """Run the registry builder"""
        print("🚀 PolicyStack Marketplace Registry Builder\n")
        
        if not self.templates_dir.exists():
            print(f"❌ Templates directory not found: {self.templates_dir}")
            return 1
        
        self.scan_templates()
        self.build_index()
        self.write_registry()
        
        # Print README snippet
        snippet = self.generate_readme_snippet()
        print("\n" + "="*60)
        print("README Snippet (copy to README.md):")
        print("="*60)
        print(snippet)
        
        print("\n✅ Registry build complete!")
        return 0


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Build PolicyStack Marketplace registry")
    parser.add_argument(
        "--templates-dir",
        default="templates",
        help="Directory containing template subdirectories (default: templates)"
    )
    parser.add_argument(
        "--output",
        default="registry.yaml",
        help="Output file for registry (default: registry.yaml)"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate metadata files without building registry"
    )
    
    args = parser.parse_args()
    
    builder = RegistryBuilder(args.templates_dir, args.output)
    return builder.run()


if __name__ == "__main__":
    exit(main())
