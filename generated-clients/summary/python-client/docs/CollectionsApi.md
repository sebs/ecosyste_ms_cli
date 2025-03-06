# ecosyste_ms_cli.clients.summary.CollectionsApi

All URIs are relative to *https://summary.ecosyste.ms/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_collection**](CollectionsApi.md#get_collection) | **GET** /collections/{id} | get a collection by id
[**get_collection_projects**](CollectionsApi.md#get_collection_projects) | **GET** /collections/{id}/projects | get projects in a collection
[**get_collections**](CollectionsApi.md#get_collections) | **GET** /collections | get collections


# **get_collection**
> Collection get_collection(id)

get a collection by id

### Example


```python
import ecosyste_ms_cli.clients.summary
from ecosyste_ms_cli.clients.summary.models.collection import Collection
from ecosyste_ms_cli.clients.summary.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://summary.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.summary.Configuration(
    host = "https://summary.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.summary.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.summary.CollectionsApi(api_client)
    id = 56 # int | id of the collection

    try:
        # get a collection by id
        api_response = api_instance.get_collection(id)
        print("The response of CollectionsApi->get_collection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->get_collection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| id of the collection | 

### Return type

[**Collection**](Collection.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_collection_projects**
> List[Project] get_collection_projects(id, page=page, per_page=per_page)

get projects in a collection

### Example


```python
import ecosyste_ms_cli.clients.summary
from ecosyste_ms_cli.clients.summary.models.project import Project
from ecosyste_ms_cli.clients.summary.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://summary.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.summary.Configuration(
    host = "https://summary.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.summary.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.summary.CollectionsApi(api_client)
    id = 56 # int | id of the collection
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)

    try:
        # get projects in a collection
        api_response = api_instance.get_collection_projects(id, page=page, per_page=per_page)
        print("The response of CollectionsApi->get_collection_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->get_collection_projects: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| id of the collection | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 

### Return type

[**List[Project]**](Project.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_collections**
> List[Collection] get_collections(page=page, per_page=per_page)

get collections

### Example


```python
import ecosyste_ms_cli.clients.summary
from ecosyste_ms_cli.clients.summary.models.collection import Collection
from ecosyste_ms_cli.clients.summary.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://summary.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.summary.Configuration(
    host = "https://summary.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.summary.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.summary.CollectionsApi(api_client)
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)

    try:
        # get collections
        api_response = api_instance.get_collections(page=page, per_page=per_page)
        print("The response of CollectionsApi->get_collections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->get_collections: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 

### Return type

[**List[Collection]**](Collection.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

