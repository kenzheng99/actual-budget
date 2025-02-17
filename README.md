# Actual Budget

## Deploying
1. `brew install flyctl`
2. `fly auth login`
3. copy template `fly.toml`
4. resources should be cpu-shared-1x, 256MB ram, 1-3GB volume
4. `fly deploy`

## Updating
1. Server update: `fly deploy`
2. UI update: `ctrl + shift + R` (hard reload)
