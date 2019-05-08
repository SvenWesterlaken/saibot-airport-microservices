const express = require('express');
const router = express.Router();
const amqpManager = require('../../events/amqp.manager');

router.get('/', (req, res) => {
	res.status(200).json({message: 'Welcome to Runway V1 API'});
});

module.exports = router;