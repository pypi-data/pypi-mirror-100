# Getting Started with ClickSend API

## Getting Started

### Install the Package

The package is compatible with Python versions `2 >=2.7.9` and `3 >=3.4`.
Install the package from PyPi using the following pip command:

```python
pip install apimaticclickSendAPI==1.0.0
```

You can also view the package at:
https://pypi.python.org/pypi/apimaticclickSendAPI

### Initialize the API Client

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| `username` | `string` | Username<br>*Default*: `'maryam.adnan@apimatic.io'` |
| `password` | `string` | Password<br>*Default*: `'0DD7D153-09B4-05CC-A443-F0BF5B1C5DCD'` |
| `timeout` | `float` | The value to use for connection timeout. <br> **Default: 60** |
| `max_retries` | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 3** |
| `backoff_factor` | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 0** |

The API client can be initialized as follows:

```python
from clicksendapi.clicksendapi_client import ClicksendapiClient
from clicksendapi.configuration import Environment

client = ClicksendapiClient(
    username='maryam.adnan@apimatic.io',
    password='0DD7D153-09B4-05CC-A443-F0BF5B1C5DCD',
    environment = ,)
```

### Authorization

This API uses `Basic Authentication`.

## Client Class Documentation

### ClickSend API Client

The gateway for the SDK. This class acts as a factory for the Controllers and also holds the configuration of the SDK.

### Controllers

| Name | Description |
|  --- | --- |
| account | Gets AccountController |
| contact | Gets ContactController |

## API Reference

### List of APIs

