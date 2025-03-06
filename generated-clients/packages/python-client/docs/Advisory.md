# Advisory


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uuid** | **str** |  | 
**url** | **str** |  | 
**title** | **str** |  | 
**description** | **str** |  | 
**origin** | **str** |  | 
**severity** | **str** |  | 
**published_at** | **str** |  | 
**withdrawn_at** | **str** |  | 
**classification** | **str** |  | 
**cvss_score** | **float** |  | 
**cvss_vector** | **str** |  | 
**references** | **List[Optional[str]]** |  | 
**source_kind** | **str** |  | 
**identifiers** | **List[Optional[str]]** |  | 
**packages** | **List[object]** |  | 
**created_at** | **str** |  | 
**updated_at** | **str** |  | 

## Example

```python
from ecosyste_ms_cli.clients.packages.models.advisory import Advisory

# TODO update the JSON string below
json = "{}"
# create an instance of Advisory from a JSON string
advisory_instance = Advisory.from_json(json)
# print the JSON string representation of the object
print(Advisory.to_json())

# convert the object into a dict
advisory_dict = advisory_instance.to_dict()
# create an instance of Advisory from a dict
advisory_from_dict = Advisory.from_dict(advisory_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


