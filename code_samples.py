# Vtion-Toluna IP-ES Integration Code Samples and Guidelines

## Overview
This document provides Python code samples and guidelines for integrating Vtion with Toluna's IP-ES API. These samples are based on the recommended IP-ES approach and align with the previously documented flows, data mapping, and implementation plan.

## Prerequisites
- Python 3.x installed
- `requests` library installed (`pip install requests`)
- Toluna API credentials (API_AUTH_KEY)
- Toluna PanelGUID
- Toluna IP-ES Base URL

## Configuration
```python
import requests
import json
import logging

# --- Configuration ---
TOLUNA_BASE_URL = "https://{IP_ES_URL}"  # Replace with actual Toluna IP-ES URL
API_AUTH_KEY = "YOUR_TOLUNA_API_AUTH_KEY"  # Replace with your API key
PANEL_GUID = "YOUR_TOLUNA_PANEL_GUID"  # Replace with your Panel GUID

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Helper Function for API Requests ---
def make_toluna_request(method, endpoint, params=None, data=None):
    """Helper function to make requests to the Toluna API."""
    url = f"{TOLUNA_BASE_URL}{endpoint}"
    headers = {
        "API_AUTH_KEY": API_AUTH_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=params, timeout=30)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, params=params, json=data, timeout=30)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, params=params, json=data, timeout=30)
        else:
            logging.error(f"Unsupported HTTP method: {method}")
            return None

        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        
        # Handle potential empty responses for certain success codes (e.g., 204 No Content)
        if response.status_code == 204:
            return {"status": "success", "status_code": 204}
            
        return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            logging.error(f"Response status: {e.response.status_code}")
            logging.error(f"Response body: {e.response.text}")
            # Return error details if available
            try:
                return {"error": e.response.json(), "status_code": e.response.status_code}
            except json.JSONDecodeError:
                return {"error": e.response.text, "status_code": e.response.status_code}
        return {"error": str(e), "status_code": None}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON response: {e}")
        logging.error(f"Response text: {response.text}")
        return {"error": "Invalid JSON response", "status_code": response.status_code}

```

## 1. Member Registration/Update

This function registers a new member or updates an existing member's profile data in Toluna.

```python
def register_or_update_member(member_data):
    """Registers a new member or updates an existing one in Toluna.

    Args:
        member_data (dict): Dictionary containing member profile data.
                            Must include 'MemberCode'.
                            Required fields: 'BirthDate', 'Gender'.
                            Recommended: 'PostalCode', 'CountryID', etc.
                            Example:
                            {
                                "MemberCode": "vtion_user_123",
                                "BirthDate": "1990-05-15",
                                "Gender": 1, # 1=Male, 2=Female, 3=Other
                                "PostalCode": "90210",
                                "CountryID": 1, # Map Vtion country to Toluna ID
                                "Attributes": [
                                    {"QuestionID": 101, "AnswerID": 5}, # Example: Education Level
                                    {"QuestionID": 102, "AnswerID": 2}  # Example: Employment Status
                                ]
                            }

    Returns:
        dict: API response from Toluna or error dictionary.
    """
    if not member_data or 'MemberCode' not in member_data:
        logging.error("MemberCode is required for registration/update.")
        return {"error": "MemberCode missing", "status_code": 400}

    # Use the Member Management v2 API (Dynamic)
    # POST creates or updates (upsert behavior)
    endpoint = f"/IntegratedPanelService/api/v2/Respondent/{PANEL_GUID}/{member_data['MemberCode']}"
    
    # Structure the payload according to Toluna's v2 API spec
    payload = {
        "BirthDate": member_data.get("BirthDate"),
        "Gender": member_data.get("Gender"),
        "PostalCode": member_data.get("PostalCode"),
        "CountryID": member_data.get("CountryID"),
        "Attributes": member_data.get("Attributes", [])
        # Add other relevant fields based on mapping
    }
    
    # Filter out None values before sending
    payload = {k: v for k, v in payload.items() if v is not None}

    logging.info(f"Registering/Updating member: {member_data['MemberCode']}")
    response = make_toluna_request('POST', endpoint, data=payload)
    
    if response and response.get("status_code") == 204: # Successful update/creation
        logging.info(f"Successfully registered/updated member: {member_data['MemberCode']}")
        return {"status": "success", "member_code": member_data['MemberCode']}
    elif response and "error" in response:
        logging.error(f"Failed to register/update member {member_data['MemberCode']}: {response['error']}")
        return response
    else:
        logging.error(f"Unexpected response for member {member_data['MemberCode']}: {response}")
        return {"error": "Unexpected API response", "details": response}

# --- Example Usage ---
# new_member = {
#     "MemberCode": "vtion_user_456",
#     "BirthDate": "1985-10-20",
#     "Gender": 2,
#     "PostalCode": "10001",
#     "CountryID": 1,
#     "Attributes": [
#         {"QuestionID": 101, "AnswerID": 6}, # Master's Degree
#         {"QuestionID": 102, "AnswerID": 1}  # Employed Full-time
#     ]
# }
# result = register_or_update_member(new_member)
# print(result)
```

