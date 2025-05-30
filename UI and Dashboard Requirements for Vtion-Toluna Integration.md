# UI and Dashboard Requirements for Vtion-Toluna Integration

## User Interface Requirements

### 1. User Profile UI

#### Profile Creation/Update Screen
- **Required Fields Section**:
  - Date of Birth field (with date picker)
  - Gender selection (dropdown or radio buttons)
  - Clear indication of required vs. optional fields
- **Additional Profile Fields Section**:
  - Education level
  - Employment status
  - Income range
  - Postal code
  - Country
  - Ethnicity
  - Language preference
- **Profile Completion Indicator**:
  - Visual progress bar showing profile completion percentage
  - Suggestions for completing profile to qualify for more surveys
- **Privacy Information**:
  - Clear explanation of how data will be used
  - Consent checkboxes for data sharing with Toluna
  - Link to privacy policy

### 2. Survey Discovery UI

#### Survey Listing Screen
- **Survey Card Components** (for each available survey):
  - Survey title/topic
  - Estimated completion time (in minutes)
  - Reward amount (prominently displayed)
  - Survey category or type indicator
  - Visual indicator for survey compatibility (desktop/mobile/tablet)
  - "Start Survey" button
- **Filtering and Sorting Options**:
  - Sort by reward amount (high to low)
  - Sort by completion time (shortest first)
  - Filter by category/topic
  - Filter by device compatibility
- **Empty State Handling**:
  - Friendly message when no surveys are available
  - Suggestion to complete profile for more opportunities
  - Estimated time for new survey availability

#### Survey Details Modal/Screen
- **Detailed Information**:
  - Comprehensive survey description
  - Topic and category details
  - Specific device requirements
  - Expiration time/date (if applicable)
- **Participation Controls**:
  - Prominent "Start Now" button
  - "Save for Later" option (if supported)
  - "Not Interested" option to remove from list

### 3. Survey Participation UI

#### Survey Transition Screens
- **Pre-Survey Screen**:
  - Loading indicator while generating survey link
  - Brief instructions or tips for successful completion
  - Reminder of estimated completion time
- **Post-Survey Return Screen**:
  - Success confirmation message
  - Reward earned confirmation
  - Option to rate survey experience
  - Suggestions for additional available surveys

#### Survey Status Indicators
- **Progress Tracking**:
  - Visual indicator for surveys in progress
  - Resume capability for interrupted surveys (if supported)
- **Completion Status**:
  - Clear indication of completed surveys
  - History of participation with outcomes

### 4. Notification UI

#### In-App Notifications
- **Survey Availability Alerts**:
  - New survey notifications with reward amount
  - Personalized survey recommendations
  - Expiring survey reminders
- **Status Updates**:
  - Reward credited notifications
  - Profile update reminders
  - Survey qualification changes

#### Push Notification Templates
- **New Survey Available**:
  - Brief description with reward amount
  - Direct deep link to survey listing
- **Survey Expiring Soon**:
  - Urgency indicator with time remaining
  - One-tap access to start survey

### 5. Rewards and History UI

#### Rewards Dashboard
- **Earnings Summary**:
  - Total rewards earned
  - Pending rewards
  - Recent activity
- **Detailed History**:
  - Complete survey participation history
  - Outcome of each survey attempt (completed, screened out, etc.)
  - Reward amount for each completed survey
  - Date and time of participation

## Admin Dashboard Requirements

### 1. Integration Management UI

#### Configuration Panel
- **API Connection Settings**:
  - Toluna API credentials management
  - Panel GUID configuration
  - Environment selection (test/production)
  - API endpoint URLs
- **Integration Status**:
  - Connection health indicators
  - Last successful sync timestamp
  - Error logs and alerts

#### Mapping Configuration
- **Field Mapping Controls**:
  - User data field mapping to Toluna fields
  - Custom field mapping options
  - Validation rule configuration
- **Reference Data Management**:
  - Country code mapping
  - Education level mapping
  - Employment status mapping
  - Other demographic value mappings

### 2. User Management Dashboard

#### User Overview
- **User Statistics**:
  - Total registered users
  - Users with complete profiles
  - Users with incomplete profiles
  - Active survey takers
