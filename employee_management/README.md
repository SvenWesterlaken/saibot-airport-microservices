# Saibot International Airport - Employee Management

## RabbitMQ Event Messages: ##

- **POST /api/v1/employee**

_Adds a new employee to the system_

**Message topic:** employee.create

**Message content:**

```json
{
  "id": "10ba038e-48da-487b-96e8-8d3b99b6d18a",
  "message": "New employee has been added successfully.",
  "from": "employee_management",
  "type": "CREATE",
  "data": {
    "first_name": "Pieter",
    "last_name": "Janssen",
    "dob": "1997-12-22"
  },
  "old_data": {}
}
```

- **PATCH /api/v1/employee/[id]**

_Updates an existing employee in the system_

**Message topic:** employee.update

**Message content:**

```json
{
  "id": "10ba038e-48da-487b-96e8-8d3b99b6d18a",
  "message": "Employee has been patched successfully.",
  "from": "employee_management",
  "type": "PATCH",
  "data": {
      "first_name": "Pieter",
      "last_name": "Janssen",
      "dob": "1997-12-22"
  },
  "data": {
      "first_name": "Hans",
      "last_name": "Janssen",
      "dob": "1997-12-22"
  }
}
```

- **DELETE /api/v1/employee/[id]**

_Deletes an existing employee in the system_

**Message topic:** employee.delete

**Message content:**

```json
{
  "id": "10ba038e-48da-487b-96e8-8d3b99b6d18a",
  "message": "Employee has been deleted successfully.",
  "from": "employee_management",
  "type": "DELETE",
  "data": {},
  "old_data": {
      "first_name": "Pieter",
      "last_name": "Janssen",
      "dob": "1997-12-22"
  }
}
```
