const amqp = require('amqplib');

module.exports = {
	connect() {
		return amqp.connect('amqp://rabbitmq')
			.then((conn) => {
				if (conn != undefined) {
					return conn.createChannel();
				} else {
					throw "Dit ging fout";
				}
			});
	},
	
	sendMessageToQueue(channel, queueName, message) {
		channel.assertQueue(queueName, {
			durable: false
		}).then(() => {
			//Queue OK
			channel.sendToQueue(queueName, Buffer.from(message));
			
			console.log(" [x] Sent %s", message);
		}).catch((error) => {
			console.log('QUEUE ERROR PRODUCER');
		});
	},
	
	consumeFromQueue(channel, queueName, callback) {
		channel.assertQueue(queueName, {
			durable: false
		}).then(() => {
			//Queue OK
			console.log('Worker for queue ' + queueName + ' started! Listening for messages...');
			
			channel.consume(queueName, function(message) {
				callback(message.content.toString());
			}, {
				noAck: true
			});
		}).catch((error) => {
			console.log('QUEUE ERROR WORKER');
		});
	}
};