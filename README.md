# composer
An easy-to-use deployment platform based on docker-compose.

# Installation
## Requirements
- Ubuntu 12.04, 14.04, 16.04
- Python 3
- Docker (https://docs.docker.com/engine/installation/)
- Docker Compose (https://docs.docker.com/compose/install/)

Firstly download the install script and make it executable:
```
wget https://raw.githubusercontent.com/gitcommitpush/composer/master/install.sh
chmod +x install.sh
```

Then, run it:
```
./install.sh
cd composer
```

# Usage
## Creating Applications
```
./composer app create <app_name>
./composer app clone <app_name> <github_clone_url>
./composer compose up <app_name>
```

More detailed documentation will come soon.
