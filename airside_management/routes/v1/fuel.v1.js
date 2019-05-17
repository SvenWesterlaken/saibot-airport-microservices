const express = require('express');
const router = express.Router();
const amqpManager = require('../../events/amqp.manager');
const uuid = require('uuid/v4');
const Fuel = require('../../models/fuel.model');
const RmqFuel = Fuel.rmq

router.get('/', (req, res) => {
	Fuel.find({})
		.then((containers) => {
			res.status(200).json(containers);
		})
		.catch((error) => res.status(400).json(error));
});

router.get('/:id', (req, res) => {
	let id = req.params.id;
	
	Fuel.findOne({_id: id})
		.then((container) => {
			res.status(200).json(container);
		})
		.catch((error) => res.status(400).json(error));
});

router.post('/', (req, res) => {
	let body = req.body;
	
	if (!body.fuel_level || !body.fuel_capacity) {
		res.status(400).json({error: 'Invalid request.'});
	}
	
	Fuel.create(body)
		.then((container) => {
			let payload = {
				id: uuid(),
				message: 'New fuel tank has been added successfully.',
				from: 'airside_management',
				type: 'CREATE',
				data: container
			};
			
			amqpManager.connectRmq()
				.then((channel) => {
					amqpManager.sendMessageToQueue(channel, 'fuel.create', JSON.stringify(payload));
				})
				.catch((error) => {
					const rmqPayload = new RmqFuel(payload);

					rmqPayload.save().then((c) => {
						console.log("Fuel created, but unable to connect to RabbitMQ")})
				});
			res.status(201).json(payload);
	})
	.catch((error) => res.status(400).json(error));
});

router.patch('/:id', (req, res) => {
	let id = req.params.id;
	let body = req.body;
	
	Fuel.findOne({_id: id})
		.then((result) => {
			let oldContainer = result;
			let oldCapacity = oldContainer.fuel_capacity;
			let oldLevel = oldContainer.fuel_level;
			
			if (body.fuel_capacity != null)
				oldContainer.fuel_capacity = body.fuel_capacity;
			
			if (body.fuel_level != null) 
				oldContainer.fuel_level = body.fuel_level;
			
			oldContainer.save()
				.then((container) => {
					let payload = {
						id: uuid(),
						message: 'Fuel tank has been patched successfully.',
						from: 'airside_management',
						type: 'PATCH',
						data: container,
						old_data: {
							fuel_level: oldLevel,
							fuel_capacity: oldCapacity
						}
					};
					
					amqpManager.connectRmq()
						.then((channel) => {
							amqpManager.sendMessageToQueue(channel, 'fuel.update', JSON.stringify(payload));
							res.status(201).json(payload);
						})
						.catch((error) => {
							res.status(400).json({
								message: 'Unable to patch fuel tank.',
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
	
	Fuel.findOneAndDelete({_id: id})
		.then((container) => {
			let payload = {
				id: uuid(),
				message: 'Fuel tank has been deleted successfully.',
				from: 'airside_management',
				type: 'DELETE',
				data: {},
				old_data: container
			};
			
			amqpManager.connectRmq()
				.then((channel) => {
					amqpManager.sendMessageToQueue(channel, 'fuel.delete', JSON.stringify(payload));
					res.status(201).json(payload);
				})
				.catch((error) => {
					res.status(400).json({
						message: 'Unable to delete fuel tank.',
						error: error
					});
				});
		})
		.catch((error) => res.status(400).json(error));
});

module.exports = router;