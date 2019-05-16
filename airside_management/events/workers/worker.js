const amqpManager = require('../amqp.manager');
let channel = null;

module.exports.init = function (queueName, callbackEvent) {
	channel = amqpManager.channel;
	if (channel != null) {
		return consume (channel, queueName, callbackEvent)
	}
	amqpManager.connectRmq().then((ch) => {
		amqpManager.channel = channel;
		return consume(ch, queueName, callbackEvent)
	});
};

function consume (channel, queueName, callbackEvent) {
	try {
		return amqpManager.consumeFromQueue(channel, queueName, callbackEvent);
	} catch {
		channel = null;
		console.log("Unable to consume from queue");
	}
}