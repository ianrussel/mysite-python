Welcome to TimeTracking Documentation
This documentation provides instructions on how to integrate this project to synchronize Timesheet.com data with Gusto.com Payroll.

This documentation also covers the endpoints, usage instructions, and architecture.

1. The first step is to authorize the Timesheet.com application to connect to your Gusto.com account. For more info, see the API documentation

2. Sync the Timesheet Payroll to Gusto Payroll For more info, see the API documentation

Connection Architecture Diagram
POST /connection/connect
Validate Credentials
Store Timesheet Credentials
Generate Gusto Auth URL
User Authorizes
Redirect with code + state
Exchange Code for Token
Store Gusto Credentials
Generate API Key for User
Run Employee Mapper
User / Timesheet App
Internal DB
Timesheet API
Redirect to Gusto OAuth
Gusto
Gusto API
Auto/Manual Employee Mapper

🔄 Connection Flow Steps
User initiates connection via /connection/connect.
TimetrackingApp validates the user's Timesheet API credentials.
Timesheet credentials are saved to the internal database.
Gusto authorization URL is generated and the user is redirected.
User authorizes access on Gusto.
Gusto redirects back with an authorization code and state.
TimetrackingApp exchanges the code for a token via the Gusto API.
Gusto credentials are saved to the database.
An API key is generated specific to the user/account.
Employee Mapper runs, with an option for manual override.


Overview: Payroll Sync Architecture
This architecture outlines the data synchronization flow between a Timesheet App and the Gusto payroll platform. The integration enables users to seamlessly sync employee timesheet data for a selected payroll period with Gusto’s payroll processing system.

🧑‍💼 Actors:
Timesheet App User: Initiates the sync process by selecting a date range and triggering the sync.
TimetrackingApp: Backend logic orchestrator handling validations, data processing, and communication with Gusto.
Timesheet API: Source of employee timesheet data.
Gusto API: Destination for payroll processing.
Employee Mapper: Maps internal user data to Gusto-compatible structure.
🔗 Integration Flow:
Date Range Selection The user selects a payroll period within the Timesheet App UI.

Payroll Sync Trigger User clicks the Sync Payroll button, initiating the backend flow in the TimetrackingApp.

Validation Phase The system performs a series of checks as defined in sync_payroll_requirements.html, such as:

Required mappings

Data completeness
Credential verification

Conditional Flow

If invalid, the system immediately returns validation errors to the user.

If valid, the sync process proceeds.

Data Fetch and Mapping

Timesheet data is fetched from the Timesheet API.

Employee data is mapped using the Employee Mapping Logic.

Data Transformation The fetched and mapped data is formatted to Gusto’s required schema.

Sync to Gusto The formatted data is pushed to Gusto API for processing.

Response Handling

Gusto responds with success or failure.
The TimetrackingApp logs the result, sends an email notification to the user, and displays the outcome in the UI.
✅ Benefits:
Automation: Reduces manual data entry and errors.
Validation Layer: Ensures data integrity before reaching Gusto.
User Feedback Loop: Users are immediately informed via UI and email notifications.
Modular Design: Separation of concerns via distinct services (validation, mapping, formatting).

Sync Architecture Diagram
Selects Date Range
Clicks Sync Payroll
Validates Requirements
If Valid
If Invalid
Fetch Timesheet Data
Fetch Mapped Employee Data
Format Data for Gusto
Send Data to Gusto
Return Success or Error
Show Result to User
Send Email to User
Timesheet App User
TimesheetApp
TimetrackingApp
Validation Logic per sync_payroll_requirements.html
Proceed to Sync Payroll Data
Return Validation Errors to User
Timesheet API
Employee Mapping Logic
Data Formatter for Gusto API
Gusto API
SyncResult
🔄 Description of Flow:
User selects a date range for payroll.
User clicks the "Sync Payroll" button.
The Timetracking App performs validations based on requirements in sync_payroll_requirements.html.
If validation fails, the user is notified of errors.
If validation passes:
Timesheet data is fetched from the Timesheet API.
Mapped employee data is retrieved.
Data is formatted to match Gusto's API format.
Data is sent to Gusto.
Gusto API returns a success or failure response, TimetrackingApp process the response, send email to user/customer.
TimetrackingApp returns a success or failure response.
Sync results are shown to the user.

Sync API Reference
POST /api/v1/payroll/sync-payroll
Trigger payroll sync for a specified date range.

Headers
Name	Type	Description
x-app-api-key	string	Application-specific API key
x-ts-account	string	Timesheet account identifier
Request Body Parameters
Name	Type	Required	Description
date_start	string	Yes	Start date in YYYY-MM-DD format
date_end	string	Yes	End date in YYYY-MM-DD format
email	string	Yes	Valid email address to receive sync info
Validation Rules
All fields are required.
email must be in a valid format.
date_start and date_end must follow ISO format (YYYY-MM-DD).
date_start must not be later than date_end.
Example Request (Python)
import requests
import json

