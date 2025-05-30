# Vtion-Toluna API Integration Manual

## Executive Summary

This comprehensive manual provides a complete guide for integrating Vtion's app with Toluna's survey platform using the IP-ES (External Sample) integration approach. After thorough analysis of both IP-ES and IP-DASH options, IP-ES is recommended as the optimal solution for Vtion due to its greater control over sampling, access to all open quotas, and real-time information capabilities.

The integration can be completed within the required 2-day timeframe by following the detailed implementation plan, code samples, and guidelines provided in this manual. This document serves as a complete reference for technical implementation, user experience design, and administrative oversight of the integration.

## Table of Contents

1. [Integration Options Analysis](#integration-options-analysis)
2. [User Data Mapping](#user-data-mapping)
3. [User and Admin Flows](#user-and-admin-flows)
4. [UI and Dashboard Requirements](#ui-and-dashboard-requirements)
5. [Implementation Plan](#implementation-plan)
6. [Code Samples and Guidelines](#code-samples-and-guidelines)
7. [Validation and Edge Cases](#validation-and-edge-cases)
8. [Appendices and References](#appendices-and-references)

## Integration Options Analysis

Toluna offers two primary integration approaches:

### IP-ES (External Sample)
- Provides near real-time details about Toluna's open quotas
- Vtion maintains control over sampling and targeting
- Access to all open quotas
- Higher flexibility in user experience customization
- More complex implementation but greater control

### IP-DASH (Dashboard)
- Relies on Toluna's router to match surveys to members
- Simpler implementation with fewer endpoints
- Less control over survey matching
- Cached results (1-minute cache)
- More standardized user experience

### Recommendation
Based on comprehensive analysis, **IP-ES (External Sample)** is recommended for Vtion because:
1. It provides access to all open quotas, maximizing survey opportunities
2. It offers greater control over which surveys are presented to which users
3. It provides near real-time information about available surveys
4. It allows for better customization of the user experience
5. Despite being slightly more complex, it can still be implemented within the 2-day timeframe

For detailed comparison, please refer to the [comparison.md](comparison.md) document.

## User Data Mapping

### Required User Data Fields
At minimum, Toluna requires **Date of Birth** and **Gender** for all members. Additional recommended fields include:

| Toluna Field | Data Type | Description | Vtion Data Source |
|--------------|-----------|-------------|-------------------|
| MemberCode | String/Int | Unique identifier | Vtion User ID |
| PartnerGUID | GUID | Toluna-provided identifier | Provided by Toluna |
| BirthDate | Date | Member's date of birth (YYYY-MM-DD) | User profile DOB |
| Gender | Int | Member's gender (1=Male, 2=Female, 3=Other) | User profile gender |
| PostalCode | String | Member's postal/ZIP code | User address |
| Country | Int | Member's country | User location |
| EducationLevel | Int | Highest education level | User profile |
| EmploymentStatus | Int | Current employment status | User profile |

For complete mapping details, data transformation requirements, and validation rules, please refer to the [user_data_mapping.md](user_data_mapping.md) document.

## User and Admin Flows

### User Flow
1. **Registration and Profile Creation**: User signs up and completes profile
2. **Survey Discovery**: System matches users with appropriate surveys
3. **Survey Notification**: Available surveys are displayed to the user
4. **Survey Selection**: User selects a survey and receives a unique link
5. **Survey Completion**: User completes the survey on Toluna's platform
6. **Post-Survey Experience**: User returns to Vtion app and receives reward

### Admin Flow
1. **Integration Setup**: Configure API credentials and settings
2. **User Management**: Monitor and manage user profiles
3. **Survey Management**: Monitor available surveys and performance
4. **Performance Monitoring**: Track key metrics and analytics
5. **Notification Management**: Configure user notifications
6. **Financial Reconciliation**: Manage rewards and revenue
7. **System Health Monitoring**: Ensure system functionality

For detailed flow diagrams, API touchpoints, and error handling strategies, please refer to the [user_admin_flows.md](user_admin_flows.md) document.

## UI and Dashboard Requirements

### User Interface Components
- **Profile UI**: Profile creation/update screens with completion indicators
- **Survey Discovery UI**: Survey listing with filtering and sorting options
- **Survey Participation UI**: Transition screens and status indicators
- **Notification UI**: In-app and push notification templates
- **Rewards UI**: Earnings summary and detailed history

### Admin Dashboard Components
- **Integration Management UI**: Configuration panel and mapping controls
- **User Management Dashboard**: User statistics and detailed views
- **Survey Management Dashboard**: Survey catalog and performance metrics
- **Performance Analytics**: Real-time monitoring and historical analysis
- **Financial Management**: Revenue tracking and reward distribution
- **System Health Dashboard**: API monitoring and performance metrics

For comprehensive UI specifications and dashboard requirements, please refer to the [ui_dashboard_requirements.md](ui_dashboard_requirements.md) document.

## Implementation Plan

The implementation is structured as a 2-day plan:

### Day 1: Core Integration and Member Management
- **Phase 1**: Setup and Configuration (2 hours)
- **Phase 2**: Member Management Implementation (3 hours)
- **Phase 3**: Survey Quota Retrieval (3 hours)

### Day 2: Survey Integration and User Experience
- **Phase 4**: Survey Invitation Implementation (2 hours)
- **Phase 5**: User Interface Implementation (4 hours)
- **Phase 6**: Admin Dashboard Implementation (4 hours)
- **Phase 7**: Integration Testing and Optimization (2 hours)

Each phase includes detailed tasks, testing procedures, and deliverables. For the complete implementation timeline, deployment plan, and maintenance procedures, please refer to the [implementation_plan.md](implementation_plan.md) document.

## Code Samples and Guidelines

### Key API Integration Points
1. **Member Registration/Update**
```python
def register_or_update_member(member_data):
    """Registers a new member or updates an existing one in Toluna."""
    endpoint = f"/IntegratedPanelService/api/v2/Respondent/{PANEL_GUID}/{member_data['MemberCode']}"
    # Implementation details in code_samples.py
```

2. **Get Available Quotas**
```python
def get_available_quotas(include_routables=True):
    """Retrieves the list of open survey quotas from Toluna."""
    endpoint = f"/IPExternalSamplingService/ExternalSample/{PANEL_GUID}/Quotas"
    # Implementation details in code_samples.py
```

3. **Generate Survey Invite**
```python
def generate_survey_invite(member_code, quota_id):
    """Generates a survey invite link for a member and quota."""
    endpoint = f"/IPExternalSamplingService/ExternalSample/{PANEL_GUID}/Quotas/{quota_id}/Invite/{member_code}"
    # Implementation details in code_samples.py
```

For complete code samples, error handling, and integration guidelines, please refer to the [code_samples.py](code_samples.py) file.

## Validation and Edge Cases

### Critical Path Validation
All integration components have been validated, with potential risks and mitigation strategies identified for:
- Member Management API
- Quota Retrieval
- Survey Matching
- Invite Generation
- Survey Completion
- User Interface
- Admin Dashboard

### Edge Cases Addressed
1. **User Profile Edge Cases**: Incomplete profiles, conflicting data, profile changes
2. **API and Integration Edge Cases**: API downtime, rate limiting, version changes
3. **User Experience Edge Cases**: Survey availability fluctuations, termination handling
4. **Business Logic Edge Cases**: Reward discrepancies, quota fulfillment tracking
5. **Technical Implementation Edge Cases**: Database scaling, network reliability

For detailed risk assessment, mitigation strategies, and additional recommendations, please refer to the [validation_edge_cases.md](validation_edge_cases.md) document.

## Appendices and References

### Toluna API Documentation
- IP-ES (External Sample): [https://docs.integratedpanel.toluna.com/externalsample/](https://docs.integratedpanel.toluna.com/externalsample/)
- Member Management: [https://docs.integratedpanel.toluna.com/membermanagement/](https://docs.integratedpanel.toluna.com/membermanagement/)
- Reference Data API: [https://docs.integratedpanel.toluna.com/mapping/referencedataapi/](https://docs.integratedpanel.toluna.com/mapping/referencedataapi/)

### Supporting Documents
- [comparison.md](comparison.md): Detailed comparison of IP-ES and IP-DASH options
- [user_data_mapping.md](user_data_mapping.md): Complete user data mapping specifications
- [user_admin_flows.md](user_admin_flows.md): Detailed user and admin flow diagrams
- [ui_dashboard_requirements.md](ui_dashboard_requirements.md): UI and dashboard specifications
- [implementation_plan.md](implementation_plan.md): Step-by-step implementation plan
- [code_samples.py](code_samples.py): Code samples and integration guidelines
- [validation_edge_cases.md](validation_edge_cases.md): Validation and edge case handling

### Contact Information
For technical support or questions about the Toluna API integration, please contact Toluna support at the contact information provided in their documentation.

---

This integration manual provides a comprehensive guide for implementing the Vtion-Toluna integration using the IP-ES approach. By following the detailed instructions, code samples, and best practices outlined in this document and its supporting files, Vtion can successfully complete the integration within the required 2-day timeframe.
