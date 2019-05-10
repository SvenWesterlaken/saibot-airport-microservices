const amqpManager = require('../amqp.manager');

module.exports.init = function(queueName, callbackEvent) {
	return amqpManager.connect()
		.then((channel) => {
			if (channel == undefined) {
				throw "Channel not found!"
			} else {
				amqpManager.consumeFromQueue(channel, queueName, callbackEvent);
			}
		});
};