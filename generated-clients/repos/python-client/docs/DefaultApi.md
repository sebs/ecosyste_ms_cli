# ecosyste_ms_cli.clients.repos.DefaultApi

All URIs are relative to *https://repos.ecosyste.ms/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_host**](DefaultApi.md#get_host) | **GET** /hosts/{hostName} | get a host by name
[**get_host_owner**](DefaultApi.md#get_host_owner) | **GET** /hosts/{hostName}/owners/{ownerLogin} | get a owner by login
[**get_host_owner_repositories**](DefaultApi.md#get_host_owner_repositories) | **GET** /hosts/{hostName}/owners/{ownerLogin}/repositories | get a list of repositories from a owner
[**get_host_owners**](DefaultApi.md#get_host_owners) | **GET** /hosts/{hostName}/owners | get a list of owners from a host
[**get_host_repositories**](DefaultApi.md#get_host_repositories) | **GET** /hosts/{hostName}/repositories | get a list of repositories from a host
[**get_host_repository**](DefaultApi.md#get_host_repository) | **GET** /hosts/{hostName}/repositories/{repositoryName} | get a repository by name
[**get_host_repository_manifests**](DefaultApi.md#get_host_repository_manifests) | **GET** /hosts/{hostName}/repositories/{repositoryName}/manifests | get a list of manifests for a repository
[**get_host_repository_names**](DefaultApi.md#get_host_repository_names) | **GET** /hosts/{hostName}/repository_names | get a list of repository names from a host
[**get_host_repository_release**](DefaultApi.md#get_host_repository_release) | **GET** /hosts/{hostName}/repositories/{repositoryName}/releases/{release} | get a release for a repository
[**get_host_repository_releases**](DefaultApi.md#get_host_repository_releases) | **GET** /hosts/{hostName}/repositories/{repositoryName}/releases | get a list of releases for a repository
[**get_host_repository_tag**](DefaultApi.md#get_host_repository_tag) | **GET** /hosts/{hostName}/repositories/{repositoryName}/tags/{tag} | get a tag for a repository
[**get_host_repository_tag_manifests**](DefaultApi.md#get_host_repository_tag_manifests) | **GET** /hosts/{hostName}/repositories/{repositoryName}/tags/{tag}/manifests | get dependency manifests for a tag
[**get_host_repository_tags**](DefaultApi.md#get_host_repository_tags) | **GET** /hosts/{hostName}/repositories/{repositoryName}/tags | get a list of tags for a repository
[**get_registries**](DefaultApi.md#get_registries) | **GET** /hosts | list registies
[**lookup_host_owner**](DefaultApi.md#lookup_host_owner) | **GET** /hosts/{HostName}/owners/lookup | lookup owner by name or email
[**repositories_lookup**](DefaultApi.md#repositories_lookup) | **GET** /repositories/lookup | Lookup repository metadata by url or purl
[**topic**](DefaultApi.md#topic) | **GET** /topics/{topic} | Get topic
[**topics**](DefaultApi.md#topics) | **GET** /topics | Get topics
[**usage**](DefaultApi.md#usage) | **GET** /usage | Get package usage ecosystems
[**usage_ecosystem**](DefaultApi.md#usage_ecosystem) | **GET** /usage/{ecosystem} | Get package usage for an ecosystem
[**usage_package**](DefaultApi.md#usage_package) | **GET** /usage/{ecosystem}/{package} | Get package usage for a package
[**usage_package_dependencies**](DefaultApi.md#usage_package_dependencies) | **GET** /usage/{ecosystem}/{package}/dependencies | Get dependent repositories for a package


# **get_host**
> Host get_host(host_name, page=page, per_page=per_page)

get a host by name

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.host import Host
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)

    try:
        # get a host by name
        api_response = api_instance.get_host(host_name, page=page, per_page=per_page)
        print("The response of DefaultApi->get_host:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 

### Return type

[**Host**](Host.md)

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

# **get_host_owner**
> Owner get_host_owner(host_name, owner_login)

get a owner by login

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.owner import Owner
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    owner_login = 'owner_login_example' # str | login of owner

    try:
        # get a owner by login
        api_response = api_instance.get_host_owner(host_name, owner_login)
        print("The response of DefaultApi->get_host_owner:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host_owner: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **owner_login** | **str**| login of owner | 

### Return type

[**Owner**](Owner.md)

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

# **get_host_owner_repositories**
> List[Repository] get_host_owner_repositories(host_name, owner_login, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, fork=fork, archived=archived, sort=sort, order=order)

get a list of repositories from a owner

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.repository import Repository
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    owner_login = 'owner_login_example' # str | login of owner
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at after given time (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at after given time (optional)
    fork = True # bool | filter by fork (optional)
    archived = True # bool | filter by archived (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # get a list of repositories from a owner
        api_response = api_instance.get_host_owner_repositories(host_name, owner_login, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, fork=fork, archived=archived, sort=sort, order=order)
        print("The response of DefaultApi->get_host_owner_repositories:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host_owner_repositories: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **owner_login** | **str**| login of owner | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **created_after** | **datetime**| filter by created_at after given time | [optional] 
 **updated_after** | **datetime**| filter by updated_at after given time | [optional] 
 **fork** | **bool**| filter by fork | [optional] 
 **archived** | **bool**| filter by archived | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 

### Return type

[**List[Repository]**](Repository.md)

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

# **get_host_owners**
> List[Owner] get_host_owners(host_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, sort=sort, order=order)

get a list of owners from a host

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.owner import Owner
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at after given time (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at after given time (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # get a list of owners from a host
        api_response = api_instance.get_host_owners(host_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, sort=sort, order=order)
        print("The response of DefaultApi->get_host_owners:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host_owners: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **created_after** | **datetime**| filter by created_at after given time | [optional] 
 **updated_after** | **datetime**| filter by updated_at after given time | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 

### Return type

[**List[Owner]**](Owner.md)

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

# **get_host_repositories**
> List[Repository] get_host_repositories(host_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, fork=fork, archived=archived, sort=sort, order=order)

get a list of repositories from a host

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.repository import Repository
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at after given time (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at after given time (optional)
    fork = True # bool | filter by fork (optional)
    archived = True # bool | filter by archived (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # get a list of repositories from a host
        api_response = api_instance.get_host_repositories(host_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, fork=fork, archived=archived, sort=sort, order=order)
        print("The response of DefaultApi->get_host_repositories:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host_repositories: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **created_after** | **datetime**| filter by created_at after given time | [optional] 
 **updated_after** | **datetime**| filter by updated_at after given time | [optional] 
 **fork** | **bool**| filter by fork | [optional] 
 **archived** | **bool**| filter by archived | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 

### Return type

[**List[Repository]**](Repository.md)

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

# **get_host_repository**
> Repository get_host_repository(host_name, repository_name)

get a repository by name

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.repository import Repository
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    repository_name = 'repository_name_example' # str | name of repository

    try:
        # get a repository by name
        api_response = api_instance.get_host_repository(host_name, repository_name)
        print("The response of DefaultApi->get_host_repository:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host_repository: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **repository_name** | **str**| name of repository | 

### Return type

[**Repository**](Repository.md)

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

# **get_host_repository_manifests**
> List[Manifest] get_host_repository_manifests(host_name, repository_name, page=page, per_page=per_page)

get a list of manifests for a repository

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.manifest import Manifest
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    repository_name = 'repository_name_example' # str | name of repository
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)

    try:
        # get a list of manifests for a repository
        api_response = api_instance.get_host_repository_manifests(host_name, repository_name, page=page, per_page=per_page)
        print("The response of DefaultApi->get_host_repository_manifests:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host_repository_manifests: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **repository_name** | **str**| name of repository | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 

### Return type

[**List[Manifest]**](Manifest.md)

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

# **get_host_repository_names**
> List[str] get_host_repository_names(host_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, fork=fork, archived=archived, sort=sort, order=order)

get a list of repository names from a host

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at after given time (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at after given time (optional)
    fork = True # bool | filter by fork (optional)
    archived = True # bool | filter by archived (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # get a list of repository names from a host
        api_response = api_instance.get_host_repository_names(host_name, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, fork=fork, archived=archived, sort=sort, order=order)
        print("The response of DefaultApi->get_host_repository_names:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host_repository_names: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **created_after** | **datetime**| filter by created_at after given time | [optional] 
 **updated_after** | **datetime**| filter by updated_at after given time | [optional] 
 **fork** | **bool**| filter by fork | [optional] 
 **archived** | **bool**| filter by archived | [optional] 
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

# **get_host_repository_release**
> Release get_host_repository_release(host_name, repository_name, release)

get a release for a repository

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.release import Release
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    repository_name = 'repository_name_example' # str | name of repository
    release = 'release_example' # str | tag_name of release

    try:
        # get a release for a repository
        api_response = api_instance.get_host_repository_release(host_name, repository_name, release)
        print("The response of DefaultApi->get_host_repository_release:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host_repository_release: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **repository_name** | **str**| name of repository | 
 **release** | **str**| tag_name of release | 

### Return type

[**Release**](Release.md)

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

# **get_host_repository_releases**
> List[Tag] get_host_repository_releases(host_name, repository_name, page=page, per_page=per_page, sort=sort, order=order)

get a list of releases for a repository

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.tag import Tag
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    repository_name = 'repository_name_example' # str | name of repository
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # get a list of releases for a repository
        api_response = api_instance.get_host_repository_releases(host_name, repository_name, page=page, per_page=per_page, sort=sort, order=order)
        print("The response of DefaultApi->get_host_repository_releases:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host_repository_releases: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **repository_name** | **str**| name of repository | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 

### Return type

[**List[Tag]**](Tag.md)

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

# **get_host_repository_tag**
> Tag get_host_repository_tag(host_name, repository_name, tag)

get a tag for a repository

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.tag import Tag
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    repository_name = 'repository_name_example' # str | name of repository
    tag = 'tag_example' # str | name of tag

    try:
        # get a tag for a repository
        api_response = api_instance.get_host_repository_tag(host_name, repository_name, tag)
        print("The response of DefaultApi->get_host_repository_tag:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host_repository_tag: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **repository_name** | **str**| name of repository | 
 **tag** | **str**| name of tag | 

### Return type

[**Tag**](Tag.md)

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

# **get_host_repository_tag_manifests**
> List[Manifest] get_host_repository_tag_manifests(host_name, repository_name, tag)

get dependency manifests for a tag

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.manifest import Manifest
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    repository_name = 'repository_name_example' # str | name of repository
    tag = 'tag_example' # str | name of tag

    try:
        # get dependency manifests for a tag
        api_response = api_instance.get_host_repository_tag_manifests(host_name, repository_name, tag)
        print("The response of DefaultApi->get_host_repository_tag_manifests:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host_repository_tag_manifests: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **repository_name** | **str**| name of repository | 
 **tag** | **str**| name of tag | 

### Return type

[**List[Manifest]**](Manifest.md)

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

# **get_host_repository_tags**
> List[Tag] get_host_repository_tags(host_name, repository_name, page=page, per_page=per_page, sort=sort, order=order)

get a list of tags for a repository

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.tag import Tag
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    repository_name = 'repository_name_example' # str | name of repository
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # get a list of tags for a repository
        api_response = api_instance.get_host_repository_tags(host_name, repository_name, page=page, per_page=per_page, sort=sort, order=order)
        print("The response of DefaultApi->get_host_repository_tags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_host_repository_tags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **repository_name** | **str**| name of repository | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 

### Return type

[**List[Tag]**](Tag.md)

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

# **get_registries**
> List[Host] get_registries(page=page, per_page=per_page)

list registies

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.host import Host
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)

    try:
        # list registies
        api_response = api_instance.get_registries(page=page, per_page=per_page)
        print("The response of DefaultApi->get_registries:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_registries: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 

### Return type

[**List[Host]**](Host.md)

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

# **lookup_host_owner**
> List[Owner] lookup_host_owner(host_name, name=name, email=email)

lookup owner by name or email

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.owner import Owner
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    host_name = 'host_name_example' # str | name of host
    name = 'name_example' # str | name of owner (optional)
    email = 'email_example' # str | email of owner (optional)

    try:
        # lookup owner by name or email
        api_response = api_instance.lookup_host_owner(host_name, name=name, email=email)
        print("The response of DefaultApi->lookup_host_owner:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->lookup_host_owner: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **host_name** | **str**| name of host | 
 **name** | **str**| name of owner | [optional] 
 **email** | **str**| email of owner | [optional] 

### Return type

[**List[Owner]**](Owner.md)

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

# **repositories_lookup**
> Repository repositories_lookup(url=url, purl=purl)

Lookup repository metadata by url or purl

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.repository import Repository
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    url = 'url_example' # str | The URL of the repository to lookup (optional)
    purl = 'purl_example' # str | package URL (optional)

    try:
        # Lookup repository metadata by url or purl
        api_response = api_instance.repositories_lookup(url=url, purl=purl)
        print("The response of DefaultApi->repositories_lookup:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->repositories_lookup: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| The URL of the repository to lookup | [optional] 
 **purl** | **str**| package URL | [optional] 

### Return type

[**Repository**](Repository.md)

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

# **topic**
> TopicWithRepositories topic(topic, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, fork=fork, archived=archived, sort=sort, order=order)

Get topic

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.topic_with_repositories import TopicWithRepositories
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    topic = 'topic_example' # str | The topic to get
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)
    created_after = '2013-10-20T19:20:30+01:00' # datetime | filter by created_at after given time (optional)
    updated_after = '2013-10-20T19:20:30+01:00' # datetime | filter by updated_at after given time (optional)
    fork = True # bool | filter by fork (optional)
    archived = True # bool | filter by archived (optional)
    sort = 'sort_example' # str | field to order results by (optional)
    order = 'order_example' # str | direction to order results by (optional)

    try:
        # Get topic
        api_response = api_instance.topic(topic, page=page, per_page=per_page, created_after=created_after, updated_after=updated_after, fork=fork, archived=archived, sort=sort, order=order)
        print("The response of DefaultApi->topic:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->topic: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **topic** | **str**| The topic to get | 
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 
 **created_after** | **datetime**| filter by created_at after given time | [optional] 
 **updated_after** | **datetime**| filter by updated_at after given time | [optional] 
 **fork** | **bool**| filter by fork | [optional] 
 **archived** | **bool**| filter by archived | [optional] 
 **sort** | **str**| field to order results by | [optional] 
 **order** | **str**| direction to order results by | [optional] 

### Return type

[**TopicWithRepositories**](TopicWithRepositories.md)

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

# **topics**
> List[Topic] topics(page=page, per_page=per_page)

Get topics

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.topic import Topic
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    page = 56 # int | pagination page number (optional)
    per_page = 56 # int | Number of records to return (optional)

    try:
        # Get topics
        api_response = api_instance.topics(page=page, per_page=per_page)
        print("The response of DefaultApi->topics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->topics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| pagination page number | [optional] 
 **per_page** | **int**| Number of records to return | [optional] 

### Return type

[**List[Topic]**](Topic.md)

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

# **usage**
> List[Ecosystem] usage()

Get package usage ecosystems

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.ecosystem import Ecosystem
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)

    try:
        # Get package usage ecosystems
        api_response = api_instance.usage()
        print("The response of DefaultApi->usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->usage: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Ecosystem]**](Ecosystem.md)

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

# **usage_ecosystem**
> List[PackageUsage] usage_ecosystem(ecosystem)

Get package usage for an ecosystem

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.package_usage import PackageUsage
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    ecosystem = 'ecosystem_example' # str | The ecosystem to get usage for

    try:
        # Get package usage for an ecosystem
        api_response = api_instance.usage_ecosystem(ecosystem)
        print("The response of DefaultApi->usage_ecosystem:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->usage_ecosystem: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ecosystem** | **str**| The ecosystem to get usage for | 

### Return type

[**List[PackageUsage]**](PackageUsage.md)

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

# **usage_package**
> PackageUsage usage_package(ecosystem, package)

Get package usage for a package

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.package_usage import PackageUsage
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    ecosystem = 'ecosystem_example' # str | The ecosystem to get usage for
    package = 'package_example' # str | The package to get usage for

    try:
        # Get package usage for a package
        api_response = api_instance.usage_package(ecosystem, package)
        print("The response of DefaultApi->usage_package:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->usage_package: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ecosystem** | **str**| The ecosystem to get usage for | 
 **package** | **str**| The package to get usage for | 

### Return type

[**PackageUsage**](PackageUsage.md)

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

# **usage_package_dependencies**
> DependencyWithRepository usage_package_dependencies(ecosystem, package)

Get dependent repositories for a package

### Example


```python
import ecosyste_ms_cli.clients.repos
from ecosyste_ms_cli.clients.repos.models.dependency_with_repository import DependencyWithRepository
from ecosyste_ms_cli.clients.repos.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://repos.ecosyste.ms/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = ecosyste_ms_cli.clients.repos.Configuration(
    host = "https://repos.ecosyste.ms/api/v1"
)


# Enter a context with an instance of the API client
with ecosyste_ms_cli.clients.repos.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = ecosyste_ms_cli.clients.repos.DefaultApi(api_client)
    ecosystem = 'ecosystem_example' # str | The ecosystem to get usage for
    package = 'package_example' # str | The package to get usage for

    try:
        # Get dependent repositories for a package
        api_response = api_instance.usage_package_dependencies(ecosystem, package)
        print("The response of DefaultApi->usage_package_dependencies:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->usage_package_dependencies: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **ecosystem** | **str**| The ecosystem to get usage for | 
 **package** | **str**| The package to get usage for | 

### Return type

[**DependencyWithRepository**](DependencyWithRepository.md)

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

