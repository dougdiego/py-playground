https://github.blog/changelog/2024-10-30-github-copilot-metrics-api-ga-release-now-available/
https://github.com/github-copilot-resources/copilot-metrics-viewer
https://github.com/github-copilot-resources/copilot-metrics-viewer/issues/15
```
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/prosperllc/copilot/usage \
  > usage.json


  curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/orgs/prosperllc/copilot/metrics \
  > metrics.json
```
