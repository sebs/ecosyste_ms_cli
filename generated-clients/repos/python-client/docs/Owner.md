# Owner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**uuid** | **str** |  | [optional] 
**kind** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**login** | **str** |  | [optional] 
**company** | **str** |  | [optional] 
**location** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**twitter** | **str** |  | [optional] 
**website** | **str** |  | [optional] 
**metadata** | **object** |  | [optional] 
**icon_url** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**repositories_count** | **int** |  | [optional] 
**last_synced_at** | **datetime** |  | [optional] 
**owner_url** | **str** |  | [optional] 
**repositories_url** | **str** |  | [optional] 
**html_url** | **str** |  | [optional] 
**funding_links** | **List[str]** |  | [optional] 
**total_stars** | **int** |  | [optional] 
**followers** | **int** |  | [optional] 
**following** | **int** |  | [optional] 

## Example

```python
from ecosyste_ms_cli.clients.repos.models.owner import Owner

# TODO update the JSON string below
json = "{}"
# create an instance of Owner from a JSON string
owner_instance = Owner.from_json(json)
# print the JSON string representation of the object
print(Owner.to_json())

# convert the object into a dict
owner_dict = owner_instance.to_dict()
# create an instance of Owner from a dict
owner_from_dict = Owner.from_dict(owner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


