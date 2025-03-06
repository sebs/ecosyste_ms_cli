# ecosyste_ms_cli.clients.packages.NamespacesApi

All URIs are relative to *https://packages.ecosyste.ms/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_registry_namespace**](NamespacesApi.md#get_registry_namespace) | **GET** /registries/{registryName}/namespaces/{namespaceName} | get a namespace by name
[**get_registry_namespace_packages**](NamespacesApi.md#get_registry_namespace_packages) | **GET** /registries/{registryName}/namespaces/{namespaceName}/packages | get packages for a namespace by login or UUID
[**get_registry_namespaces**](NamespacesApi.md#get_registry_namespaces) | **GET** /registries/{registryName}/namespaces | get a list of namespaces from a registry


# **get_registry_namespace**
> Namespace get_registry_namespace(registry_name, namespace_name)

get a namespace by name

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.namespace import Namespace
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
    api_instance = ecosyste_ms_cli.clients.packages.NamespacesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    namespace_name = 'namespace_name_example' # str | name of namespace

    try:
        # get a namespace by name
        api_response = api_instance.get_registry_namespace(registry_name, namespace_name)
        print("The response of NamespacesApi->get_registry_namespace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NamespacesApi->get_registry_namespace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **namespace_name** | **str**| name of namespace | 

### Return type

[**Namespace**](Namespace.md)

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

# **get_registry_namespace_packages**
> List[Package] get_registry_namespace_packages(registry_name, namespace_name, page=page, per_page=per_page)

get packages for a namespace by login or UUID

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.package import Package
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
    api_instance = ecosyste_ms_cli.clients.packages.NamespacesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    namespace_name = 'namespace_name_example' # str | lname of namespace
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)

    try:
        # get packages for a namespace by login or UUID
        api_response = api_instance.get_registry_namespace_packages(registry_name, namespace_name, page=page, per_page=per_page)
        print("The response of NamespacesApi->get_registry_namespace_packages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NamespacesApi->get_registry_namespace_packages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **namespace_name** | **str**| lname of namespace | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 

### Return type

[**List[Package]**](Package.md)

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

# **get_registry_namespaces**
> List[Namespace] get_registry_namespaces(registry_name, page=page, per_page=per_page)

get a list of namespaces from a registry

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.namespace import Namespace
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
    api_instance = ecosyste_ms_cli.clients.packages.NamespacesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)

    try:
        # get a list of namespaces from a registry
        api_response = api_instance.get_registry_namespaces(registry_name, page=page, per_page=per_page)
        print("The response of NamespacesApi->get_registry_namespaces:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NamespacesApi->get_registry_namespaces: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 

### Return type

[**List[Namespace]**](Namespace.md)

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

