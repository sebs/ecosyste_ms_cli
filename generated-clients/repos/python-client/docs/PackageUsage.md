# PackageUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ecosystem** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**dependents_count** | **int** |  | [optional] 
**package_usage_url** | **str** |  | [optional] 
**dependencies_url** | **str** |  | [optional] 

## Example

```python
from ecosyste_ms_cli.clients.repos.models.package_usage import PackageUsage

# TODO update the JSON string below
json = "{}"
# create an instance of PackageUsage from a JSON string
package_usage_instance = PackageUsage.from_json(json)
# print the JSON string representation of the object
print(PackageUsage.to_json())

# convert the object into a dict
package_usage_dict = package_usage_instance.to_dict()
# create an instance of PackageUsage from a dict
package_usage_from_dict = PackageUsage.from_dict(package_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


