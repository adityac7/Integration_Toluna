# End-to-End User and Admin Flows for Vtion-Toluna Integration

## User Flow

### 1. User Registration and Profile Creation
- **User Action**: Signs up on Vtion app and completes profile information
- **System Action**: 
  - Stores user data in Vtion database
  - Sends user data to Toluna via Member Management API
  - Minimum required fields: Date of Birth and Gender
  - Recommended: Include additional demographic information for better survey matching

### 2. Survey Discovery
- **System Action**:
  - Vtion backend periodically calls Toluna's Get Quotas API to retrieve available surveys
  - Applies sampling logic to match users with appropriate surveys based on:
    - Demographic requirements
    - Survey quotas
    - User preferences
    - Previous participation history
  - Stores matched surveys in Vtion database

### 3. Survey Notification and Presentation
- **User Action**: Opens Vtion app and navigates to surveys section
- **System Action**:
  - Displays list of available surveys matched to the user
  - For each survey, shows:
    - Estimated completion time (LOI - Length of Interview)
    - Reward amount
    - Brief description or category
    - Expiration time (if applicable)

### 4. Survey Selection
- **User Action**: Selects a survey from the available options
- **System Action**:
  - Calls Toluna's Generate Invite API to get a unique survey link for the user
  - Records the survey invitation in Vtion's database
  - Redirects user to the survey via the generated link

### 5. Survey Completion
- **User Action**: Completes the survey on Toluna's platform
- **System Action**:
  - Toluna redirects user back to Vtion app with status parameters
  - Vtion processes the return status:
    - If completed: Credits user's account with appropriate reward
    - If screened out: Records status and potentially offers alternative surveys
    - If quota full: Updates survey availability and offers alternatives

### 6. Post-Survey Experience
- **User Action**: Returns to Vtion app after survey completion
- **System Action**:
  - Displays completion confirmation and reward information
  - Updates user's survey history
  - Offers additional available surveys
  - Updates user's profile with any new information learned

## Admin Flow

### 1. Integration Setup and Configuration
- **Admin Action**: Configures Toluna integration settings
- **System Components**:
  - API credentials storage
  - Panel GUID configuration
  - Survey reward mapping
  - Sampling rules configuration

### 2. User Management
- **Admin Action**: Monitors and manages user profiles
- **System Capabilities**:
  - View users with complete/incomplete profiles
  - Check user eligibility status for surveys
  - Manually update user profiles when needed
  - Handle user opt-out requests

### 3. Survey Management
- **Admin Action**: Monitors available surveys and performance
- **System Capabilities**:
  - View all available quotas from Toluna
  - Set survey visibility rules (who can see which surveys)
  - Configure survey prioritization
  - Set custom reward amounts per survey
  - Pause/resume specific surveys

### 4. Performance Monitoring
- **Admin Action**: Tracks key performance metrics
- **System Dashboards**:
  - Survey completion rates
  - Screen-out rates
  - Average reward per user
  - User participation frequency
  - Revenue tracking
  - API call volume and performance

### 5. Notification Management
- **Admin Action**: Configures user notifications
- **System Capabilities**:
  - Set rules for survey availability notifications
  - Configure reminder notifications
  - Customize notification content
  - Schedule promotional campaigns

### 6. Financial Reconciliation
- **Admin Action**: Manages financial aspects of the integration
- **System Capabilities**:
  - Track rewards issued to users
  - Monitor revenue from Toluna
  - Generate financial reports
  - Reconcile completed surveys with payments

### 7. System Health Monitoring
- **Admin Action**: Ensures system is functioning properly
- **System Capabilities**:
  - Monitor API connectivity with Toluna
  - Track API error rates
  - Set up alerts for critical issues
  - View system logs for troubleshooting

## Integration Touchpoints with Toluna API

### User Flow API Touchpoints
1. **User Registration/Update**:
   ```
   POST https://{IP_ES_URL}/IntegratedPanelService/api/Respondent
   ```

2. **Get Available Surveys**:
   ```
   GET https://{IP_ES_URL}/IPExternalSamplingService/ExternalSample/{PanelGUID}/Quotas
   ```

3. **Generate Survey Invite**:
   ```
   POST https://{IP_ES_URL}/IPExternalSamplingService/ExternalSample/{PanelGUID}/Quotas/{QuotaID}/Invite/{MemberCode}
   ```

### Admin Flow API Touchpoints
1. **Reference Data Retrieval**:
   ```
   GET https://{IP_CORE_URL}/IntegratedPanelService/api/ReferenceData
   ```

2. **Survey Wave Exclusion**:
   ```
   GET https://{IP_ES_URL}/IPExternalSamplingService/ExternalSample/SurveyWaveExclusions
   ```

3. **Get Quota Details**:
   ```
   GET https://{IP_ES_URL}/IPExternalSamplingService/ExternalSample/{PanelGUID}/Quotas/{QuotaID}
   ```

## Data Flow Diagram

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│             │         │             │         │             │
│  Vtion App  │◄────────│  Vtion API  │◄────────│ Toluna API  │
│  (User)     │         │  Server     │         │             │
│             │─────────►│             │─────────►│             │
└─────────────┘         └─────────────┘         └─────────────┘
                              ▲                        ▲
                              │                        │
                              ▼                        │
                        ┌─────────────┐               │
                        │             │               │
                        │  Vtion      │               │
                        │  Admin      │───────────────┘
                        │  Dashboard  │
                        │             │
                        └─────────────┘
```

## Error Handling and Edge Cases

### User Flow Error Handling
1. **Incomplete Profile**:
   - Detect missing required fields
   - Prompt user to complete profile before showing surveys
   - Store partial data and resume when profile is completed

2. **No Available Surveys**:
   - Display appropriate message
   - Offer profile enhancement options to qualify for more surveys
   - Provide estimated time for new survey availability

3. **Survey Link Expiration**:
   - Monitor link validity timeframe
   - Regenerate link if expired
   - Track and limit regeneration attempts

4. **Survey Termination**:
   - Process different termination reasons
   - Provide appropriate feedback based on termination type
   - Update user eligibility for future surveys

### Admin Flow Error Handling
1. **API Connection Issues**:
   - Implement retry logic with exponential backoff
   - Alert administrators of persistent connection problems
   - Maintain local cache of critical data for temporary offline operation

2. **Data Synchronization Errors**:
   - Log detailed error information
   - Provide manual reconciliation tools
   - Implement periodic consistency checks

3. **Quota Management**:
   - Handle sudden quota closures
   - Update survey availability in near real-time
   - Prevent users from attempting to access closed quotas

## Implementation Considerations

1. **Scalability**:
   - Design for handling increasing user volume
   - Implement efficient caching of quota data
   - Consider batch processing for user-survey matching

2. **Performance**:
   - Optimize API calls to Toluna
   - Pre-fetch and cache survey data when possible
   - Implement background processing for non-critical operations

3. **User Experience**:
   - Minimize waiting time for survey availability
   - Provide clear status updates throughout the process
   - Design intuitive survey discovery and selection interface

4. **Admin Experience**:
   - Create intuitive dashboards with actionable insights
   - Provide flexible configuration options
   - Implement robust reporting capabilities

This end-to-end flow design provides a comprehensive blueprint for implementing the Vtion-Toluna integration using the IP-ES approach, covering all user touchpoints, admin controls, and system interactions required for a successful implementation.
