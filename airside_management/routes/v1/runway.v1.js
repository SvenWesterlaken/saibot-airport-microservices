const express = require('express');
const router = express.Router();
const amqpManager = require('../../events/amqp.manager');

router.get('/', (req, res) => {
	amqpManager.connect()
		.then((channel) => {
			amqpManager.sendMessageToQueue(channel, 'airside-runway', JSON.stringify({
				message: 'Hoi',
				code: 200
			}))
		});
	res.status(200).json({message: 'Welcome to Runway V1 API'});
});

module.exports = router;