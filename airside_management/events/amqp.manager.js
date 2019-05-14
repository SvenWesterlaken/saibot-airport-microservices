const amqp = require('amqplib');
const workerManager = require('./worker.manager');

// amount of tries reconnecting
let count = 0;
// existing channel is used when available
let channel = null;
// no need for multiple reconnect attempts at the same time
let reconnecting = false;
// delay for reconnecting attempts in ms
let iVal = 5000;

const delay = ms => new Promise(res => setTimeout(res, ms));

const reconnect = function (){
	reconnecting = true;
	channel = null;
	count+=1;
	console.log("reconnecting #" + count);
	delay(iVal)
		.then(() => {
			module.exports.connectRmq();
		});
};

module.exports = {
	connectRmq() {
		reconnecting = false;
		return amqp.connect('amqp://rabbitmq')
			.then((conn) => {
				conn.on('error', () => {if(!reconnecting) reconnect.bind(this)});
				conn.on("close", (err) => {
					if (err) {
						 return reconnecting ? null : reconnect();
					}
				});
				if (conn != null) {
					channel = conn.createChannel();
					reconnecting = false;
					if (count > 0){
						count = 0;
						workerManager.init();
					}
					return channel;
				} else {
					return reconnecting ? null : reconnect();
				}
			}, function connectionFailed() {
				return reconnecting ? null : reconnect();
			}).catch(() => {
				return reconnecting ? null : reconnect();
			})
	},
	channel,
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