# Saibot International Airport - Airside Management

## RabbitMQ Event Messages: ##

- **POST /api/v1/runway**

_Adds a new runway to the system_

**Message topic:** runway.create

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

**Message topic:** runway.update

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

**Message topic:** runway.delete

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

- **POST /api/v1/taxiway**

_Adds a new taxiway to the system_

**Message topic:** taxiway.create

**Message content:**

```json
{
  "id": "10ba038e-48da-487b-96e8-8d3b99b6d18a",
  "message": "New taxiway has been added successfully.",
  "from": "airside_management",
  "type": "CREATE",
  "data": {
    "identifier": "A",
    "from_point": "A2",
    "to_point": "A3"
  },
  "old_data": {}
}
```

- **PATCH /api/v1/taxiway/[id]**

_Updates an existing taxiway in the system_

**Message topic:** taxiway.update

**Message content:**

```json
{
  "id": "10ba038e-48da-487b-96e8-8d3b99b6d18a",
  "message": "Taxiway has been patched successfully.",
  "from": "airside_management",
  "type": "PATCH",
  "data": {
    "identifier": "A",
    "from_point": "A3",
    "to_point": "A4"
  },
  "old_data": {
    "identifier": "A",
    "from_point": "A2",
    "to_point": "A3"
  }
}
```

- **DELETE /api/v1/taxiway/[id]**

_Deletes an existing taxiway in the system_

**Message topic:** taxiway.delete

**Message content:**

```json
{
  "id": "10ba038e-48da-487b-96e8-8d3b99b6d18a",
  "message": "Taxiway has been deleted successfully.",
  "from": "airside_management",
  "type": "DELETE",
  "data": {},
  "old_data": {
    "identifier": "A",
    "from_point": "A2",
    "to_point": "A3"
  }
}
```

- **POST /api/v1/fuel**

_Adds a new fuel tank to the system_

**Message topic:** fuel.create

**Message content:**

```json
{
  "id": "10ba038e-48da-487b-96e8-8d3b99b6d18a",
  "message": "New fuel tank has been added successfully.",
  "from": "airside_management",
  "type": "CREATE",
  "data": {
    "fuel_level": 943839,
    "fuel_capacity": 1000000
  },
  "old_data": {}
}
```

- **PATCH /api/v1/fuel/[id]**

_Updates an existing fuel tank in the system_

**Message topic:** fuel.update

**Message content:**

```json
{
  "id": "10ba038e-48da-487b-96e8-8d3b99b6d18a",
  "message": "Fuel tank has been patched successfully.",
  "from": "airside_management",
  "type": "PATCH",
  "data": {
    "fuel_level": 943839,
    "fuel_capacity": 1000000
  },
  "old_data": {
    "fuel_level": 943000,
    "fuel_capacity": 1000000
  }
}
```

- **DELETE /api/v1/fuel/[id]**

_Deletes an existing fuel tank in the system_

**Message topic:** fuel.delete

**Message content:**

```json
{
  "id": "10ba038e-48da-487b-96e8-8d3b99b6d18a",
  "message": "Fuel tank has been deleted successfully.",
  "from": "airside_management",
  "type": "DELETE",
  "data": {},
  "old_data": {
    "fuel_level": 943839,
    "fuel_capacity": 1000000
  }
}
```