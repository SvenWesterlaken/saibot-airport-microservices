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
					amqpManager.sendMessageToQueue(channel, 'employee-management', JSON.stringify(payload));
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

module.exports = router;