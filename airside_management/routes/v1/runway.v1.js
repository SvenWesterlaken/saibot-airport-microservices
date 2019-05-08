const express = require('express');
const router = express.Router();
const amqpManager = require('../../events/amqp.manager');
const uuid = require('uuid/v4');

router.get('/', (req, res) => {
	let payload = [
		{
			side1: '36L',
			side2: '18R',
			length: 3800,
			width: 60
		},
		{
			side1: '09',
			side2: '27',
			length: 3453,
			width: 45
		}
	];
	res.status(200).json({runways: payload});
});

router.get('/:id', (req, res) => {
	let payload = {
		side1: '36L',
		side2: '18R',
		length: 3800,
		width: 60
	};
	
	res.status(200).json({runway: payload});
});

router.post('/', (req, res) => {
	let body = req.body;
	
	//Check for missing properties
	if (!body.side1 || !body.side2 || !body.length || !body.width) {
		res.status(400).json({error: 'Invalid request.'});
	}
	
	//TODO Implement logic to add runway to database
	
	//Create message payload
	let payload = {
		id: uuid(),
		message: 'New runway has been added successfully.',
		from: 'airside_management',
		type: 'CREATE',
		data: {
			side1: body.side1,
			side2: body.side2,
			length: body.length,
			width: body.width
		},
		old_data: {}
	};
	
	//Send message
	amqpManager.connect()
		.then((channel) => {
			amqpManager.sendMessageToQueue(channel, 'airside-runway', JSON.stringify(payload));
			res.status(201).json(payload);
		});
});

router.delete('/:id', (req, res) => {
	let runwayId = req.params.id;
	
	//TODO Get runway data from database, and remove
	
	let payload = {
		id: uuid(),
		message: 'Runway has been delete successfully.',
		from: 'airside_management',
		'type': 'DELETE',
		data: {},
		old_data: {
			side1: '36L',
			side2: '18R',
			length: 3800,
			width: 60
		}
	};
	
	amqpManager.connect()
		.then((channel) => {
			amqpManager.sendMessageToQueue(channel, 'airside-runway', JSON.stringify(payload));
			res.status(200).json(payload);
		});
});

module.exports = router;