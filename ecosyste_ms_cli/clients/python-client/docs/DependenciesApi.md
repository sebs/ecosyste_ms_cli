# ecosyste_ms_cli.clients.packages.DependenciesApi

All URIs are relative to *https://packages.ecosyste.ms/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_dependencies**](DependenciesApi.md#get_dependencies) | **GET** /dependencies | list dependencies


# **get_dependencies**
> List[Dependency] get_dependencies(page=page, per_page=per_page, ecosystem=ecosystem, package_name=package_name, package_id=package_id, requirements=requirements, kind=kind, optional=optional, after=after)

list dependencies

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.dependency import Dependency
from ecosyste_ms_cli.clients.packages.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://packages.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.packages.Configuration(
    host = "https://packages.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.packages.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.packages.DependenciesApi(api_client)
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    ecosystem = 'ecosystem_example' # str | ecosystem name (optional)
    package_name = 'package_name_example' # str | package name (optional)
    package_id = 'package_id_example' # str | package id (optional)
    requirements = 'requirements_example' # str | requirements (optional)
    kind = 'kind_example' # str | kind (optional)
    optional = True # bool | optional (optional)
    after = 'after_example' # str | filter by id after given id (optional)

    try:
        # list dependencies
        api_response = api_instance.get_dependencies(page=page, per_page=per_page, ecosystem=ecosystem, package_name=package_name, package_id=package_id, requirements=requirements, kind=kind, optional=optional, after=after)
        print("The response of DependenciesApi->get_dependencies:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DependenciesApi->get_dependencies: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **ecosystem** | **str**| ecosystem name | [optional] 
 **package_name** | **str**| package name | [optional] 
 **package_id** | **str**| package id | [optional] 
 **requirements** | **str**| requirements | [optional] 
 **kind** | **str**| kind | [optional] 
 **optional** | **bool**| optional | [optional] 
 **after** | **str**| filter by id after given id | [optional] 

### Return type

[**List[Dependency]**](Dependency.md)

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