* [Account](#account)
* [Contact](#contact)

### Account

#### Overview

##### Get instance

An instance of the `AccountController` class can be accessed from the API Client.

```
account_controller = client.account
```

#### Create Account

:information_source: **Note** This endpoint does not require authentication.

```python
def create_account(self,
                  account_info)
```

##### Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `account_info` | [`AccountInfo`](#account-info) | Body, Required | account information properties |

##### Response Type

`mixed`

##### Example Usage

```python
account_info = AccountInfo()
account_info.username = 'username4'
account_info.password = 'password8'
account_info.user_phone = 'user_phone2'
account_info.user_email = 'user_email8'
account_info.user_first_name = 'user_first_name0'
account_info.user_last_name = 'user_last_name6'
account_info.account_name = 'account_name2'
account_info.country = 'country8'

result = account_controller.create_account(account_info)
```

#### View Account Details

```python
def view_account_details(self)
```

##### Response Type

`mixed`

##### Example Usage

```python
result = account_controller.view_account_details()
```

#### View Account Usage

```python
def view_account_usage(self,
                      year,
                      month)
```

##### Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `year` | `string` | Template, Required | account usage year |
| `month` | `string` | Template, Required | account usage month |

##### Response Type

`mixed`

##### Example Usage

```python
year = 'year8'
month = 'month0'

result = account_controller.view_account_usage(year, month)
```

#### Send Account Verification

```python
def send_account_verification(self,
                             account_verification_info)
```

##### Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `account_verification_info` | [`AccountVerificationInfo`](#account-verification-info) | Body, Required | - |

##### Response Type

`mixed`

##### Example Usage

```python
account_verification_info = AccountVerificationInfo()
account_verification_info.country = 'country4'
account_verification_info.user_phone = 'user_phone8'
account_verification_info.mtype = 'type0'

result = account_controller.send_account_verification(account_verification_info)
```

### Contact

#### Overview

##### Get instance

An instance of the `ContactController` class can be accessed from the API Client.

```
contact_controller = client.contact
```

#### View Contact List

```python
def view_contact_list(self,
                     list_id,
                     page=None,
                     limit=None,
                     updated_after=None)
```

##### Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `list_id` | `string` | Template, Required | Contact list ID |
| `page` | `int` | Query, Optional | page number |
| `limit` | `string` | Query, Optional | Number of records per page |
| `updated_after` | `int` | Query, Optional | Get all contacts updated after a given timestamp |

##### Response Type

`mixed`

##### Example Usage

```python
list_id = 'list_id2'

result = contact_controller.view_contact_list(list_id)
```

#### Create New Contact

```python
def create_new_contact(self,
                      list_id,
                      contact_info,
                      page=None,
                      limit=None)
```

##### Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `list_id` | `string` | Template, Required | List id |
| `contact_info` | [`NewContactInfo`](#new-contact-info) | Body, Required | info to create new contact |
| `page` | `int` | Query, Optional | page number |
| `limit` | `int` | Query, Optional | Number of records per page |

##### Response Type

`mixed`

##### Example Usage

```python
list_id = 'list_id2'
contact_info = NewContactInfo()
contact_info.phone_number = 'phone_number4'
contact_info.email = 'email8'
contact_info.fax_number = 'fax_number6'
contact_info.first_name = 'first_name8'
contact_info.address_line_1 = 'address_line_12'
contact_info.address_line_2 = 'address_line_28'
contact_info.address_city = 'address_city8'
contact_info.address_state = 'address_state0'
contact_info.address_postal_code = 'address_postal_code2'
contact_info.address_country = 'address_country0'
contact_info.organization_name = 'organization_name0'
contact_info.custom_1 = 'custom_16'
contact_info.custom_2 = 'custom_28'
contact_info.custom_3 = 'custom_36'
contact_info.custom_4 = 'custom_46'
contact_info.last_name = 'last_name6'

result = contact_controller.create_new_contact(list_id, contact_info)
```

#### Delete Contact

```python
def delete_contact(self,
                  list_id,
                  contact_id)
```

##### Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `list_id` | `int` | Template, Required | List ID |
| `contact_id` | `int` | Template, Required | Contact ID |

##### Response Type

`void`

##### Example Usage

```python
list_id = 102
contact_id = 38

result = contact_controller.delete_contact(list_id, contact_id)
```

#### Remove Opted Out Contacts

```python
def remove_opted_out_contacts(self,
                             list_id,
                             opt_out_list_id)
```

##### Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `list_id` | `int` | Template, Required | Your list id |
| `opt_out_list_id` | `int` | Template, Required | Your opt out list id |

##### Response Type

`mixed`

##### Example Usage

```python
list_id = 102
opt_out_list_id = 84

result = contact_controller.remove_opted_out_contacts(list_id, opt_out_list_id)
```

## Model Reference

### Structures

* [Account Info](#account-info)
* [Account Verification Info](#account-verification-info)
* [New Contact Info](#new-contact-info)

#### Account Info

info related to account creation

##### Class Name

`AccountInfo`

##### Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `username` | `string` | Required | Your username |
| `password` | `string` | Required | Your password |
| `user_phone` | `string` | Required | Your phone number in E.164 format. |
| `user_email` | `string` | Required | Your email |
| `user_first_name` | `string` | Required | Your first name |
| `user_last_name` | `string` | Required | Your last name |
| `account_name` | `string` | Required | Your delivery to value. |
| `country` | `string` | Required | Your country |

##### Example (as JSON)

```json
{
  "username": "username0",
  "password": "password4",
  "user_phone": "user_phone2",
  "user_email": "user_email6",
  "user_first_name": "user_first_name6",
  "user_last_name": "user_last_name2",
  "account_name": "account_name2",
  "country": "country4"
}
```

#### Account Verification Info

##### Class Name

`AccountVerificationInfo`

##### Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `country` | `string` | Required | Two-letter country code (ISO3166) |
| `user_phone` | `string` | Required | User's phone number |
| `mtype` | `string` | Required | Type of verification |

##### Example (as JSON)

```json
{
  "country": "country4",
  "user_phone": "user_phone2",
  "type": "type0"
}
```

#### New Contact Info

info to create new contact

##### Class Name

`NewContactInfo`

##### Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `phone_number` | `string` | Required | Your phone number in E.164 format. Must be provided if no fax number or email. |
| `email` | `string` | Required | Your email. Must be provided if no phone number or fax number. |
| `fax_number` | `string` | Required | Your fax number. Must be provided if no phone number or email. |
| `first_name` | `string` | Required | Your first name. |
| `address_line_1` | `string` | Required | Your street address |
| `address_line_2` | `string` | Required | none |
| `address_city` | `string` | Required | Your nearest city |
| `address_state` | `string` | Required | Your current state |
| `address_postal_code` | `string` | Required | Your current postcode |
| `address_country` | `string` | Required | Your current country |
| `organization_name` | `string` | Required | Your organisation name |
| `custom_1` | `string` | Required | none |
| `custom_2` | `string` | Required | none |
| `custom_3` | `string` | Required | none |
| `custom_4` | `string` | Required | none |
| `last_name` | `string` | Required | Your last name |

##### Example (as JSON)

```json
{
  "phone_number": "phone_number2",
  "email": "email6",
  "fax_number": "fax_number4",
  "first_name": "first_name0",
  "address_line_1": "address_line_10",
  "address_line_2": "address_line_20",
  "address_city": "address_city0",
  "address_state": "address_state2",
  "address_postal_code": "address_postal_code0",
  "address_country": "address_country8",
  "organization_name": "organization_name2",
  "custom_1": "custom_14",
  "custom_2": "custom_20",
  "custom_3": "custom_34",
  "custom_4": "custom_48",
  "last_name": "last_name8"
}
```

## Utility Classes Documentation

### ApiHelper

A utility class for processing API Calls. Also contains classes for supporting standard datetime formats.

#### Methods

| Name | Description |
|  --- | --- |
| json_deserialize | Deserializes a JSON string to a Python dictionary. |

#### Classes

| Name | Description |
|  --- | --- |
| HttpDateTime | A wrapper for datetime to support HTTP date format. |
| UnixDateTime | A wrapper for datetime to support Unix date format. |
| RFC3339DateTime | A wrapper for datetime to support RFC3339 format. |

## Common Code Documentation

### HttpResponse

Http response received.

#### Parameters

| Name | Type | Description |
|  --- | --- | --- |
| status_code | int | The status code returned by the server. |
| reason_phrase | str | The reason phrase returned by the server. |
| headers | dict | Response headers. |
| text | str | Response body. |
| request | HttpRequest | The request that resulted in this response. |

### HttpRequest

Represents a single Http Request.

#### Parameters

| Name | Type | Tag | Description |
|  --- | --- | --- | --- |
| http_method | HttpMethodEnum |  | The HTTP method of the request. |
| query_url | str |  | The endpoint URL for the API request. |
| headers | dict | optional | Request headers. |
| query_parameters | dict | optional | Query parameters to add in the URL. |
| parameters | dict &#124; str | optional | Request body, either as a serialized string or else a list of parameters to form encode. |
| files | dict | optional | Files to be sent with the request. |

