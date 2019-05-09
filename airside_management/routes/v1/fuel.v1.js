const express = require('express');
const router = express.Router();
const amqpManager = require('../../events/amqp.manager');
const uuid = require('uuid/v4');

router.get('/', (req, res) => {
	//TODO Get current fuel levels from database
	
	let payload = [
		{
			fuel_level: 1000000,
			fuel_capacity: 1000000
		},
		{
			fuel_level: 943839,
			fuel_capacity: 1000000
		},
		{
			fuel_level: 32029,
			fuel_capacity: 500000
		}
	];
	
	res.status(200).json({fuel_levels: payload});
});

router.get('/:id', (req, res) => {
	let id = req.params.id;
	
	//TODO Get fuel tank usage from database
	
	let payload = {
		fuel_level: 943839,
		fuel_capacity: 1000000
	};
	
	res.status(200).json(payload);
});

router.post('/', (req, res) => {
	let body = req.body;
	
	if (!body.fuel_level || !body.fuel_capacity) {
		res.status(400).json({error: 'Invalid request.'});
	}
	
	//TODO Add new fuel tank to the database
	
	//Create message payload
	let payload = {
		id: uuid(),
		message: 'New fuel tank has been added successfully.',
		from: 'airside_management',
		type: 'CREATE',
		data: {
			fuel_level: body.fuel_level,
			fuel_capacity: body.fuel_capacity
		},
		old_data: {}
	};
	
	amqpManager.connect()
		.then((channel) => {
			amqpManager.sendMessageToQueue(channel, 'airside-fuel', JSON.stringify(payload));
			res.status(201).json(payload);
		})
		.catch((error) => {
			res.status(400).json({
				message: 'Unable to add new fuel tank.',
				error: error
			});
		});
});

router.patch('/:id', (req, res) => {
	let id = req.params.id;
	let body = req.body;
	
	//TODO Get fuel tank data from database, and patch
	
	let payload = {
		id: uuid(),
		message: 'Fuel tank has been patched successfully.',
		from: 'airside_management',
		type: 'PATCH',
		data: {
			fuel_level: body.fuel_level,
			fuel_capacity: body.fuel_capacity
		},
		old_data: {
			fuel_level: body.fuel_level,
			fuel_capacity: body.fuel_capacity
		}
	};
	
	amqpManager.connect()
		.then((channel) => {
			amqpManager.sendMessageToQueue(channel, 'airside-fuel', JSON.stringify(payload));
			res.status(201).json(payload);
		})
		.catch((error) => {
			res.status(400).json({
				message: 'Unable to patch fuel tank.',
				error: error
			});
		});
});

router.delete('/:id', (req, res) => {
	let id = req.params.id;
	
	//TODO Get fuel tank data from database, and remove
	
	let payload = {
		id: uuid(),
		message: 'Fuel tank has been deleted successfully.',
		from: 'airside_management',
		type: 'PATCH',
		data: {},
		old_data: {
			fuel_level: 943839,
			fuel_capacity: 1000000
		}
	};
	
	amqpManager.connect()
		.then((channel) => {
			amqpManager.sendMessageToQueue(channel, 'airside-fuel', JSON.stringify(payload));
			res.status(201).json(payload);
		})
		.catch((error) => {
			res.status(400).json({
				message: 'Unable to delete fuel tank.',
				error: error
			});
		});
});

module.exports = router;