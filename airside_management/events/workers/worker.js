const amqpManager = require('../amqp.manager');

module.exports.init = function (queueName, callbackEvent) {
	if (amqpManager.channel != null){
		return consume(amqpManager.channel, queueName, callbackEvent)
	}else {
		return consume(amqpManager.connectRmq(), queueName, callbackEvent)
	}
};

function consume (channel, queueName, callbackEvent) {
	try {
		console.log("trying to consume from queue...");
		return amqpManager.consumeFromQueue(channel, queueName, callbackEvent);
	} catch (error) {
		console.log("Unable to consume from queue");
	}
}