# Release


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**uuid** | **str** |  | [optional] 
**tag_name** | **str** |  | [optional] 
**target_commitish** | **str** |  | [optional] 
**body** | **str** |  | [optional] 
**draft** | **bool** |  | [optional] 
**prerelease** | **bool** |  | [optional] 
**published_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**author** | **str** |  | [optional] 
**assets** | **List[object]** |  | [optional] 
**last_synced_at** | **datetime** |  | [optional] 
**tag_url** | **str** |  | [optional] 
**html_url** | **str** |  | [optional] 

## Example

```python
from ecosyste_ms_cli.clients.repos.models.release import Release

# TODO update the JSON string below
json = "{}"
# create an instance of Release from a JSON string
release_instance = Release.from_json(json)
# print the JSON string representation of the object
print(Release.to_json())

# convert the object into a dict
release_dict = release_instance.to_dict()
# create an instance of Release from a dict
release_from_dict = Release.from_dict(release_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


