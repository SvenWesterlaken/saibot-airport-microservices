const amqpManager = require('../amqp.manager');
let channel = null;

module.exports.init = function (queueName, topicKey, callbackEvent) {
	// reusing connection/channel not implemented
	// channel = amqpManager.channel;
	// if (channel != null) {
	// 	return consume (channel, queueName, callbackEvent)
	// }
	amqpManager.connectRmq().then((ch) => {
		// amqpManager.channel = ch;
		// channel = ch
		return consume(ch, queueName, topicKey, callbackEvent)
	});
};

function consume (channel, queueName, key, callbackEvent) {
	try {
		return amqpManager.consumeFromQueue(channel, queueName, key, callbackEvent);
	} catch {
		channel = null;
		console.log("Unable to consume from queue");
	}
}