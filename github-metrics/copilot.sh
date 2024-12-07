# Load environment variables from .env file
source .env

curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/enterprises/prosper-llc/copilot/metrics > output.json