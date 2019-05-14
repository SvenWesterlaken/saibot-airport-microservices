const amqpManager = require('../amqp.manager');

module.exports.init = function (queueName, callbackEvent) {
	let channel = amqpManager.channel;
	if (channel != null) {
		return consume (channel, queueName, callbackEvent)
	}
	amqpManager.connectRmq().then((ch) => {
		return consume(ch, queueName, callbackEvent)
	});
};

function consume (channel, queueName, callbackEvent) {
	try {
		return amqpManager.consumeFromQueue(channel, queueName, callbackEvent);
	} catch {
		console.log("Unable to consume from queue");
	}
}