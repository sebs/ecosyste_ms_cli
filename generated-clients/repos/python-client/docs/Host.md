# Host


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**url** | **str** |  | [optional] 
**kind** | **str** |  | [optional] 
**repositories_count** | **int** |  | [optional] 
**owners_count** | **int** |  | [optional] 
**icon_url** | **str** |  | [optional] 
**host_url** | **str** |  | [optional] 
**repositoris_url** | **str** |  | [optional] 
**repository_names_url** | **str** |  | [optional] 
**owners_url** | **str** |  | [optional] 
**version** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 

## Example

```python
from ecosyste_ms_cli.clients.repos.models.host import Host

# TODO update the JSON string below
json = "{}"
# create an instance of Host from a JSON string
host_instance = Host.from_json(json)
# print the JSON string representation of the object
print(Host.to_json())

# convert the object into a dict
host_dict = host_instance.to_dict()
# create an instance of Host from a dict
host_from_dict = Host.from_dict(host_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


