# VersionWithDependencies


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
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
**latest** | **bool** |  | 
**dependencies** | [**List[Dependency]**](Dependency.md) |  | 

## Example

```python
from ecosyste_ms_cli.clients.packages.models.version_with_dependencies import VersionWithDependencies

# TODO update the JSON string below
json = "{}"
# create an instance of VersionWithDependencies from a JSON string
version_with_dependencies_instance = VersionWithDependencies.from_json(json)
# print the JSON string representation of the object
print(VersionWithDependencies.to_json())

# convert the object into a dict
version_with_dependencies_dict = version_with_dependencies_instance.to_dict()
# create an instance of VersionWithDependencies from a dict
version_with_dependencies_from_dict = VersionWithDependencies.from_dict(version_with_dependencies_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


