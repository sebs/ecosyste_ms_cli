#!/bin/sh
curl -sL https://advisories.ecosyste.ms/docs/api/v1/openapi.yaml > apis/advisories.openapi.yaml
curl -sL https://packages.ecosyste.ms/docs/api/v1/openapi.yaml > apis/packages.openapi.yaml
