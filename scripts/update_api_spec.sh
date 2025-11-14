#!/bin/sh
curl -sL https://packages.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/packages.openapi.yaml
curl -sL https://repos.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/repos.openapi.yaml
curl -sL https://advisories.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/advisories.openapi.yaml

curl -sL https://timeline.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/timeline.openapi.yaml
curl -sL https://commits.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/commits.openapi.yaml
curl -sL https://issues.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/issues.openapi.yaml
curl -sL https://sponsors.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/sponsors.openapi.yaml
curl -sL https://docker.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/docker.openapi.yaml
curl -sL https://opencollective.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/opencollective.openapi.yaml
curl -sL https://dependabot.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/dependabot.openapi.yaml

curl -sL https://parser.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/parser.openapi.yaml
curl -sL https://resolve.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/resolve.openapi.yaml
curl -sL https://sbom.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/sbom.openapi.yaml
curl -sL https://licenses.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/licenses.openapi.yaml
curl -sL https://archives.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/archives.openapi.yaml
curl -sL https://diff.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/diff.openapi.yaml
curl -sL https://diff.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/diff.openapi.yaml
curl -sL https://summary.ecosyste.ms/docs/api/v1/openapi.yaml > ecosystems_cli/apis/summary.openapi.yaml
