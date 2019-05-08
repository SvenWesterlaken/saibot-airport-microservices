const amqpManager = require('../amqp.manager');

module.exports.init = function(queueName, callbackEvent) {
	amqpManager.connect()
		.then((channel) => {
			amqpManager.consumeFromQueue(channel, queueName, callbackEvent);
		})
		.catch((error) => {
			console.log(error);
		});
};