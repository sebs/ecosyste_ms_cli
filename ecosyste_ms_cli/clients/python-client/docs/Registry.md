# Registry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**url** | **str** |  | 
**ecosystem** | **str** |  | 
**default** | **bool** |  | 
**packages_count** | **int** |  | 
**versions_count** | **int** |  | [optional] 
**maintainers_count** | **int** |  | 
**namespaces_count** | **int** |  | 
**keywords_count** | **int** |  | 
**downloads** | **int** |  | 
**github** | **str** |  | 
**metadata** | **object** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 
**packages_url** | **str** |  | 
**maintainers_url** | **str** |  | 
**icon_url** | **str** |  | 
**purl_type** | **str** |  | 

## Example

```python
from ecosyste_ms_cli.clients.packages.models.registry import Registry

# TODO update the JSON string below
json = "{}"
# create an instance of Registry from a JSON string
registry_instance = Registry.from_json(json)
# print the JSON string representation of the object
print(Registry.to_json())

# convert the object into a dict
registry_dict = registry_instance.to_dict()
# create an instance of Registry from a dict
registry_from_dict = Registry.from_dict(registry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


