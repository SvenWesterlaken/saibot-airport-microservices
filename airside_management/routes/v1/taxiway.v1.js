const express = require('express');
const router = express.Router();
const amqpManager = require('../../events/amqp.manager');
const uuid = require('uuid/v4');
const Taxiway = require('../../models/taxiway.model');

router.get('/', (req, res) => {
	Taxiway.find({})
		.then((taxiways) => {
			res.status(200).json(taxiways);
		})
		.catch((error) => res.status(400).json(error));
});

router.get('/:id', (req, res) => {
	let id = req.params.id;
	
	Taxiway.findOne({_id: id})
		.then((taxiway) => {
			res.status(200).json(taxiway);
		})
		.catch((error) => res.status(400).json(error));
});

router.post('/', (req, res) => {
	let body = req.body;
	
	//Check for missing properties
	if (!body.identifier || !body.from_point || !body.to_point) {
		res.status(400).json({error: 'Invalid request.'});
	}
	
	Taxiway.create(body)
		.then((taxiway) => {
			//Create message payload
			let payload = {
				id: uuid(),
				message: 'New taxiway has been added successfully.',
				from: 'airside_management',
				type: 'CREATE',
				data: taxiway,
				old_data: {}
			};
			
			amqpManager.connectRmq()
				.then((channel) => {
					amqpManager.sendMessageToQueue(channel, 'taxiway.create', JSON.stringify(payload));
					res.status(201).json(payload);
				})
				.catch((error) => {
					res.status(400).json({
						message: 'Unable to add new taxiway.',
						error: error
					});
				});
		})
		.catch((error) => res.status(200).json(error));
});

router.patch('/:id', (req, res) => {
	let id = req.params.id;
	let body = req.body;
	
	Taxiway.findOne({_id: id})
		.then((result) => {
			let oldTaxiway = result;
			let oldIdentifier = result.identifier;
			let oldFromPoint = result.from_point;
			let oldToPoint = result.to_point;
			
			if (body.identifier != null)
				oldTaxiway.identifier = body.identifier;
			
			if (body.from_point != null)
				oldTaxiway.from_point = body.from_point;
			
			if (body.to_point != null)
				oldTaxiway.to_point = body.to_point;
			
			oldTaxiway.save()
				.then((taxiway) => {
					let payload = {
						id: uuid(),
						message: 'Taxiway has been patched successfully.',
						from: 'airside_management',
						type: 'PATCH',
						data: taxiway,
						old_data: {
							identifier: oldIdentifier,
							from_point: oldFromPoint,
							to_point: oldToPoint
						}
					};
					
					amqpManager.connectRmq()
						.then((channel) => {
							amqpManager.sendMessageToQueue(channel, 'taxiway.update', JSON.stringify(payload));
							res.status(201).json(payload);
						})
						.catch((error) => {
							res.status(400).json({
								message: 'Unable to patch taxiway.',
								error: error
							});
						});
				})
				.catch((error) => res.status(400).json(error));
		})
		.catch((error) => res.status(200).json(error));
});

router.delete('/:id', (req, res) => {
	let id = req.params.id;
	
	Taxiway.findOneAndDelete({_id: id})
		.then((taxiway) => {
			let payload = {
				id: uuid(),
				message: 'Taxiway has been deleted successfully.',
				from: 'airside_management',
				type: 'DELETE',
				data: {},
				old_data: taxiway
			};
			
			amqpManager.connectRmq()
				.then((channel) => {
					amqpManager.sendMessageToQueue(channel, 'taxiway.delete', JSON.stringify(payload));
					res.status(201).json(payload);
				})
				.catch((error) => {
					res.status(400).json({
						message: 'Unable to delete taxiway.',
						error: error
					});
				});
		})
		.catch((error) => res.status(400).json(error));
});

module.exports = router;