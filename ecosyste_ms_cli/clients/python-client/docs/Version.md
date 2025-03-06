# Version


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**number** | **str** |  | 
**published_at** | **str** |  | 
**licenses** | **str** |  | 
**integrity** | **str** |  | 
**status** | **str** |  | 
**download_url** | **str** |  | 
**registry_url** | **str** |  | 
**documentation_url** | **str** |  | 
**install_command** | **str** |  | 
**metadata** | **object** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 
**purl** | **str** |  | 
**version_url** | **str** |  | 
**related_tag** | **object** |  | 

## Example

```python
from ecosyste_ms_cli.clients.packages.models.version import Version

# TODO update the JSON string below
json = "{}"
# create an instance of Version from a JSON string
version_instance = Version.from_json(json)
# print the JSON string representation of the object
print(Version.to_json())

# convert the object into a dict
version_dict = version_instance.to_dict()
# create an instance of Version from a dict
version_from_dict = Version.from_dict(version_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


