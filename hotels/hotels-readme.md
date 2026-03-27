# Hotels Data Structure

This document describes the structure of the `HotelsData_toAzureBlobs.json` file.

## Overview

The JSON file contains an array of hotel objects, each with detailed information about the hotel, its location, and available rooms.

## Data Structure

### Entity Relationship

```mermaid
erDiagram
    HOTEL ||--|| ADDRESS : has
    HOTEL ||--|| LOCATION : has
    HOTEL ||--o{ ROOM : contains
    
    HOTEL {
        string HotelId PK
        string HotelName
        string Description
        string Description_fr
        string Category
        array Tags
        boolean ParkingIncluded
        boolean IsDeleted
        datetime LastRenovationDate
        float Rating
    }
    
    ADDRESS {
        string StreetAddress
        string City
        string StateProvince
        string PostalCode
        string Country
    }
    
    LOCATION {
        string type
        array coordinates
    }
    
    ROOM {
        string Description
        string Description_fr
        string Type
        float BaseRate
        string BedOptions
        int SleepsCount
        boolean SmokingAllowed
        array Tags
    }
```

### Class Diagram

```mermaid
classDiagram
    class Hotel {
        +string HotelId
        +string HotelName
        +string Description
        +string Description_fr
        +string Category
        +string[] Tags
        +boolean ParkingIncluded
        +boolean IsDeleted
        +datetime LastRenovationDate
        +float Rating
        +Address Address
        +Location Location
        +Room[] Rooms
    }
    
    class Address {
        +string StreetAddress
        +string City
        +string StateProvince
        +string PostalCode
        +string Country
    }
    
    class Location {
        +string type
        +float[] coordinates
    }
    
    class Room {
        +string Description
        +string Description_fr
        +string Type
        +float BaseRate
        +string BedOptions
        +int SleepsCount
        +boolean SmokingAllowed
        +string[] Tags
    }
    
    Hotel "1" *-- "1" Address : contains
    Hotel "1" *-- "1" Location : contains
    Hotel "1" *-- "0..*" Room : contains
```

### Structure Flow

```mermaid
graph TD
    A[Hotels Array] --> B[Hotel Object]
    B --> C[Basic Info]
    B --> D[Address Object]
    B --> E[Location Object]
    B --> F[Rooms Array]
    
    C --> C1[HotelId]
    C --> C2[HotelName]
    C --> C3[Description & Description_fr]
    C --> C4[Category]
    C --> C5[Tags]
    C --> C6[ParkingIncluded]
    C --> C7[IsDeleted]
    C --> C8[LastRenovationDate]
    C --> C9[Rating]
    
    D --> D1[StreetAddress]
    D --> D2[City]
    D --> D3[StateProvince]
    D --> D4[PostalCode]
    D --> D5[Country]
    
    E --> E1[type: Point]
    E --> E2[coordinates: longitude, latitude]
    
    F --> G[Room Object]
    G --> G1[Description & Description_fr]
    G --> G2[Type]
    G --> G3[BaseRate]
    G --> G4[BedOptions]
    G --> G5[SleepsCount]
    G --> G6[SmokingAllowed]
    G --> G7[Tags]
```

## Field Descriptions

### Hotel Object

| Field | Type | Description |
|-------|------|-------------|
| `HotelId` | string | Unique identifier for the hotel |
| `HotelName` | string | Name of the hotel |
| `Description` | string | Hotel description in English |
| `Description_fr` | string | Hotel description in French |
| `Category` | string | Hotel category (e.g., "Boutique") |
| `Tags` | array of strings | Amenities and features (e.g., "view", "air conditioning", "concierge") |
| `ParkingIncluded` | boolean | Whether parking is included |
| `IsDeleted` | boolean | Soft delete flag |
| `LastRenovationDate` | datetime | ISO 8601 format timestamp of last renovation |
| `Rating` | float | Hotel rating (e.g., 3.60) |
| `Address` | object | Physical address of the hotel |
| `Location` | object | Geographic coordinates (GeoJSON format) |
| `Rooms` | array of objects | Available room types |

### Address Object

| Field | Type | Description |
|-------|------|-------------|
| `StreetAddress` | string | Street address |
| `City` | string | City name |
| `StateProvince` | string | State or province code |
| `PostalCode` | string | ZIP/postal code |
| `Country` | string | Country name |

### Location Object

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | GeoJSON type (always "Point") |
| `coordinates` | array of floats | [longitude, latitude] in decimal degrees |

### Room Object

| Field | Type | Description |
|-------|------|-------------|
| `Description` | string | Room description in English |
| `Description_fr` | string | Room description in French |
| `Type` | string | Room type (e.g., "Budget Room", "Suite", "Deluxe Room") |
| `BaseRate` | float | Nightly rate in USD |
| `BedOptions` | string | Bed configuration (e.g., "1 Queen Bed", "2 Double Beds") |
| `SleepsCount` | integer | Maximum occupancy |
| `SmokingAllowed` | boolean | Whether smoking is permitted |
| `Tags` | array of strings | Room-specific amenities (e.g., "vcr/dvd", "jacuzzi tub") |

## Example Data

```json
{
  "HotelId": "1",
  "HotelName": "Stay-Kay City Hotel",
  "Description": "This classic hotel is fully-refurbished...",
  "Description_fr": "Cet hôtel classique entièrement rénové...",
  "Category": "Boutique",
  "Tags": ["view", "air conditioning", "concierge"],
  "ParkingIncluded": false,
  "IsDeleted": false,
  "LastRenovationDate": "2022-01-18T00:00:00Z",
  "Rating": 3.60,
  "Address": {
    "StreetAddress": "677 5th Ave",
    "City": "New York",
    "StateProvince": "NY",
    "PostalCode": "10022",
    "Country": "USA"
  },
  "Location": {
    "type": "Point",
    "coordinates": [-73.975403, 40.760586]
  },
  "Rooms": [
    {
      "Description": "Budget Room, 1 Queen Bed (Cityside)",
      "Description_fr": "Chambre Économique, 1 grand lit (côté ville)",
      "Type": "Budget Room",
      "BaseRate": 96.99,
      "BedOptions": "1 Queen Bed",
      "SleepsCount": 2,
      "SmokingAllowed": true,
      "Tags": ["vcr/dvd"]
    }
  ]
}
```

## Notes

- The file format is standard JSON array containing hotel objects
- All descriptions are provided in both English and French
- Location coordinates follow the GeoJSON specification (longitude first, then latitude)
- Each hotel can have multiple room types with varying rates and amenities
- The data structure is suitable for Azure Blob Storage and Azure Cognitive Search indexing
