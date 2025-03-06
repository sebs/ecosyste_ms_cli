# ecosyste_ms_cli.clients.packages.PackagesApi

All URIs are relative to *https://packages.ecosyste.ms/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_registry_package**](PackagesApi.md#get_registry_package) | **GET** /registries/{registryName}/packages/{packageName} | get a package by name
[**get_registry_package_dependent_package_kinds**](PackagesApi.md#get_registry_package_dependent_package_kinds) | **GET** /registries/{registryName}/packages/{packageName}/dependent_package_kinds | get a list of dependency kinds for a package
[**get_registry_package_dependent_packages**](PackagesApi.md#get_registry_package_dependent_packages) | **GET** /registries/{registryName}/packages/{packageName}/dependent_packages | get a list of packages that depend on a package
[**get_registry_package_names**](PackagesApi.md#get_registry_package_names) | **GET** /registries/{registryName}/package_names | get a list of package names from a registry
[**get_registry_package_related_packages**](PackagesApi.md#get_registry_package_related_packages) | **GET** /registries/{registryName}/packages/{packageName}/related_packages | get a list of packages that are related to a package
[**get_registry_package_version**](PackagesApi.md#get_registry_package_version) | **GET** /registries/{registryName}/packages/{packageName}/versions/{versionNumber} | get a version of a package
[**get_registry_package_version_numbers**](PackagesApi.md#get_registry_package_version_numbers) | **GET** /registries/{registryName}/packages/{packageName}/version_numbers | get a list of version numbers for a package from a registry
[**get_registry_package_versions**](PackagesApi.md#get_registry_package_versions) | **GET** /registries/{registryName}/packages/{packageName}/versions | get a list of versions for a package
[**get_registry_packages**](PackagesApi.md#get_registry_packages) | **GET** /registries/{registryName}/packages | get a list of packages from a registry
[**get_registry_recent_versions**](PackagesApi.md#get_registry_recent_versions) | **GET** /registries/{registryName}/versions | get a list of recently published versions from a registry
[**lookup_package**](PackagesApi.md#lookup_package) | **GET** /packages/lookup | lookup a package by repository URL, purl or ecosystem+name
[**lookup_registry_package**](PackagesApi.md#lookup_registry_package) | **GET** /registries/{registryName}/lookup | lookup a package within a registry by repository URL, purl or ecosystem+name


# **get_registry_package**
> Package get_registry_package(registry_name, package_name)

get a package by name

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
    api_instance = ecosyste_ms_cli.clients.packages.PackagesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    package_name = 'package_name_example' # str | name of package

    try:
        # get a package by name
        api_response = api_instance.get_registry_package(registry_name, package_name)
        print("The response of PackagesApi->get_registry_package:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PackagesApi->get_registry_package: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **package_name** | **str**| name of package | 

### Return type

[**Package**](Package.md)

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

# **get_registry_package_dependent_package_kinds**
> List[str] get_registry_package_dependent_package_kinds(registry_name, package_name, latest=latest)

get a list of dependency kinds for a package

### Example


```python
import ecosyste_ms_cli.clients.packages
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
    api_instance = ecosyste_ms_cli.clients.packages.PackagesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    package_name = 'package_name_example' # str | name of package
    latest = True # bool | filter by latest version (optional)

    try:
        # get a list of dependency kinds for a package
        api_response = api_instance.get_registry_package_dependent_package_kinds(registry_name, package_name, latest=latest)
        print("The response of PackagesApi->get_registry_package_dependent_package_kinds:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PackagesApi->get_registry_package_dependent_package_kinds: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **package_name** | **str**| name of package | 
 **latest** | **bool**| filter by latest version | [optional] 

### Return type

**List[str]**

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

# **get_registry_package_dependent_packages**
> List[Package] get_registry_package_dependent_packages(registry_name, package_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, sort=sort, order=order, latest=latest, kind=kind)

get a list of packages that depend on a package

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
    api_instance = ecosyste_ms_cli.clients.packages.PackagesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    package_name = 'package_name_example' # str | name of package
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at after given time (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at after given time (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)
    latest = True # bool | filter by latest version (optional)
    kind = 'kind_example' # str | filter by dependency kind (optional)

    try:
        # get a list of packages that depend on a package
        api_response = api_instance.get_registry_package_dependent_packages(registry_name, package_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, sort=sort, order=order, latest=latest, kind=kind)
        print("The response of PackagesApi->get_registry_package_dependent_packages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PackagesApi->get_registry_package_dependent_packages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **package_name** | **str**| name of package | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **created_after** | **datetime**| filter by created_at after given time | [optional] 
 **updated_after** | **datetime**| filter by updated_at after given time | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 
 **latest** | **bool**| filter by latest version | [optional] 
 **kind** | **str**| filter by dependency kind | [optional] 

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

# **get_registry_package_names**
> List[str] get_registry_package_names(registry_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, created_before=created_before, updated_before=updated_before, sort=sort, order=order)

get a list of package names from a registry

### Example


```python
import ecosyste_ms_cli.clients.packages
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
    api_instance = ecosyste_ms_cli.clients.packages.PackagesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at after given time (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at after given time (optional)
    created_before = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at before given time (optional)
    updated_before = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at before given time (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # get a list of package names from a registry
        api_response = api_instance.get_registry_package_names(registry_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, created_before=created_before, updated_before=updated_before, sort=sort, order=order)
        print("The response of PackagesApi->get_registry_package_names:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PackagesApi->get_registry_package_names: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **created_after** | **datetime**| filter by created_at after given time | [optional] 
 **updated_after** | **datetime**| filter by updated_at after given time | [optional] 
 **created_before** | **datetime**| filter by created_at before given time | [optional] 
 **updated_before** | **datetime**| filter by updated_at before given time | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 

### Return type

**List[str]**

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

# **get_registry_package_related_packages**
> List[Package] get_registry_package_related_packages(registry_name, package_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, sort=sort, order=order)

get a list of packages that are related to a package

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
    api_instance = ecosyste_ms_cli.clients.packages.PackagesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    package_name = 'package_name_example' # str | name of package
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at after given time (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at after given time (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # get a list of packages that are related to a package
        api_response = api_instance.get_registry_package_related_packages(registry_name, package_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, sort=sort, order=order)
        print("The response of PackagesApi->get_registry_package_related_packages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PackagesApi->get_registry_package_related_packages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **package_name** | **str**| name of package | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **created_after** | **datetime**| filter by created_at after given time | [optional] 
 **updated_after** | **datetime**| filter by updated_at after given time | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 

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

# **get_registry_package_version**
> VersionWithDependencies get_registry_package_version(registry_name, package_name, version_number)

get a version of a package

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.version_with_dependencies import VersionWithDependencies
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
    api_instance = ecosyste_ms_cli.clients.packages.PackagesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    package_name = 'package_name_example' # str | name of package
    version_number = 'version_number_example' # str | number of version

    try:
        # get a version of a package
        api_response = api_instance.get_registry_package_version(registry_name, package_name, version_number)
        print("The response of PackagesApi->get_registry_package_version:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PackagesApi->get_registry_package_version: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **package_name** | **str**| name of package | 
 **version_number** | **str**| number of version | 

### Return type

[**VersionWithDependencies**](VersionWithDependencies.md)

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

# **get_registry_package_version_numbers**
> List[str] get_registry_package_version_numbers(registry_name, package_name)

get a list of version numbers for a package from a registry

### Example


```python
import ecosyste_ms_cli.clients.packages
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
    api_instance = ecosyste_ms_cli.clients.packages.PackagesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    package_name = 'package_name_example' # str | name of package

    try:
        # get a list of version numbers for a package from a registry
        api_response = api_instance.get_registry_package_version_numbers(registry_name, package_name)
        print("The response of PackagesApi->get_registry_package_version_numbers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PackagesApi->get_registry_package_version_numbers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **package_name** | **str**| name of package | 

### Return type

**List[str]**

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

# **get_registry_package_versions**
> List[Version] get_registry_package_versions(registry_name, package_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, published_after=published_after, published_before=published_before, created_before=created_before, updated_before=updated_before, sort=sort, order=order)

get a list of versions for a package

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.version import Version
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
    api_instance = ecosyste_ms_cli.clients.packages.PackagesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    package_name = 'package_name_example' # str | name of package
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at after given time (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at after given time (optional)
    published_after = '2013-10-20T19:20:30+01:00' # datetime | filter by published_at after given time (optional)
    published_before = '2013-10-20T19:20:30+01:00' # datetime | filter by published_at before given time (optional)
    created_before = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at before given time (optional)
    updated_before = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at before given time (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # get a list of versions for a package
        api_response = api_instance.get_registry_package_versions(registry_name, package_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, published_after=published_after, published_before=published_before, created_before=created_before, updated_before=updated_before, sort=sort, order=order)
        print("The response of PackagesApi->get_registry_package_versions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PackagesApi->get_registry_package_versions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **package_name** | **str**| name of package | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **created_after** | **datetime**| filter by created_at after given time | [optional] 
 **updated_after** | **datetime**| filter by updated_at after given time | [optional] 
 **published_after** | **datetime**| filter by published_at after given time | [optional] 
 **published_before** | **datetime**| filter by published_at before given time | [optional] 
 **created_before** | **datetime**| filter by created_at before given time | [optional] 
 **updated_before** | **datetime**| filter by updated_at before given time | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 

### Return type

[**List[Version]**](Version.md)

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

# **get_registry_packages**
> List[Package] get_registry_packages(registry_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, created_before=created_before, updated_before=updated_before, critical=critical, sort=sort, order=order)

get a list of packages from a registry

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
    api_instance = ecosyste_ms_cli.clients.packages.PackagesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at after given time (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at after given time (optional)
    created_before = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at before given time (optional)
    updated_before = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at before given time (optional)
    critical = True # bool | filter by critical packages (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # get a list of packages from a registry
        api_response = api_instance.get_registry_packages(registry_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, created_before=created_before, updated_before=updated_before, critical=critical, sort=sort, order=order)
        print("The response of PackagesApi->get_registry_packages:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PackagesApi->get_registry_packages: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **created_after** | **datetime**| filter by created_at after given time | [optional] 
 **updated_after** | **datetime**| filter by updated_at after given time | [optional] 
 **created_before** | **datetime**| filter by created_at before given time | [optional] 
 **updated_before** | **datetime**| filter by updated_at before given time | [optional] 
 **critical** | **bool**| filter by critical packages | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 

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

# **get_registry_recent_versions**
> List[VersionWithPackage] get_registry_recent_versions(registry_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, published_after=published_after, published_before=published_before, created_before=created_before, updated_before=updated_before, sort=sort, order=order)

get a list of recently published versions from a registry

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.version_with_package import VersionWithPackage
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
    api_instance = ecosyste_ms_cli.clients.packages.PackagesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at after given time (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at after given time (optional)
    published_after = '2013-10-20T19:20:30+01:00' # datetime | filter by published_at after given time (optional)
    published_before = '2013-10-20T19:20:30+01:00' # datetime | filter by published_at before given time (optional)
    created_before = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at before given time (optional)
    updated_before = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at before given time (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # get a list of recently published versions from a registry
        api_response = api_instance.get_registry_recent_versions(registry_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, published_after=published_after, published_before=published_before, created_before=created_before, updated_before=updated_before, sort=sort, order=order)
        print("The response of PackagesApi->get_registry_recent_versions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PackagesApi->get_registry_recent_versions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **created_after** | **datetime**| filter by created_at after given time | [optional] 
 **updated_after** | **datetime**| filter by updated_at after given time | [optional] 
 **published_after** | **datetime**| filter by published_at after given time | [optional] 
 **published_before** | **datetime**| filter by published_at before given time | [optional] 
 **created_before** | **datetime**| filter by created_at before given time | [optional] 
 **updated_before** | **datetime**| filter by updated_at before given time | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 

### Return type

[**List[VersionWithPackage]**](VersionWithPackage.md)

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

# **lookup_package**
> List[PackageWithRegistry] lookup_package(repository_url=repository_url, purl=purl, ecosystem=ecosystem, name=name, sort=sort, order=order)

lookup a package by repository URL, purl or ecosystem+name

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.package_with_registry import PackageWithRegistry
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
    api_instance = ecosyste_ms_cli.clients.packages.PackagesApi(api_client)
    repository_url = 'repository_url_example' # str | repository URL (optional)
    purl = 'purl_example' # str | package URL (optional)
    ecosystem = 'ecosystem_example' # str | ecosystem name (optional)
    name = 'name_example' # str | package name (optional)
    sort = 'sort_example' # str | field to sort results by (optional)
    order = 'order_example' # str | direction to sort results by (optional)

    try:
        # lookup a package by repository URL, purl or ecosystem+name
        api_response = api_instance.lookup_package(repository_url=repository_url, purl=purl, ecosystem=ecosystem, name=name, sort=sort, order=order)
        print("The response of PackagesApi->lookup_package:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PackagesApi->lookup_package: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **repository_url** | **str**| repository URL | [optional] 
 **purl** | **str**| package URL | [optional] 
 **ecosystem** | **str**| ecosystem name | [optional] 
 **name** | **str**| package name | [optional] 
 **sort** | **str**| field to sort results by | [optional] 
 **order** | **str**| direction to sort results by | [optional] 

### Return type

[**List[PackageWithRegistry]**](PackageWithRegistry.md)

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

# **lookup_registry_package**
> List[PackageWithRegistry] lookup_registry_package(registry_name, repository_url=repository_url, purl=purl, ecosystem=ecosystem, name=name, sort=sort, order=order)

lookup a package within a registry by repository URL, purl or ecosystem+name

### Example


```python
import ecosyste_ms_cli.clients.packages
from ecosyste_ms_cli.clients.packages.models.package_with_registry import PackageWithRegistry
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
    api_instance = ecosyste_ms_cli.clients.packages.PackagesApi(api_client)
    registry_name = 'registry_name_example' # str | name of registry
    repository_url = 'repository_url_example' # str | repository URL (optional)
    purl = 'purl_example' # str | package URL (optional)
    ecosystem = 'ecosystem_example' # str | ecosystem name (optional)
    name = 'name_example' # str | package name (optional)
    sort = 'sort_example' # str | field to sort results by (optional)
    order = 'order_example' # str | direction to sort results by (optional)

    try:
        # lookup a package within a registry by repository URL, purl or ecosystem+name
        api_response = api_instance.lookup_registry_package(registry_name, repository_url=repository_url, purl=purl, ecosystem=ecosystem, name=name, sort=sort, order=order)
        print("The response of PackagesApi->lookup_registry_package:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PackagesApi->lookup_registry_package: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **registry_name** | **str**| name of registry | 
 **repository_url** | **str**| repository URL | [optional] 
 **purl** | **str**| package URL | [optional] 
 **ecosystem** | **str**| ecosystem name | [optional] 
 **name** | **str**| package name | [optional] 
 **sort** | **str**| field to sort results by | [optional] 
 **order** | **str**| direction to sort results by | [optional] 

### Return type

[**List[PackageWithRegistry]**](PackageWithRegistry.md)

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

