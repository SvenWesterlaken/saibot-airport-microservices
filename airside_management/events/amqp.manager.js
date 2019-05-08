const amqp = require('amqplib/callback_api');

module.exports.connect = () => {
	return new Promise((resolve, reject) => {
		amqp.connect('amqp://localhost', (err0, conn) => {
			if (err0) {
				console.log(err0);
				reject(err0);
			}
			
			conn.createChannel((err1, channel) => {
				if (err1) {
					console.log(err1);
					reject(err1);
				}
				
				resolve(channel);
			});
		});
	});
};

module.exports.sendMessageToQueue = function(channel, queueName, message) {
	channel.assertQueue(queueName, {
		durable: false
	});
	
	channel.sendToQueue(queueName, Buffer.from(message));
	
	console.log(" [x] Sent %s", message);
};

module.exports.consumeFromQueue = function(channel, queueName, callback) {
	channel.assertQueue(queueName, {
		durable: false
	});
	
	console.log('Worker for queue ' + queueName + ' started! Listening for messages...');
	
	channel.consume(queueName, function(message) {
		callback(message.content.toString());
	}, {
		noAck: true
	});
};