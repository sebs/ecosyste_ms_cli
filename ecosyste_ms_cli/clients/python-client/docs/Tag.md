# Tag


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**sha** | **str** |  | [optional] 
**kind** | **str** |  | [optional] 
**published_at** | **datetime** |  | [optional] 
**download_url** | **str** |  | [optional] 
**html_url** | **str** |  | [optional] 
**dependencies_parsed_at** | **datetime** |  | [optional] 
**dependency_job_id** | **str** |  | [optional] 
**tag_url** | **str** |  | [optional] 
**manifests_url** | **str** |  | [optional] 

## Example

```python
from ecosyste_ms_cli.clients.repos.models.tag import Tag

# TODO update the JSON string below
json = "{}"
# create an instance of Tag from a JSON string
tag_instance = Tag.from_json(json)
# print the JSON string representation of the object
print(Tag.to_json())

# convert the object into a dict
tag_dict = tag_instance.to_dict()
# create an instance of Tag from a dict
tag_from_dict = Tag.from_dict(tag_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


