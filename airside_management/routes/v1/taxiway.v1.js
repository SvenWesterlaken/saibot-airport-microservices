const express = require('express');
const router = express.Router();
const amqpManager = require('../../events/amqp.manager');
const uuid = require('uuid/v4');

router.get('/', (req, res) => {
	//TODO Get taxiways from database
	//TODO Add ID
	let payload = [
		{
			identifier: 'A',
			from_point: 'A1',
			to_point: 'A2'
		},
		{
			identifier: 'A',
			from_point: 'A2',
			to_point: 'A3'
		},
		{
			identifier: 'B',
			from_point: 'B1',
			to_point: 'B2'
		}
	];
	
	res.status(200).json({taxiways: payload});
});

router.get('/:id', (req, res) => {
	let id = req.params.id;
	
	//TODO Get taxiway from database
	let payload = {
		identifier: 'A',
		from_point: 'A2',
		to_point: 'A3'
	};
	
	res.status(200).json(payload);
});

router.post('/', (req, res) => {
	let body = req.body;
	
	//Check for missing properties
	if (!body.identifier || !body.from_point || !body.to_point) {
		res.status(400).json({error: 'Invalid request.'});
	}
	
	//TODO Implement logic to add taxiway to database
	
	//Create message payload
	let payload = {
		id: uuid(),
		message: 'New taxiway has been added successfully.',
		from: 'airside_management',
		type: 'CREATE',
		data: {
			identifier: body.identifier,
			from_point: body.from_point,
			to_point: body.to_point
		},
		old_data: {}
	};
	
	amqpManager.connect()
		.then((channel) => {
			amqpManager.sendMessageToQueue(channel, 'airside-taxiway', JSON.stringify(payload));
			res.status(201).json(payload);
		})
		.catch((error) => {
			res.status(400).json({
				message: 'Unable to add new taxiway.',
				error: error
			});
		});
});

router.patch('/:id', (req, res) => {
	let id = req.params.id;
	let body = req.body;
	
	//TODO Get taxiway data from database, and patch
	
	let payload = {
		id: uuid(),
		message: 'Taxiway has been patched successfully.',
		from: 'airside_management',
		type: 'PATCH',
		data: {
			identifier: body.identifier,
			from_point: body.from_point,
			to_point: body.to_point
		},
		old_data: {
			identifier: body.identifier,
			from_point: body.from_point,
			to_point: body.to_point
		}
	};
	
	amqpManager.connect()
		.then((channel) => {
			amqpManager.sendMessageToQueue(channel, 'airside-taxiway', JSON.stringify(payload));
			res.status(201).json(payload);
		})
		.catch((error) => {
			res.status(400).json({
				message: 'Unable to patch taxiway.',
				error: error
			});
		});
});

router.delete('/:id', (req, res) => {
	let id = req.params.id;
	
	//TODO Get taxiway data from database, and remove
	
	let payload = {
		id: uuid(),
		message: 'Taxiway has been deleted successfully.',
		from: 'airside_management',
		type: 'DELETE',
		data: {},
		old_data: {
			identifier: 'A',
			from_point: 'A2',
			to_point: 'A3'
		}
	};
	
	amqpManager.connect()
		.then((channel) => {
			amqpManager.sendMessageToQueue(channel, 'airside-taxiway', JSON.stringify(payload));
			res.status(201).json(payload);
		})
		.catch((error) => {
			res.status(400).json({
				message: 'Unable to delete taxiway.',
				error: error
			});
		});
});

module.exports = router;