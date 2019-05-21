const amqpManager = require('../amqp.manager');

module.exports.init = function (queueName, topicKey, callbackEvent) {
	console.log('Init ' + queueName);
	
	if (amqpManager.channel != null){
		return consume(amqpManager.channel, queueName, topicKey, callbackEvent)
	}else {
		return consume(amqpManager.connectRmq(), queueName, topicKey, callbackEvent)
	}
};

function consume (channel, queueName, key, callbackEvent) {
	try {
		console.log("trying to consume from queue...");
		return amqpManager.consumeFromQueue(channel, queueName, key, callbackEvent);
	} catch (error) {
		console.log("Unable to consume from queue");
	}
}