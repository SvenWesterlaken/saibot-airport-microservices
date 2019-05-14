# Saibot International Airport - Airside Management

##RabbitMQ Event Messages: ##

- **POST /api/v1/runway**

_Adds a new runway to the system_

**Message sent in queue:** airside-runway

**Message content:**

```json
{
  "id": "10ba038e-48da-487b-96e8-8d3b99b6d18a",
  "message": "New runway has been added successfully.",
  "from": "airside_management",
  "type": "CREATE",
  "data": {
    "side1": "36L",
    "side2": "18R",
    "length": 3800,
    "width": 60
  },
  "old_data": {}
}
```

- **PATCH /api/v1/runway/[id]**

_Updates an existing runway in the system_

**Message sent in queue:** airside-runway

**Message content:**

```json
{
  "id": "10ba038e-48da-487b-96e8-8d3b99b6d18a",
  "message": "Runway has been patched successfully.",
  "from": "airside_management",
  "type": "PATCH",
  "data": {
    "side1": "36L",
    "side2": "18R",
    "length": 3900,
    "width": 65
  },
  "old_data": {
    "side1": "36L",
    "side2": "18R",
    "length": 3800,
    "width": 60
  }
}
```

- **DELETE /api/v1/runway/[id]**

_Deletes an existing runway in the system_

**Message sent in queue:** airside-runway

**Message content:**

```json
{
  "id": "10ba038e-48da-487b-96e8-8d3b99b6d18a",
  "message": "Runway has been deleted successfully.",
  "from": "airside_management",
  "type": "DELETE",
  "data": {},
  "old_data": {
    "side1": "36L",
    "side2": "18R",
    "length": 3800,
    "width": 60
  }
}
```