url = "http://localhost:5000/InternetTechnologyYMWrjhzKjcjPIkpi03eV/api/v1/payroll/sync-payroll"

payload = json.dumps({
  "date_start": "2025-02-08",
  "date_end": "2025-02-21",
  "email": "ianrussel537@gmail.com"
})
headers = {
  'x-app-api-key': '4b0a422b66c44c6fb28d504b1d6c025f',
  'x-ts-account': '2687',
  'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=payload)
print(response.text)

Sample response
{
  "message": "Payroll update task submitted.",
  "task_id": "8971b70c-1c8c-4fdc-803d-b7701f3cc1e2"
}

Sync Status API Reference
GET /api/v1/payroll/sync-payroll/task/
Fetch the status and detailed result of a submitted payroll sync task.

Path Parameters
Name	Type	Description
task_id	string	The unique ID of the submitted task
Headers
Name	Type	Description
x-app-api-key	string	Application-specific API key
x-ts-account	string	Timesheet account identifier
Example Request (Python)
import requests

url = "http://localhost:5000/InternetTechnologyYMWrjhzKjcjPIkpi03eV/api/v1/payroll/sync-payroll/task/8971b70c-1c8c-4fdc-803d-b7701f3cc1e2"

headers = {
  'x-app-api-key': '4b0a422b66c44c6fb28d504b1d6c025f',
  'x-ts-account': '2687'
}

response = requests.get(url, headers=headers)
print(response.text)

sample Successful Response
{
  "result": {
    "error": false,
    "response": {
      "auto_pilot": false,
      "check_date": "2025-05-27",
      "created_at": "2025-02-10T08:05:32Z",
      "employee_compensations": [
        {
          "employee_uuid": "69dea763-7356-4ee8-9445-120b2a60fe52",
          "excluded": false,
          "hourly_compensations": [
            {
              "name": "Regular Hours",
              "hours": "40.000",
              "compensation_multiplier": 1.0
            }
          ],
          "payment_method": "Direct Deposit"
        }
      ],
      "pay_period": {
        "start_date": "2025-02-08",
        "end_date": "2025-02-21"
      },
      "payroll_uuid": "e9d44646-f2e8-4cb4-a78c-c93e892cfec6",
      "status": "SUCCESS"
    },
    "status": 200
  }
}

Sync Status All API Reference
GET /api/v1/payroll/sync-payroll/tasks
Retrieve a list of all submitted payroll sync tasks for the authenticated account.

Headers
Name	Type	Description
x-app-api-key	string	Application-specific API key
x-ts-account	string	Timesheet account identifier
Example Request (Python)
import requests

url = "http://localhost:5000/InternetTechnologyYMWrjhzKjcjPIkpi03eV/api/v1/payroll/sync-payroll/tasks"

headers = {
  'x-app-api-key': '4b0a422b66c44c6fb28d504b1d6c025f',
  'x-ts-account': '2687'
}

response = requests.get(url, headers=headers)
print(response.text)

Example Response
{
  "data": [
    {
      "company_id": 1,
      "created_at": "Tue, 06 April 2025 07:47:49 GMT",
      "date_range": "2025-02-08|2025-02-21",
      "id": 1,
      "modified_at": "Tue, 06 April 2025 07:47:49 GMT",
      "status": "SUCCESS",
      "task_id": "8971b70c-1c8c-4fdc-803d-b7701f3cc1e2"
    },
    {
      "company_id": 1,
      "created_at": "Tue, 06 May 2025 07:47:49 GMT",
      "date_range": "2025-02-08|2025-02-21",
      "id": 2,
      "modified_at": "Tue, 06 May 2025 07:47:49 GMT",
      "status": "PENDING",
      "task_id": "8971b70c-1c8c-4fdc-803d-b7701f3cc1e2"
    }
  ],
  "message": "Success"
}

Using the demo

This system provides a guided interface to demonstrate key features related to payroll synchronization, company authorization, and employee mapping. It is intended for demo purposes and allows users to simulate actions with pre-defined email accounts. Each tab showcases different functionalities that mimic real-world workflows.

Instructions
Login to the system.
Use any demo email [ w***687@timesheets.com*,w**606@timesheets.com] For more info, see the Demo documentation and Demo Authentication
Navigate to any tabs ['Sync Payroll','Authorize Company', 'Employee Mapper']
Just follow the flow in the screen

Authentication
This section covers the login process required to access the system.

Login Screen
To begin, navigate to the login screen where you will be prompted to enter your credentials. Use one of the demo email addresses provided.

Login Screen

After logging in, you will be redirected to the main interface where you can access various features of the system.


Users
Demo users are for testing purposes only. They do not exist in the actual production database.

Current Demo Users
w****687@timesheets.com
w****606@timesheets.com
⚠️ These accounts are strictly for demonstration use and should not be considered valid for production access.

For more information, please contact Judy.