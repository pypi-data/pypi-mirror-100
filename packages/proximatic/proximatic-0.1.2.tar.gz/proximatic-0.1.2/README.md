# Proximatic

Python API for managing Proximatic configuration files.

When installed, the `proximatic` command provides a CLI for managing Proximatic configuration.

This Python package provides the core for the Proximatic system.

## Installation

```bash
pip install proximatic
```

## Usage

### Command Line Interface (CLI)

Open a Terminal and type:

```bash
proximatic
```

Use `proximatic --help` for available commands and options.

### Python API programmatic interface

```python
import proximatic

# List existing domains.
manager = proximatic.DomainsManager(yml_dir = '/path/to/your/data/traefik/conf/')
result = manager.domain_list()
for domain in result['domains']:
    for name, url in domain.items():
        print(f"{name} <=proxy=> {url}")

# Create new or update existing domain.

manager.set_fqdn('yourdomain.com') # change to your domain
result = manager.domain_update(subdomain = 'mysubdomain', url = 'https://news.ycombinator.com')

# See your newly created domain.
result = manager.domain_list()
for domain in result['domains']:
    for name, url in domain.items():
        print(f"{name} <=proxy=> {url}")

# Delete the domain.
result = manager.domain_delete('mysubdomain')
print(result)

# See that it is gone.
result = manager.domain_list()
for domain in result['domains']:
    for name, url in domain.items():
        print(f"{name} <=proxy=> {url}")
```

## License

The MIT License (MIT)

## Author

Link Swanson (LunkRat)