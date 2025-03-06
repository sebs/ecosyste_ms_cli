# PackageWithRegistry


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**ecosystem** | **str** |  | 
**description** | **str** |  | 
**homepage** | **str** |  | 
**licenses** | **str** |  | 
**normalized_licenses** | **List[str]** |  | 
**repository_url** | **str** |  | 
**keywords_array** | **List[str]** |  | 
**namespace** | **str** |  | 
**versions_count** | **int** |  | 
**first_release_published_at** | **datetime** |  | 
**latest_release_published_at** | **datetime** |  | 
**latest_release_number** | **str** |  | 
**last_synced_at** | **datetime** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 
**registry_url** | **str** |  | 
**documentation_url** | **str** |  | 
**install_command** | **str** |  | 
**metadata** | **object** |  | 
**repo_metadata** | **object** |  | 
**repo_metadata_updated_at** | **datetime** |  | 
**dependent_packages_count** | **int** |  | 
**downloads** | **int** |  | 
**downloads_period** | **str** |  | 
**dependent_repos_count** | **int** |  | 
**rankings** | **object** |  | 
**purl** | **str** |  | 
**advisories** | [**List[Advisory]**](Advisory.md) |  | 
**versions_url** | **str** |  | 
**version_numbers_url** | **str** |  | [optional] 
**dependent_packages_url** | **str** |  | 
**related_packages_url** | **str** |  | 
**docker_usage_url** | **str** |  | 
**docker_dependents_count** | **int** |  | 
**docker_downloads_count** | **int** |  | 
**usage_url** | **str** |  | 
**dependent_repositories_url** | **str** |  | 
**status** | **str** |  | 
**funding_links** | **List[str]** |  | 
**maintainers** | [**List[Maintainer]**](Maintainer.md) |  | 
**critical** | **bool** |  | 
**registry** | [**Registry**](Registry.md) |  | 

## Example

```python
from ecosyste_ms_cli.clients.packages.models.package_with_registry import PackageWithRegistry

# TODO update the JSON string below
json = "{}"
# create an instance of PackageWithRegistry from a JSON string
package_with_registry_instance = PackageWithRegistry.from_json(json)
# print the JSON string representation of the object
print(PackageWithRegistry.to_json())

# convert the object into a dict
package_with_registry_dict = package_with_registry_instance.to_dict()
# create an instance of PackageWithRegistry from a dict
package_with_registry_from_dict = PackageWithRegistry.from_dict(package_with_registry_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


