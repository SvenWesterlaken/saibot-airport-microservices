const express = require('express');
const router = express.Router();
const amqpManager = require('../../events/amqp.manager');
const uuid = require('uuid/v4');
const Runway = require('../../models/runway.model');

router.get('/', (req, res) => {
	Runway.find({})
		.then((runways) => {
			res.status(200).json(runways);
		})
		.catch((error) => res.status(400).json(error));
});

router.get('/:id', (req, res) => {
	let id = req.params.id;
	
	Runway.findOne({_id: id})
		.then((runway) => {
			res.status(200).json(runway);
		})
		.catch((error) => res.status(400).json(error));
});

router.post('/', (req, res) => {
	let body = req.body;
	
	//Check for missing properties
	if (!body.side1 || !body.side2 || !body.length || !body.width) {
		res.status(400).json({error: 'Invalid request.'});
	}
	
	Runway.create(body)
		.then((runway) => {
			//Create message payload
			let payload = {
				id: uuid(),
				message: 'New runway has been added successfully.',
				from: 'airside_management',
				type: 'CREATE',
				data: runway,
				old_data: {}
			};
			
			//Send message
			amqpManager.connectRmq()
				.then((channel) => {
					amqpManager.sendMessageToQueue(channel, 'runway.create', JSON.stringify(payload));
					res.status(201).json(payload);
				})
				.catch((error) => {
					res.status(400).json({
						message: 'Unable to add new runway.',
						error: error
					});
				});
		})
		.catch((error) => res.status(400).json(error));
});

router.patch('/:id', (req, res) => {
	let id = req.params.id;
	let body = req.body;
	
	Runway.findOne({_id: id})
		.then((result) => {
			let oldRunway = result;
			let oldSide1 = result.side1;
			let oldSide2 = result.side2;
			let oldLength = result.length;
			let oldWidth = result.width;
			
			if (body.side1 != null)
				oldRunway.side1 = body.side1;
			
			if (body.side2 != null)
				oldRunway.side2 = body.side2;
			
			if (body.length != null)
				oldRunway.length = body.length;
			
			if (body.width != null)
				oldRunway.width = body.width;
			
			oldRunway.save()
				.then((runway) => {
					let payload = {
						id: uuid(),
						message: 'Runway has been patched successfully.',
						from: 'airside_management',
						type: 'PATCH',
						data: runway,
						old_data: {
							side1: oldSide1,
							side2: oldSide2,
							length: oldLength,
							width: oldWidth
						}
					};
					
					amqpManager.connectRmq()
						.then((channel) => {
							amqpManager.sendMessageToQueue(channel, 'runway.update', JSON.stringify(payload));
							res.status(200).json(payload);
						})
						.catch((error) => {
							res.status(400).json({
								message: 'Unable to patch runway.',
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
	
	Runway.findOneAndDelete({_id: id})
		.then((runway) => {
			let payload = {
				id: uuid(),
				message: 'Runway has been deleted successfully.',
				from: 'airside_management',
				type: 'DELETE',
				data: {},
				old_data: runway
			};
			
			amqpManager.connectRmq()
				.then((channel) => {
					amqpManager.sendMessageToQueue(channel, 'runway.delete', JSON.stringify(payload));
					res.status(200).json(payload);
				})
				.catch((error) => {
					res.status(400).json({
						message: 'Unable to delete runway.',
						error: error
					});
				});
		})
		.catch((error) => res.status(400).json(error));
});

module.exports = router;