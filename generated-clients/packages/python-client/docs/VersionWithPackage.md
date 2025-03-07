# VersionWithPackage


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
**latest** | **bool** |  | 
**version_url** | **str** |  | 
**package_url** | **str** |  | 

## Example

```python
from ecosyste_ms_cli.clients.packages.models.version_with_package import VersionWithPackage

# TODO update the JSON string below
json = "{}"
# create an instance of VersionWithPackage from a JSON string
version_with_package_instance = VersionWithPackage.from_json(json)
# print the JSON string representation of the object
print(VersionWithPackage.to_json())

# convert the object into a dict
version_with_package_dict = version_with_package_instance.to_dict()
# create an instance of VersionWithPackage from a dict
version_with_package_from_dict = VersionWithPackage.from_dict(version_with_package_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


