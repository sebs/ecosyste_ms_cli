# ecosyste_ms_cli.clients.summary.ProjectsApi

All URIs are relative to *https://summary.ecosyste.ms/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_project**](ProjectsApi.md#get_project) | **GET** /projects/{id} | get a project by id
[**get_projects**](ProjectsApi.md#get_projects) | **GET** /projects | get projects
[**lookup_project**](ProjectsApi.md#lookup_project) | **GET** /projects/lookup | lookup project by url


# **get_project**
> Project get_project(id)

get a project by id

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
    api_instance = ecosyste_ms_cli.clients.summary.ProjectsApi(api_client)
    id = 56 # int | id of the project

    try:
        # get a project by id
        api_response = api_instance.get_project(id)
        print("The response of ProjectsApi->get_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->get_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| id of the project | 

### Return type

[**Project**](Project.md)

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

# **get_projects**
> List[Project] get_projects(page=page, per_page=per_page)

get projects

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
    api_instance = ecosyste_ms_cli.clients.summary.ProjectsApi(api_client)
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)

    try:
        # get projects
        api_response = api_instance.get_projects(page=page, per_page=per_page)
        print("The response of ProjectsApi->get_projects:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->get_projects: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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

# **lookup_project**
> Project lookup_project(url)

lookup project by url

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
    api_instance = ecosyste_ms_cli.clients.summary.ProjectsApi(api_client)
    url = 'url_example' # str | url of the project

    try:
        # lookup project by url
        api_response = api_instance.lookup_project(url)
        print("The response of ProjectsApi->lookup_project:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProjectsApi->lookup_project: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| url of the project | 

### Return type

[**Project**](Project.md)

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

