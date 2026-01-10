# Actual Budget
Deployment files and utility scripts for my Actual Budget instances.

## Deploying
1. `brew install flyctl`
2. `fly auth login`
3. copy template `fly.toml`
4. resources should be cpu-shared-1x, 256MB ram, 1-3GB volume
4. `fly deploy`

## Updating
1. Server update: `fly deploy`
2. UI update: `ctrl + shift + R` (hard reload)

## Scripts
- `python scripts/venmo.py ~/Downloads` - parses and combines monthly venmo statements
- `python scripts/bofa.py ~/Downloads` - combines monthly BofA statements
