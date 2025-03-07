# ecosyste_ms_cli.clients.packages.MaintainersApi

All URIs are relative to *https://packages.ecosyste.ms/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_registry_maintainer**](MaintainersApi.md#get_registry_maintainer) | **GET** /registries/{registryName}/maintainers/{MaintainerLoginOrUUID} | get a maintainer by login or UUID
[**get_registry_maintainer_packages**](MaintainersApi.md#get_registry_maintainer_packages) | **GET** /registries/{registryName}/maintainers/{MaintainerLoginOrUUID}/packages | get packages for a maintainer by login or UUID
[**get_registry_maintainers**](MaintainersApi.md#get_registry_maintainers) | **GET** /registries/{registryName}/maintainers | get a list of maintainers from a registry


# **get_registry_maintainer**
> Maintainer get_registry_maintainer(registry_name, maintainer_login_or_uuid)

get a maintainer by login or UUID

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.maintainer import Maintainer
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
    api_instance = ecosyste_ms_cli.clients.packages.MaintainersApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    maintainer_login_or_uuid = 'maintainer_login_or_uuid_example' # str | login or uuid of maintainer

    try:
        # get a maintainer by login or UUID
        api_response = api_instance.get_registry_maintainer(registry_name, maintainer_login_or_uuid)
        print("The response of MaintainersApi->get_registry_maintainer:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintainersApi->get_registry_maintainer: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **maintainer_login_or_uuid** | **str**| login or uuid of maintainer | 

### Return type

[**Maintainer**](Maintainer.md)

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

# **get_registry_maintainer_packages**
> List[Package] get_registry_maintainer_packages(registry_name, maintainer_login_or_uuid, page=page, per_page=per_page)

get packages for a maintainer by login or UUID

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
    api_instance = ecosyste_ms_cli.clients.packages.MaintainersApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    maintainer_login_or_uuid = 'maintainer_login_or_uuid_example' # str | login or uuid of maintainer
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)

    try:
        # get packages for a maintainer by login or UUID
        api_response = api_instance.get_registry_maintainer_packages(registry_name, maintainer_login_or_uuid, page=page, per_page=per_page)
        print("The response of MaintainersApi->get_registry_maintainer_packages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintainersApi->get_registry_maintainer_packages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **maintainer_login_or_uuid** | **str**| login or uuid of maintainer | 
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

# **get_registry_maintainers**
> List[Maintainer] get_registry_maintainers(registry_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, sort=sort, order=order)

get a list of maintainers from a registry

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.maintainer import Maintainer
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
    api_instance = ecosyste_ms_cli.clients.packages.MaintainersApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at after given time (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at after given time (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # get a list of maintainers from a registry
        api_response = api_instance.get_registry_maintainers(registry_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, sort=sort, order=order)
        print("The response of MaintainersApi->get_registry_maintainers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MaintainersApi->get_registry_maintainers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **created_after** | **datetime**| filter by created_at after given time | [optional] 
 **updated_after** | **datetime**| filter by updated_at after given time | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 

### Return type

[**List[Maintainer]**](Maintainer.md)

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

