# Saibot International Airport

## Usage
### Setup
The whole application architecture can be started by using docker compose with the following command:
```
docker-compose up
```
This will start all available microservices.

### Applications
Once everything is started the following microservices should be available:

#### Airport Microservices

| Microservice                    | Url                     | Endpoint documentation            |
| ------------------------------- | ----------------------- | ----------------------            |
| **Flight Management**           | http://localhost:5001/  | http://localhost:5001/api/1/docs  |
| **Airplane Management**         | http://localhost:5002/  | http://localhost:5002/api/1/docs  |
| **Airside Management**          | http://localhost:5003/  | Postman scripts                   |
| **Gate Management**             | http://localhost:5004/  | http://localhost:5004/api/1/docs  |
| **Check-in Counter Management** | http://localhost:5005/  | http://localhost:5004/api/1/docs  |
| **Employee Management**         | http://localhost:5007/  | Postman scripts                   |
| **Security Management**         | http://localhost:5008/  | http://localhost:5008/api/1/docs  |

#### Management/Development Microservices

| Microservice                    | Url                     |
| ------------------------------- | ----------------------- |
| PHPMyAdmin                      | http://localhost:8080/  |
| Container Visualizer            | http://localhost:9000/  |
| RabbitMQ                        | http://localhost:15672/ |


---

## Assigment Information

**Motivation for chosen concepts can be found [here](/_docs/motivation_document.pdf)!**

### Functional requirements:
- [x] An airline is able to register itself at an airport.
- [x] An airline can park their planes at a gate.
- [x] An airline can arrive and depart with their planes at scheduled runways.
- [x] An airline can request time slots for flights.
- [x] An airline can register airplanes.
- [x] The airport can schedule flights requested by airlines.
- [x] The airport can assign a gate and check-in counters for each flight.
- [ ] Passengers are informed of gate and check-in counter changes for their flight.
- [ ] Passengers are able to check themselves in at the check-in counter.
- [ ] Visitors are able to check in their baggage at the check-in counter.
- [ ] All airport customers are billed through the airport financial department.
- [ ] All payments have to be successfully authorised before finalizing an action or
request.
- [ ] Visitors are able to park at the airport.
- [ ] All internal transactions in the airport are also billed through the airport financial
department.
- [x] Security is able to have insight in all airport events.
- [ ] External baggage companies are notified of changes in baggage status.
- [ ] External baggage companies are able to notify airport of changes in baggage status.
- [ ] Passengers are able to claim their baggage
- [ ] Plane is not able to leave the gate until authorized by ground personnel and control
tower.
- [ ] A plane cannot land or take-off on runway without authorization of the control tower.
- [ ] Airside department notifies ground personnel when and where planes need to be
refueled.
- [ ] Retail is able to rent a spot at the tax-free zones.

### Requirements for assignment:
1. - [x] ArchiMate model of the enterprise architecture. (http://pubs.opengroup.org/architecture/archimate-doc/ts_archimate/)
2. - [x] Context map.
3. - [x] Non-functional requirements.
4. - [x] Functional requirements added to the given requirements, based on assumptions.
5. - [ ] Implementation of all functional and non-functional requirements as described for your case.
6. - [x] Postman or Swagger scripts that trigger the various RESTful Web API’s to allow showing that functionality works. So, there’s no need to create a GUI in order to save you work.
7. - [x] Docker image of your application.
8. - [x] Motivation of each of the following concepts as applied to your case in a document. Use of these concepts is mandatory. Describe where it is applied and why it is applied:
    - [x] Microservices based on the principles of DDD
    - [x] Eventual consistency
    - [x] Event driven architecture based on messaging
    - [x] Command Query Responsibility Segregation (CQRS)
    - [x] Event Sourcing
    - [x] Enterprise Integration Patterns (at least one)

### Context Map:

![Context Map](/_docs/context_diagram/context_map.png)
