const express = require('express');
const router = express.Router();
const amqpManager = require('../../events/amqp.manager');
const uuid = require('uuid/v4');
const Fuel = require('../../models/fuel.model');
const RmqFuel = Fuel.rmq;

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

			let channel = amqpManager.channel;
			const key = 'fuel.create';
				try {
					amqpManager.sendMessageToQueue(channel, key, JSON.stringify(payload));
				} catch (err) {
					const rmqPayload = new RmqFuel(payload);
					rmqPayload.key = key;

						rmqPayload.save().then(() => {
							console.log("Fuel created, but unable to publish event")})
				}

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

					let channel = amqpManager.channel;
					const key = 'fuel.update';
					try {
						amqpManager.sendMessageToQueue(channel, key, JSON.stringify(payload));
					} catch (err) {
						const rmqPayload = new RmqFuel(payload);
						rmqPayload.key = key;
						rmqPayload.save().then(() => {
							console.log("Fuel patched, but unable to publish event")})
					}
					res.status(201).json(payload);
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

			let channel = amqpManager.channel;
			const key = 'fuel.delete';
			try {
				amqpManager.sendMessageToQueue(channel, key, JSON.stringify(payload));
			} catch (err) {
				const rmqPayload = new RmqFuel(payload);
				rmqPayload.key = key;
				rmqPayload.save().then(() => {
					console.log("Fuel deleted, but unable to publish event")})
			}
			res.status(201).json(payload);
		})
		.catch((error) => res.status(400).json(error));
});

module.exports = router;