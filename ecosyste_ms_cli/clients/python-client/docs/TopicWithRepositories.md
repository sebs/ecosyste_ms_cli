# TopicWithRepositories


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**repositories_count** | **int** |  | [optional] 
**topic_url** | **str** |  | [optional] 
**related_topics** | [**List[Topic]**](Topic.md) |  | [optional] 
**repositories** | [**List[Repository]**](Repository.md) |  | [optional] 

## Example

```python
from ecosyste_ms_cli.clients.repos.models.topic_with_repositories import TopicWithRepositories

# TODO update the JSON string below
json = "{}"
# create an instance of TopicWithRepositories from a JSON string
topic_with_repositories_instance = TopicWithRepositories.from_json(json)
# print the JSON string representation of the object
print(TopicWithRepositories.to_json())

# convert the object into a dict
topic_with_repositories_dict = topic_with_repositories_instance.to_dict()
# create an instance of TopicWithRepositories from a dict
topic_with_repositories_from_dict = TopicWithRepositories.from_dict(topic_with_repositories_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


