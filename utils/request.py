import json
import requests
import pdb

def pre_process_request(url, method="GET", headers=None, cookies=None, params=None, json_data=None):
  """
  This function pre-processes a request by assembling the necessary components.

  Args:
      url: The URL for the request.
      method: The HTTP method (default: "GET"). Can be "GET", "POST", etc.
      headers: Optional dictionary of request headers.
      cookies: Optional dictionary of request cookies.
      params: Optional dictionary (GET params), string (URL-encoded data), or JSON string (JSON data) for the request.
      json_data: Optional dictionary for JSON data to be sent in the request body.

  Returns:
      A dictionary containing the pre-processed request data (url, method, headers, cookies, data)
  """

  # Prepare request data
  request_data = {
      "url": url,
      "method": method.upper(),  # Ensure uppercase method (standard)
      "headers": headers or {},  # Use empty dictionary if headers is None
      "cookies": cookies or {},  # Use empty dictionary if cookies is None
  }

  # Handle params
  if params:
    if isinstance(params, dict):
      request_data["params"] = params
    elif isinstance(params, str):
      request_data["data"] = params  # Assuming URL-encoded format
    else:
      try:
        request_data["json"] = json.loads(params)  # Assuming JSON string
      except json.JSONDecodeError:
        pass  # Handle potential invalid JSON

  # Handle JSON data (overrides any params data)
  if json_data:
    request_data["json"] = json_data

  return request_data


def process_request(request_data):
  """
  This function sends a request based on the provided data and returns the response.

  Args:
      request_data: A dictionary containing pre-processed request information (url, method, headers, cookies, optional data/json).

  Returns:
      A requests.Response object containing the response from the server, or None on error.
  """

  try:
    response = requests.request(**request_data)
    response.raise_for_status()  # Raise an exception for non-2xx status codes

    # Handle successful response (optional additional processing here)
    return response

  except requests.exceptions.RequestException as e:
    print(f"Error making request: {e}")
    return None  # Or return an error object or handle differently in your scraper


def post_process_data(data, headers=None, cookies=None, params=None):
  """
  This function performs general post-processing on the provided data after making a request.

  Args:
      data: The data to be processed (can be a dictionary, list, etc.)
      headers: Optional dictionary of request headers.
      cookies: Optional dictionary of request cookies.
      params: Optional dictionary (GET params), string (URL-encoded data), or JSON string (JSON data) for the request.

  Returns:
      The processed data (may be the same or modified data structure)
  """

  # Add your specific post-processing logic here

  # Example: Formatting or cleaning data
  if isinstance(data, dict):
    # Modify values or structure within the dictionary
    data["key1"] = data["key1"].upper()  # Example modification

  # Include information about the request:
  if headers:
    data["headers"] = headers
  if cookies:
    data["cookies"] = cookies
  if params:
    if isinstance(params, dict):
      data["params"] = params
    elif isinstance(params, str):
      data["params"] = params  # Assuming URL-encoded format
    else:
      try:
        data["params"] = json.loads(params)  # Assuming JSON string
      except json.JSONDecodeError:
        pass  # Handle potential invalid JSON

  return data

def save_http_response(response, filename):
  """
  Downloads an HTTP response and saves it to a file, including headers, cookies, and content.

  Args:
      url: The URL of the resource to download.
      filename: The filename to save the response to.
  """
  try:
    response.raise_for_status()  # Raise an exception for non-2xx status codes

    # Prepare content string with headers and cookies
    content = f"--- HTTP Response ---\n"
    content += f"Status Code: {response.status_code}\n"
    content += f"Reason: {response.reason}\n"
    for key, value in response.headers.items():
      content += f"{key}: {value}\n"
    if response.cookies:
      content += "\n--- Cookies ---\n"
      for key, value in response.cookies.items():
        content += f"{key}: {value}\n"
    content += "\n--- Response Body ---\n"
    content += response.text

    # Write content to file
    with open(filename, "wb") as f:
      f.write(content.encode("utf-8"))  # Encode content as UTF-8

    print(f"HTTP response saved to: {filename}")

  except requests.exceptions.RequestException as e:
    print(f"Error downloading response: {e}")