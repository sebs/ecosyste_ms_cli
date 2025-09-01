#!/bin/sh
curl -sL https://packages.ecosyste.ms/docs/api/v1/openapi.yaml > apis/packages.openapi.yaml
curl -sL https://repos.ecosyste.ms/docs/api/v1/openapi.yaml > apis/repos.openapi.yaml
curl -sL https://advisories.ecosyste.ms/docs/api/v1/openapi.yaml > apis/advisories.openapi.yaml

curl -sL https://timeline.ecosyste.ms/docs/api/v1/openapi.yaml > apis/timeline.openapi.yaml
curl -sL https://commits.ecosyste.ms/docs/api/v1/openapi.yaml > apis/commits.openapi.yaml
curl -sL https://issues.ecosyste.ms/docs/api/v1/openapi.yaml > apis/issues.openapi.yaml
curl -sL https://sponsors.ecosyste.ms/docs/api/v1/openapi.yaml > apis/sponsors.openapi.yaml
curl -sL https://docker.ecosyste.ms/docs/api/v1/openapi.yaml > apis/docker.openapi.yaml
