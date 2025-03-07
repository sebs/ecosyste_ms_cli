# KeywordWithPackages


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**packages_count** | **int** |  | 
**packages_url** | **str** |  | 
**related_keywords** | [**List[Keyword]**](Keyword.md) |  | 
**packages** | [**List[Package]**](Package.md) |  | 

## Example

```python
from ecosyste_ms_cli.clients.packages.models.keyword_with_packages import KeywordWithPackages

# TODO update the JSON string below
json = "{}"
# create an instance of KeywordWithPackages from a JSON string
keyword_with_packages_instance = KeywordWithPackages.from_json(json)
# print the JSON string representation of the object
print(KeywordWithPackages.to_json())

# convert the object into a dict
keyword_with_packages_dict = keyword_with_packages_instance.to_dict()
# create an instance of KeywordWithPackages from a dict
keyword_with_packages_from_dict = KeywordWithPackages.from_dict(keyword_with_packages_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


