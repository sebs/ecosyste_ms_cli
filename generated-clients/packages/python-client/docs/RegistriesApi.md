# ecosyste_ms_cli.clients.packages.RegistriesApi

All URIs are relative to *https://packages.ecosyste.ms/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_registries**](RegistriesApi.md#get_registries) | **GET** /registries | list registies
[**get_registry**](RegistriesApi.md#get_registry) | **GET** /registries/{registryName} | get a registry by name


# **get_registries**
> List[Registry] get_registries(page=page, per_page=per_page)

list registies

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.registry import Registry
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
    api_instance = ecosyste_ms_cli.clients.packages.RegistriesApi(api_client)
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)

    try:
        # list registies
        api_response = api_instance.get_registries(page=page, per_page=per_page)
        print("The response of RegistriesApi->get_registries:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistriesApi->get_registries: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 

### Return type

[**List[Registry]**](Registry.md)

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

# **get_registry**
> Registry get_registry(registry_name, page=page, per_page=per_page)

get a registry by name

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.registry import Registry
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
    api_instance = ecosyste_ms_cli.clients.packages.RegistriesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)

    try:
        # get a registry by name
        api_response = api_instance.get_registry(registry_name, page=page, per_page=per_page)
        print("The response of RegistriesApi->get_registry:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RegistriesApi->get_registry: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 

### Return type

[**Registry**](Registry.md)

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

