# Ecosystem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**packages_count** | **int** |  | [optional] 
**ecosystem_url** | **str** |  | [optional] 

## Example

```python
from ecosyste_ms_cli.clients.repos.models.ecosystem import Ecosystem

# TODO update the JSON string below
json = "{}"
# create an instance of Ecosystem from a JSON string
ecosystem_instance = Ecosystem.from_json(json)
# print the JSON string representation of the object
print(Ecosystem.to_json())

# convert the object into a dict
ecosystem_dict = ecosystem_instance.to_dict()
# create an instance of Ecosystem from a dict
ecosystem_from_dict = Ecosystem.from_dict(ecosystem_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