- **User Search and Filtering**:
  - Search by user ID, email, or name
  - Filter by profile completion status
  - Filter by survey participation level
  - Filter by demographic attributes

#### User Detail View
- **Profile Information**:
  - Complete user profile data
  - Profile completion status
  - Toluna Member ID mapping
  - Profile update history
- **Survey Participation**:
  - Survey history for specific user
  - Completion rates and patterns
  - Reward history
  - Survey eligibility status

### 3. Survey Management Dashboard

#### Survey Catalog
- **Available Quotas**:
  - Complete list of current Toluna quotas
  - Quota details (requirements, rewards, etc.)
  - Quota status (open, filling, closed)
  - Remaining capacity
- **Survey Configuration**:
  - Ability to enable/disable specific surveys
  - Custom reward setting per survey
  - Priority configuration
  - Custom targeting rules

#### Survey Performance
- **Completion Metrics**:
  - Start rates
  - Completion rates
  - Screen-out rates
  - Average completion time
- **Demographic Performance**:
  - Completion rates by demographic segments
  - Screen-out patterns by demographics
  - Targeting effectiveness analysis

### 4. Performance Analytics Dashboard

#### Real-time Monitoring
- **Current Activity**:
  - Active survey sessions
  - Users currently taking surveys
  - Surveys nearing quota capacity
  - API call volume and response times
- **Today's Summary**:
  - Surveys started today
  - Surveys completed today
  - Total rewards issued today
  - New user registrations

#### Historical Analytics
- **Trend Analysis**:
  - Daily/weekly/monthly completion trends
  - Revenue trends
  - User participation patterns
  - Seasonal variations
- **Performance Comparisons**:
  - Survey performance comparisons
  - Demographic group comparisons
  - Time period comparisons

### 5. Financial Management Dashboard

#### Revenue Tracking
- **Earnings Overview**:
  - Total revenue from Toluna
  - Revenue by survey category
  - Revenue by time period
  - Projected earnings
- **Payment Reconciliation**:
  - Completed surveys vs. payments received
  - Discrepancy identification
  - Invoice generation
  - Payment status tracking

#### Reward Management
- **Reward Distribution**:
  - Total rewards issued to users
  - Rewards by survey type
  - Rewards by user segment
  - Reward efficiency metrics
- **Reward Configuration**:
  - Global reward rate settings
  - Custom reward multipliers
  - Bonus program management
  - Reward approval workflows

### 6. System Health Dashboard

#### API Monitoring
- **Connection Status**:
  - Real-time API connectivity indicators
  - Response time monitoring
  - Error rate tracking
  - Rate limit usage
- **Error Logging**:
  - Detailed API error logs
  - Error categorization
  - Resolution status tracking
  - Trend analysis of common errors

#### System Performance
- **Resource Utilization**:
  - Server load metrics
  - Database performance
  - Cache efficiency
  - Background job status
- **Alert Configuration**:
  - Custom alert thresholds
  - Notification routing
  - Escalation rules
  - Scheduled maintenance management

## Mobile App-Specific UI Requirements

### Responsive Design Considerations
- All user interfaces must be fully responsive
- Survey cards should adapt to different screen sizes
- Touch-friendly controls with appropriate sizing
- Simplified navigation for mobile users

### Mobile-Specific Features
- Streamlined profile completion process
- Survey compatibility indicators for mobile devices
- Optimized survey transition experience
- Mobile-friendly notification management

## Implementation Guidelines

### UI/UX Best Practices
- Maintain consistent branding with Vtion's existing design language
- Use clear, concise language for all instructions
- Implement progressive disclosure for complex information
- Ensure accessibility compliance throughout

### Technical Considerations
- Use responsive frameworks for all UI components
- Implement efficient data loading with pagination
- Cache survey data to minimize API calls
- Ensure secure handling of user credentials and tokens

### Dashboard Development Approach
- Build modular dashboard components
- Implement role-based access control
- Design for extensibility as integration evolves
- Include comprehensive export capabilities for all data

This comprehensive UI and dashboard requirements document provides a detailed blueprint for implementing both the user-facing and administrative interfaces needed for the Vtion-Toluna integration using the IP-ES approach.
