# Mapping Vtion User Data to Toluna API Requirements

## Overview
This document outlines how Vtion's user data should be mapped to Toluna's API requirements for the IP-ES (External Sample) integration. Proper data mapping is essential for successful integration and ensuring users receive relevant surveys.

## Required User Data Fields

Toluna requires specific demographic information to match users with appropriate surveys. At minimum, **Date of Birth** and **Gender** are required for all members.

### Minimum Required Fields

| Toluna Field | Data Type | Description | Vtion Data Source | Transformation Needed |
|--------------|-----------|-------------|-------------------|----------------------|
| MemberCode | String/Int | Unique identifier for the member | Vtion User ID | None - Use existing unique ID |
| PartnerGUID | GUID | Toluna-provided unique identifier for Vtion's panel | Provided by Toluna | None - Use as provided by Toluna |
| BirthDate | Date | Member's date of birth (YYYY-MM-DD) | User profile DOB | Format as YYYY-MM-DD if not already |
| Gender | Int | Member's gender (1=Male, 2=Female, 3=Other) | User profile gender | Map to Toluna codes (1, 2, 3) |

### Recommended Additional Fields

These additional fields will improve survey matching and user experience:

| Toluna Field | Data Type | Description | Vtion Data Source | Transformation Needed |
|--------------|-----------|-------------|-------------------|----------------------|
| PostalCode | String | Member's postal/ZIP code | User address | None |
| Country | Int | Member's country | User location | Map to Toluna country codes |
| Language | String | Member's preferred language | User preferences | Use ISO language codes |
| EducationLevel | Int | Highest education level | User profile | Map to Toluna education codes |
| EmploymentStatus | Int | Current employment status | User profile | Map to Toluna employment codes |
| Ethnicity | Int | Member's ethnicity | User profile | Map to Toluna ethnicity codes |
| Income | Int | Household income range | User profile | Map to Toluna income range codes |
| DeviceTypeIDs | Array[Int] | Devices member can use for surveys | User device info | Map to Toluna device type codes (1=Desktop/Laptop, 2=Tablet, 3=Phone) |

## Data Transformation Requirements

### Gender Mapping
```
Vtion Gender → Toluna Gender Code
Male → 1
Female → 2
Other/Non-binary → 3
```

### Country Mapping
Toluna uses specific country codes that need to be mapped from Vtion's country data. The complete list is available via Toluna's Reference Data API, but common examples include:
```
US/USA/United States → 1
UK/United Kingdom → 2
CA/Canada → 3
```

### Education Level Mapping
```
No formal education → 1
Primary education → 2
Secondary education → 3
Vocational/Technical → 4
Bachelor's degree → 5
Master's degree → 6
Doctorate → 7
```

## API Integration Points for User Data

### 1. Member Registration/Update
When a new user registers on Vtion or updates their profile, their data should be sent to Toluna using the Member Management API:

```
POST https://{IP_ES_URL}/IntegratedPanelService/api/Respondent
```

### 2. Before Survey Matching
When retrieving quotas and generating invites, ensure the member data is up-to-date in Toluna's system.

### 3. Data Privacy Considerations
- Only send the minimum required data for survey matching
- Ensure compliance with data protection regulations
- Implement proper consent mechanisms for data sharing

## Data Validation Rules

Before sending user data to Toluna, validate:

1. **Date of Birth** is in valid format (YYYY-MM-DD) and represents an age between 18-100
2. **Gender** is mapped to valid Toluna codes (1, 2, or 3)
3. **PostalCode** follows the correct format for the member's country
4. All mapped codes (Country, Education, etc.) are valid according to Toluna's reference data

## Error Handling for Data Issues

| Error Scenario | Handling Approach |
|----------------|-------------------|
| Missing required fields | Prompt user to complete profile before offering surveys |
| Invalid data format | Transform to correct format if possible, otherwise prompt user to correct |
| Unknown mapping values | Use default/most common value and log for review |
| API rejection of data | Retry with corrected data or flag account for manual review |

## Implementation Recommendations

1. **Cache Reference Data**: Retrieve and cache Toluna's reference data (country codes, education levels, etc.) to minimize API calls
2. **Batch Updates**: When possible, batch member updates rather than sending individual API calls
3. **Progressive Profiling**: Implement a system to gradually collect additional profile data from users
4. **Data Synchronization**: Establish a regular process to ensure Vtion and Toluna data remains in sync

## Testing Data Mapping

Before full implementation, test the data mapping with:
1. A sample of existing users with complete profiles
2. Edge cases (users with minimal data, unusual demographic combinations)
3. Various device types to ensure device detection works correctly

This comprehensive mapping ensures that Vtion's user data will be properly integrated with Toluna's system, maximizing the relevance of surveys offered to users and optimizing completion rates.
