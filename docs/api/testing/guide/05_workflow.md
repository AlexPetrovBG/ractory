## 9. Workflow Management Tests (`/api/v1/workflow`)

Requires at least `ProjectManager` role. Assume `$COMP_A_PM_TOKEN` is available for a Project Manager in `$COMPANY_A_GUID` (created in User Management tests or use an equivalent). Also assume `$WS_A_GUID` (a workstation in Company A) is available.

### 9.1 Create Workflow Entry
```bash
# Ensure COMP_A_PM_TOKEN, COMPANY_A_GUID, and WS_A_GUID are correctly set from previous tests.
ACTION_VALUE_JSON="{\\\"barcode\\\": \\\"WF_TEST_$(date +%N)\\\", \\\"station_check\\\": true}"

WORKFLOW_CREATE_RESP=$(curl -s -X POST -H "Content-Type: application/json" \
     -H "Authorization: Bearer $COMP_A_PM_TOKEN" \
     -d "{\"action_type\": \"barcode_scan\", \"company_guid\": \"$COMPANY_A_GUID\", \"workstation_guid\": \"$WS_A_GUID\", \"action_value\": \"$ACTION_VALUE_JSON\"}" \
     http://localhost:8000/api/v1/workflow | jq '.')
WORKFLOW_ENTRY_GUID=$(echo $WORKFLOW_CREATE_RESP | jq -r '.guid')
echo "Workflow Entry GUID: $WORKFLOW_ENTRY_GUID"
echo $WORKFLOW_CREATE_RESP
```
**Expected (201 Created):** Workflow entry details. 
-   Verify `company_name`, `workstation_name`, `user_name` are auto-populated.
-   Test with an invalid `action_type` (expect `422 Unprocessable Entity` with a list of valid types).
-   Test creating without `user_guid` (should default to current token's user).

### 9.2 List Workflow Entries
```bash
cURL -s -G -H "Authorization: Bearer $COMP_A_PM_TOKEN" \
     --data-urlencode "action_type=barcode_scan" \
     --data-urlencode "workstation_guid=$WS_A_GUID" \
     --data-urlencode "limit=5" \
     "http://localhost:8000/api/v1/workflow" | jq '.'
# Test with date filters: start_date, end_date
# Test pagination: limit, offset
```
**Expected (200 OK):** List of workflow entries for the company, matching filters.

### 9.3 Get Workflow Entry
```bash
cURL -s -G -H "Authorization: Bearer $COMP_A_PM_TOKEN" \
     "http://localhost:8000/api/v1/workflow/$WORKFLOW_ENTRY_GUID" | jq '.'
```
**Expected (200 OK):** Specific workflow entry details.
-   Attempt to get entry from another company (using different user token) should fail `403`/`404`.

### 9.4 Get Workflow Statistics
```bash
# Get stats for last 7 days for the current user's company
START_DATE_STATS=$(date -u +%Y-%m-%dT00:00:00Z --date='-7 days')
cURL -s -G -H "Authorization: Bearer $COMP_A_PM_TOKEN" \
     --data-urlencode "start_date=$START_DATE_STATS" \
     "http://localhost:8000/api/v1/workflow/statistics" | jq '.'
```
**Expected (200 OK):** Workflow statistics object (verify structure against `WorkflowStatistics` schema). 