## 2. Get Available Quotas

This function retrieves the list of currently open survey quotas from Toluna.

```python
def get_available_quotas(include_routables=True):
    """Retrieves the list of open survey quotas from Toluna.

    Args:
        include_routables (bool): Whether to include routable questions. Defaults to True.

    Returns:
        dict: API response containing the list of surveys and quotas, or error dictionary.
    """
    endpoint = f"/IPExternalSamplingService/ExternalSample/{PANEL_GUID}/Quotas"
    params = {"includeRoutables": str(include_routables).lower()}
    
    logging.info("Fetching available quotas...")
    response = make_toluna_request('GET', endpoint, params=params)
    
    if response and "Surveys" in response: # Check for expected key in successful response
        logging.info(f"Successfully retrieved {len(response.get('Surveys', []))} surveys with open quotas.")
        return response
    elif response and "error" in response:
        logging.error(f"Failed to retrieve quotas: {response['error']}")
        return response
    else:
        logging.error(f"Unexpected response when retrieving quotas: {response}")
        return {"error": "Unexpected API response", "details": response}

# --- Example Usage ---
# quotas_response = get_available_quotas()
# if quotas_response and "Surveys" in quotas_response:
#     # Process the quotas_response['Surveys'] list
#     # Implement matching logic here based on user profile and quota requirements
#     print(f"Found {len(quotas_response['Surveys'])} surveys.")
# else:
#     print("Failed to get quotas or no surveys available.")
```

## 3. Generate Survey Invite

This function generates a unique survey invitation link for a specific member and quota.

```python
def generate_survey_invite(member_code, quota_id):
    """Generates a survey invite link for a member and quota.

    Args:
        member_code (str): The unique identifier for the Vtion user.
        quota_id (int): The ID of the Toluna quota the user is matched to.

    Returns:
        dict: API response containing the survey URL and details, or error dictionary.
    """
    if not member_code or not quota_id:
        logging.error("MemberCode and QuotaID are required to generate an invite.")
        return {"error": "MemberCode or QuotaID missing", "status_code": 400}
        
    endpoint = f"/IPExternalSamplingService/ExternalSample/{PANEL_GUID}/Quotas/{quota_id}/Invite/{member_code}"
    
    logging.info(f"Generating invite for member {member_code} and quota {quota_id}...")
    response = make_toluna_request('POST', endpoint)
    
    if response and "URL" in response: # Check for expected key in successful response
        logging.info(f"Successfully generated invite for member {member_code}.")
        return response
    elif response and "error" in response:
        # Handle specific errors like 'Member Not Qualified', 'Quota Full', etc.
        logging.warning(f"Failed to generate invite for member {member_code}, quota {quota_id}: {response['error']}")
        return response
    else:
        logging.error(f"Unexpected response when generating invite: {response}")
        return {"error": "Unexpected API response", "details": response}

# --- Example Usage ---
# matched_member_code = "vtion_user_456"
# matched_quota_id = 12345 # Replace with an actual quota ID from get_available_quotas
# invite_response = generate_survey_invite(matched_member_code, matched_quota_id)
# if invite_response and "URL" in invite_response:
#     survey_url = invite_response['URL']
#     print(f"Survey URL: {survey_url}")
#     # Redirect user to survey_url
# else:
#     print(f"Could not generate invite. Reason: {invite_response.get('error', 'Unknown')}")

```

