const amqp = require('amqplib');
const workerManager = require('./worker.manager');

const Fuel = require('../models/fuel.model');
const RmqFuel = Fuel.rmq;

// amount of tries reconnecting
let count = 0;
// existing channel is used when available (not implemented yet)
let channel = null;
// no need for multiple reconnect attempts at the same time
let reconnecting = false;
// delay for reconnecting attempts in ms
let iVal = 5000;

let exchange = 'events';

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

function restoreEvents() {
	module.exports.connectRmq().then((ch) => {
		console.log("Restoring events...");
		RmqFuel.find({})
			.then((containers) => {
				containers.forEach((container) => {
						module.exports.sendMessageToQueue(ch, 'airside-fuel', JSON.stringify(container));
						RmqFuel.findOneAndDelete({_id: container._id})
							.catch((error) => {
								console.log(error);
							})
						})
		})
			.catch((error) => {
				console.log(error)
			});
		console.log("Restoring events completed!");
		})

}

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
					if (!reconnecting) {
						reconnecting = false;

						// check if connection was lost (count will increase by 1 for each attempt to reconnect)
						// if so, we restart the workers and restore events (send to rabbitmq)
						if (count > 0) {
							count = 0;
							workerManager.init();
							delay(iVal)
								.then(() => {
									restoreEvents();
								});
						}
					}
					return conn.createChannel();
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
	sendMessageToQueue(channel, key, message) {
		channel.assertExchange(exchange, 'topic', {
			durable: true
		}).then(() => {
			//Exchange OK
			channel.publish(exchange, key, Buffer.from(message), {deliveryMode: 2});
			
			console.log(" [x] Sent %s", message);
		}).catch((error) => {
			console.log('QUEUE ERROR PRODUCER');
		});
		//
		// channel.assertQueue(queueName, {
		// 	durable: true
		// }).then(() => {
		// 	//Queue OK
		// 	channel.sendToQueue(queueName, Buffer.from(message), {deliveryMode: 2});
		//
		// 	console.log(" [x] Sent %s", message);
		// }).catch((error) => {
		// 	console.log('QUEUE ERROR PRODUCER');
		// });
	},
	
	consumeFromQueue(channel, queueName, key, callback) {
		channel.assertExchange(exchange, 'topic', {
			durable: true
		});
		
		channel.assertQueue(queueName, {
			durable: true
		}).then((queue) => {
			//Queue OK
			channel.bindQueue(queue.queue, exchange, key);
			
			console.log('Worker for queue ' + queueName + ' started! Listening for messages...');

			channel.consume(queue.queue, function(message) {
				callback(message.content.toString());
			}, {
				noAck: true
			});
		}).catch((error) => {
			console.log('QUEUE ERROR WORKER');
		});
	}
};