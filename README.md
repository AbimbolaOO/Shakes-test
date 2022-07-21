# ABIMBOLA OLAYEMI'S attempt at Shake's currency converter API test

## How to run the project

### Requirements

- An installation of docker on your laptop.
- A command line terminal that can run a simple bash script.

### Instruction to run the API

- Download the code on your laptop.
- Open your terminal in the newly downloaded folder.
- Go to [Fastforex](https://fastforex.readme.io/) and create an account to get your own apikey.
- Open the `run.sh` file paste your newly obtained API as described below

    ```{bash}
    export FAST_FOREX_API_KEY=<YOUR_FAST_FOREX_API_KEY>'
    ```

- Copy and paste the code below into your terminal then click the enter button

    ```{bash}
    bash run.sh
    ```

- Provide the terminal with your password. This is usually your laptop password.

- Once you're done testing the endpoint hit the Ctrl^D on your terminal, and the container is automatically removed and stopped.

## Project Description

This is a currency converter API and it provides the customer with 4 endpoints listed below

- /createaccount `POST`
- /gettoken `POST`
- /v1/currency/all `GET`
- /v1/convert `GET`

The `/createaccount` is the first endpoint the user is expected to first visit. In this endpoint, the user creates an account by making a post request to the `/createaccount` endpoint. To do this the user is to provide a username and password. **Note** it is important for users to remember their username and password because this would be used later to create a `JWT`  that would be needed to authenticate the user when accessing `/v1/currency/all` and `/v1/convert` endpoints.

```{python}
import requests

url = "http://localhost:8000/createaccount"

payload = {"username": <username>, "password": <password>}

response = requests.request("POST", url, data=payload)

print(response.text)
```

The `/gettoken` is the second endpoint the user is expected to visit. Here the user provides the username and password they created an account with earlier. The user-provided credentials if valid would return a `JWT` token to the user which can then be used to access `/v1/currency/all` and `/v1/convert`  endpoints.

```{python}
import requests

url = "http://localhost:8000/gettoken"

payload = {"username": <username>, "password": <password>}

response = requests.request("POST", url, data=payload)

print(response.text)

```

The `/v1/currency/all` endpoint provides the user with a list of all supported currencies when visited. The user is expected to provide the `JWT`. If the token is valid the user gets a list of supported currencies back from the endpoint. A sample of how to achieve this is given below.

```{python}
import requests

url = "http://localhost:8000/v1/currency/all/"

headers = {
    "Authorization": "Bearer <YOUR BEARER TOKEN GOES IN HERE>"
}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

The `/v1/convert` when visited accepts  query strings, 3 of which are optional. The list of supported query strings is below.

- base_currency `REQUIRED` currency you are converting from.
- target_currency `REQUIRED` currency you are converting to.
- amount `REQUIRED` the amount of base currency you are converting.
- date `OPTIONAL` this makes use of the exchange rate at that time.

**NOTE:** The date you provide must be of this specific format `yyyy-mm-dd`
**NOTE:** If you are using a free account from Fastforex to test you can not insert a date that is earlier than 14 days from the date you are performing the test on this API

If date isn't provided to do the conversion use the code below

```{bash}
import requests

base_currency=CAD
target_currency=AED
amount=1000
date=2022-07-13

url = f"http://localhost:8000/v1/convert?base_currency={base_currency}&target_currency={target_currency}&amount={amount}&date={2022-07-13}"

headers = {
    "Authorization": "Bearer <YOUR BEARER TOKEN GOES IN HERE>"
}

response = requests.request("GET", url, headers=headers)

print(response.text)

```

If the optional date is used to make the conversion use the code below

```{bash}
import requests

base_currency=CAD
target_currency=AED
amount=1000

url = f"http://localhost:8000/v1/convert?base_currency={base_currency}&target_currency={target_currency}&amount={amount}"

headers = {
    "Authorization": "Bearer <YOUR BEARER TOKEN GOES IN HERE>"
}

response = requests.request("GET", url, headers=headers)

print(response.text)

```

**Note** In the run.sh file the `ACCESS_TOKEN_EXPIRE_MINUTES` is set to 30 minute you can increase it if you want the `JWT` to last longer.

**Note** For more info about the API please visit the `http://localhost:8000/docs` while the API is running in the background.