## 4. Handling Survey Completion (Redirect)

Toluna redirects the user back to a pre-configured URL on Vtion's side after the survey attempt. This URL should include parameters indicating the outcome.

**Example Redirect URL Structure (Configured in Toluna):**
`https://your-vtion-app.com/survey/callback?member={MemberCode}&status={SurveyStatus}&pid={TolunaPartnerID}&tid={TransactionID}&amt={Amount}`

**Backend Handler (Conceptual Example - e.g., using Flask):**

```python
# This is a conceptual example, adapt to your web framework (Flask, Django, etc.)
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/survey/callback', methods=['GET'])
# def handle_survey_callback():
#     member_code = request.args.get('member')
#     status = request.args.get('status') # e.g., 'C'=Complete, 'S'=Screenout, 'Q'=QuotaFull
#     transaction_id = request.args.get('tid')
#     amount = request.args.get('amt') # PartnerAmount from GenerateInvite response

#     logging.info(f"Received survey callback for member {member_code}, status {status}, tid {transaction_id}")

#     # --- Process the callback ---
#     # 1. Validate the callback (e.g., check transaction ID against stored invites)
#     # 2. Update survey status in Vtion database
#     # 3. If status is 'C' (Complete):
#     #    - Credit user's account with the reward (use 'amount' or pre-configured value)
#     #    - Mark survey as completed for the user
#     # 4. If status is 'S' (Screenout) or 'Q' (QuotaFull):
#     #    - Mark survey attempt accordingly
#     #    - Potentially offer alternative surveys
#     # 5. Handle other statuses as needed

#     # --- Respond to the callback (optional, depends on flow) ---
#     # You might redirect the user to a specific page in your app
#     # return redirect(url_for('survey_complete_page', member_code=member_code))
#     return jsonify({"status": "Callback received", "member": member_code, "outcome": status}), 200

# if __name__ == '__main__':
#     # Run the Flask app (example)
#     # app.run(debug=True)
#     pass
```

## Integration Guidelines

1.  **Error Handling**: Implement robust error handling for all API calls. Check response status codes and error messages provided by Toluna. Implement retry logic for transient network issues.
2.  **Rate Limiting**: Be mindful of potential API rate limits. Implement appropriate delays or use caching strategies (especially for `Get Quotas`) to avoid hitting limits.
3.  **Security**: Store API keys securely. Never expose them in client-side code. Use HTTPS for all communication.
4.  **Data Mapping**: Maintain an up-to-date mapping of Vtion's internal demographic codes to Toluna's reference data codes. Regularly refresh reference data using the Reference Data API.
5.  **User Experience**: Provide clear feedback to users about survey availability, participation status, and rewards. Handle screenouts and quota-full scenarios gracefully.
6.  **Logging**: Implement comprehensive logging for all API interactions, including request payloads and responses (mask sensitive data). This is crucial for debugging.
7.  **Testing**: Test thoroughly in Toluna's staging/test environment before deploying to production. Test edge cases like incomplete profiles, invalid data, and various survey outcomes.
8.  **Asynchronous Operations**: Consider using background jobs or asynchronous tasks for operations like fetching quotas and matching users to avoid blocking user interactions.
9.  **Configuration Management**: Manage API keys, base URLs, and PanelGUIDs through configuration files or environment variables, not hardcoded in the source.
10. **Scalability**: Design the matching logic and data storage to handle a growing number of users and quotas efficiently.
