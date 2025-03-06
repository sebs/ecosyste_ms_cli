# DependencyWithRepository


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**package_name** | **str** |  | [optional] 
**ecosystem** | **str** |  | [optional] 
**requirements** | **str** |  | [optional] 
**kind** | **str** |  | [optional] 
**direct** | **bool** |  | [optional] 
**optional** | **bool** |  | [optional] 
**repository** | [**Repository**](.md) |  | [optional] 
**manifest** | [**Manifest**](.md) |  | [optional] 

## Example

```python
from ecosyste_ms_cli.clients.repos.models.dependency_with_repository import DependencyWithRepository

# TODO update the JSON string below
json = "{}"
# create an instance of DependencyWithRepository from a JSON string
dependency_with_repository_instance = DependencyWithRepository.from_json(json)
# print the JSON string representation of the object
print(DependencyWithRepository.to_json())

# convert the object into a dict
dependency_with_repository_dict = dependency_with_repository_instance.to_dict()
# create an instance of DependencyWithRepository from a dict
dependency_with_repository_from_dict = DependencyWithRepository.from_dict(dependency_with_repository_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


