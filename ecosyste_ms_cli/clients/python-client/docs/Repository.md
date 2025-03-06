# Repository


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**uuid** | **str** |  | [optional] 
**full_name** | **str** |  | [optional] 
**owner** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**archived** | **bool** |  | [optional] 
**fork** | **bool** |  | [optional] 
**pushed_at** | **datetime** |  | [optional] 
**size** | **int** |  | [optional] 
**stargazers_count** | **int** |  | [optional] 
**open_issues_count** | **int** |  | [optional] 
**forks_count** | **int** |  | [optional] 
**subscribers_count** | **int** |  | [optional] 
**default_branch** | **str** |  | [optional] 
**last_synced_at** | **datetime** |  | [optional] 
**etag** | **str** |  | [optional] 
**topics** | **List[str]** |  | [optional] 
**latest_commit_sha** | **str** |  | [optional] 
**homepage** | **str** |  | [optional] 
**language** | **str** |  | [optional] 
**has_issues** | **bool** |  | [optional] 
**has_wiki** | **bool** |  | [optional] 
**has_pages** | **bool** |  | [optional] 
**mirror_url** | **str** |  | [optional] 
**source_name** | **str** |  | [optional] 
**license** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**scm** | **str** |  | [optional] 
**pull_requests_enabled** | **bool** |  | [optional] 
**icon_url** | **str** |  | [optional] 
**metadata** | **object** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**dependencies_parsed_at** | **datetime** |  | [optional] 
**dependency_job_id** | **str** |  | [optional] 
**html_url** | **str** |  | [optional] 
**previous_names** | **List[str]** |  | [optional] 
**tags_count** | **int** |  | [optional] 
**template** | **bool** |  | [optional] 
**template_full_name** | **str** |  | [optional] 
**latest_tag_name** | **str** |  | [optional] 
**latest_tag_published_at** | **datetime** |  | [optional] 
**repository_url** | **str** |  | [optional] 
**tags_url** | **str** |  | [optional] 
**releases_url** | **str** |  | [optional] 
**manifests_url** | **str** |  | [optional] 
**owner_url** | **str** |  | [optional] 
**download_url** | **str** |  | [optional] 
**commit_stats** | **object** |  | [optional] 
**host** | [**Host**](.md) |  | [optional] 

## Example

```python
from ecosyste_ms_cli.clients.repos.models.repository import Repository

# TODO update the JSON string below
json = "{}"
# create an instance of Repository from a JSON string
repository_instance = Repository.from_json(json)
# print the JSON string representation of the object
print(Repository.to_json())

# convert the object into a dict
repository_dict = repository_instance.to_dict()
# create an instance of Repository from a dict
repository_from_dict = Repository.from_dict(repository_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


