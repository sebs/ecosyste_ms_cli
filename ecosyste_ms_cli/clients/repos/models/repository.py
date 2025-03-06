# coding: utf-8

"""
    Ecosyste.ms: Repos

    An open API service providing repository metadata for many open source software ecosystems.

    The version of the OpenAPI document: 1.0.0
    Contact: support@ecosyste.ms
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class Repository(BaseModel):
    """
    Repository
    """ # noqa: E501
    id: Optional[StrictInt] = None
    uuid: Optional[StrictStr] = None
    full_name: Optional[StrictStr] = None
    owner: Optional[StrictStr] = None
    description: Optional[StrictStr] = None
    archived: Optional[StrictBool] = None
    fork: Optional[StrictBool] = None
    pushed_at: Optional[datetime] = None
    size: Optional[StrictInt] = None
    stargazers_count: Optional[StrictInt] = None
    open_issues_count: Optional[StrictInt] = None
    forks_count: Optional[StrictInt] = None
    subscribers_count: Optional[StrictInt] = None
    default_branch: Optional[StrictStr] = None
    last_synced_at: Optional[datetime] = None
    etag: Optional[StrictStr] = None
    topics: Optional[List[StrictStr]] = None
    latest_commit_sha: Optional[StrictStr] = None
    homepage: Optional[StrictStr] = None
    language: Optional[StrictStr] = None
    has_issues: Optional[StrictBool] = None
    has_wiki: Optional[StrictBool] = None
    has_pages: Optional[StrictBool] = None
    mirror_url: Optional[StrictStr] = None
    source_name: Optional[StrictStr] = None
    license: Optional[StrictStr] = None
    status: Optional[StrictStr] = None
    scm: Optional[StrictStr] = None
    pull_requests_enabled: Optional[StrictBool] = None
    icon_url: Optional[StrictStr] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    dependencies_parsed_at: Optional[datetime] = None
    dependency_job_id: Optional[StrictStr] = None
    html_url: Optional[StrictStr] = None
    previous_names: Optional[List[StrictStr]] = None
    tags_count: Optional[StrictInt] = None
    template: Optional[StrictBool] = None
    template_full_name: Optional[StrictStr] = None
    latest_tag_name: Optional[StrictStr] = None
    latest_tag_published_at: Optional[datetime] = None
    repository_url: Optional[StrictStr] = None
    tags_url: Optional[StrictStr] = None
    releases_url: Optional[StrictStr] = None
    manifests_url: Optional[StrictStr] = None
    owner_url: Optional[StrictStr] = None
    download_url: Optional[StrictStr] = None
    commit_stats: Optional[Dict[str, Any]] = None
    host: Optional[Dict[str, Any]] = None
    __properties: ClassVar[List[str]] = ["id", "uuid", "full_name", "owner", "description", "archived", "fork", "pushed_at", "size", "stargazers_count", "open_issues_count", "forks_count", "subscribers_count", "default_branch", "last_synced_at", "etag", "topics", "latest_commit_sha", "homepage", "language", "has_issues", "has_wiki", "has_pages", "mirror_url", "source_name", "license", "status", "scm", "pull_requests_enabled", "icon_url", "metadata", "created_at", "updated_at", "dependencies_parsed_at", "dependency_job_id", "html_url", "previous_names", "tags_count", "template", "template_full_name", "latest_tag_name", "latest_tag_published_at", "repository_url", "tags_url", "releases_url", "manifests_url", "owner_url", "download_url", "commit_stats", "host"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Repository from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of host
        if self.host:
            _dict['host'] = self.host.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Repository from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "uuid": obj.get("uuid"),
            "full_name": obj.get("full_name"),
            "owner": obj.get("owner"),
            "description": obj.get("description"),
            "archived": obj.get("archived"),
            "fork": obj.get("fork"),
            "pushed_at": obj.get("pushed_at"),
            "size": obj.get("size"),
            "stargazers_count": obj.get("stargazers_count"),
            "open_issues_count": obj.get("open_issues_count"),
            "forks_count": obj.get("forks_count"),
            "subscribers_count": obj.get("subscribers_count"),
            "default_branch": obj.get("default_branch"),
            "last_synced_at": obj.get("last_synced_at"),
            "etag": obj.get("etag"),
            "topics": obj.get("topics"),
            "latest_commit_sha": obj.get("latest_commit_sha"),
            "homepage": obj.get("homepage"),
            "language": obj.get("language"),
            "has_issues": obj.get("has_issues"),
            "has_wiki": obj.get("has_wiki"),
            "has_pages": obj.get("has_pages"),
            "mirror_url": obj.get("mirror_url"),
            "source_name": obj.get("source_name"),
            "license": obj.get("license"),
            "status": obj.get("status"),
            "scm": obj.get("scm"),
            "pull_requests_enabled": obj.get("pull_requests_enabled"),
            "icon_url": obj.get("icon_url"),
            "metadata": obj.get("metadata"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "dependencies_parsed_at": obj.get("dependencies_parsed_at"),
            "dependency_job_id": obj.get("dependency_job_id"),
            "html_url": obj.get("html_url"),
            "previous_names": obj.get("previous_names"),
            "tags_count": obj.get("tags_count"),
            "template": obj.get("template"),
            "template_full_name": obj.get("template_full_name"),
            "latest_tag_name": obj.get("latest_tag_name"),
            "latest_tag_published_at": obj.get("latest_tag_published_at"),
            "repository_url": obj.get("repository_url"),
            "tags_url": obj.get("tags_url"),
            "releases_url": obj.get("releases_url"),
            "manifests_url": obj.get("manifests_url"),
            "owner_url": obj.get("owner_url"),
            "download_url": obj.get("download_url"),
            "commit_stats": obj.get("commit_stats"),
            "host": Host.from_dict(obj["host"]) if obj.get("host") is not None else None
        })
        return _obj


