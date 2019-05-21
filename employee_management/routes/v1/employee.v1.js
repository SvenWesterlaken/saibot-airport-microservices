const express = require('express');
const router = express.Router();
const Employee = require('../../models/employee.model');
const amqpManager = require('../../events/amqp.manager');
const uuid = require('uuid/v4');

router.get('/', (req, res) => {
	Employee.find({})
		.then((employees) => res.status(200).json(employees))
		.catch((error) => res.status(400).json(error));
});

router.get('/:id', (req, res) => {
	let id = req.params.id;
	
	Employee.findOne({_id: id})
		.then((employee) => res.status(200).json(employee))
		.catch((error) => res.status(400).json(error));
});

router.post('/', (req, res) => {
	let body = req.body;
	
	if (!body.first_name || !body.last_name || !body.dob) {
		res.status(400).json({error: 'Invalid request.'});
	}
	
	Employee.create(body)
		.then((employee) => {
			let payload = {
				id: uuid(),
				message: 'New employee has been added successfully.',
				from: 'employee_management',
				type: 'CREATE',
				data: employee,
				old_data: {}
			};
			
			amqpManager.connectRmq()
				.then((channel) => {
					amqpManager.sendMessageToQueue(channel, 'employee.create', JSON.stringify(payload));
					res.status(201).json(payload);
				})
				.catch((error) => {
					res.status(400).json({
						message: 'Unable to add new employee.',
						error: error
					});
				});
		})
		.catch((error) => res.status(400).json(error));
});

router.patch('/:id', (req, res) => {
	let id = req.params.id;
	let body = req.body;
	
	Employee.findOne({_id: id})
		.then((result) => {
			let oldEmployee = result;
			let oldFirstName = result.first_name;
			let oldLastName = result.last_name;
			let oldDob = result.dob;
			
			if (body.first_name != null)
				oldEmployee.first_name = body.first_name;
			
			if (body.last_name != null)
				oldEmployee.last_name = body.last_name;
			
			if (body.dob != null)
				oldEmployee.dob = body.dob;
			
			oldEmployee.save()
				.then((employee) => {
					let payload = {
						id: uuid(),
						message: 'Employee has been patched successfully.',
						from: 'employee_management',
						type: 'PATCH',
						data: employee,
						old_data: {
							first_name: oldFirstName,
							last_name: oldLastName,
							dob: oldDob
						}
					};
					
					amqpManager.connectRmq()
						.then((channel) => {
							amqpManager.sendMessageToQueue(channel, 'employee.update', JSON.stringify(payload));
							res.status(201).json(payload);
						})
						.catch((error) => {
							res.status(400).json({
								message: 'Unable to patch employee.',
								error: error
							});
						});
				})
				.catch((error) => res.status(400).json(error));
		})
		.catch((error) => res.status(400).json(error));
});

router.delete('/:id', (req, res) => {
	let id = req.params.id;
	
	Employee.findOneAndDelete({_id: id})
		.then((employee) => {
			let payload = {
				id: uuid(),
				message: 'Employee has been deleted successfully.',
				from: 'employee_management',
				type: 'DELETE',
				data: {},
				old_data: employee
			};
			
			amqpManager.connectRmq()
				.then((channel) => {
					amqpManager.sendMessageToQueue(channel, 'employee.delete', JSON.stringify(payload));
					res.status(201).json(payload);
				})
				.catch((error) => {
					res.status(400).json({
						message: 'Unable to delete employee.',
						error: error
					});
				});
		})
		.catch((error) => res.status(400).json(error));
});

module.exports = router;