const amqp = require('amqplib');
const workerManager = require('./worker.manager');

const Fuel = require('../models/fuel.model');
const RmqFuel = Fuel.rmq;

// amount of tries reconnecting
let count = 0;

let conn = null;
// no need for multiple reconnect attempts at the same time
let reconnecting = false;
// delay for reconnecting attempts in ms
let iVal = 5000;

let exchange = 'events';

const delay = ms => new Promise(res => setTimeout(res, ms));

const reconnect = function (){
	reconnecting = true;
	module.exports.channel = null;
	count+=1;
	console.log("reconnecting #" + count);
	delay(iVal)
		.then(() => {
			module.exports.connectRmq();
		});
};

function restoreEvents() {
	console.log("Restoring events...");
	RmqFuel.find({})
		.then((objs) => {
			// if any, create new connection
			if (objs.length > 0) {
				if (conn != null) {
					console.log('Creating separate channel for restoration...');

					// confirm channel to receive ack for deleting (temporary) saved events
					conn.createConfirmChannel().then((ch) => {
						objs.forEach((obj) => {
							ch.publish(exchange, obj.key, Buffer.from(JSON.stringify(obj)), {}, function(err, ok) {
								if (err !== null) console.warn('Message nacked!');
								else {
									console.log("Successfully restored event");
									RmqFuel.findOneAndDelete({_id: obj._id})
										.catch((error) => {
											console.log(error);
										})
								}
							});
						});
						ch.waitForConfirms().then(() => {
							ch.close();
							console.log("Restoring events completed! -- channel closed");
						}).catch(() => {
							ch.close();
							console.warn("Message(s) nacked -- channel closed");
						});
					})
				}
			} else {
				console.log("No events available to restore");
			}
		})
		.catch((error) => {
			console.log(error)
		});
}

function createChannel() {
	if (conn != null) {
		if (module.exports.channel != null && !module.exports.channel.connection.closed) {
			console.log("Using existing channel...");
			return channel;
		} else {
			module.exports.channel = null;
			conn.createChannel().then((ch) => {
				console.log("Creating new channel...");
				module.exports.channel = ch;
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
			return module.exports.channel;
		});}
	} else {
		return reconnecting ? null : reconnect();
	}
}
module.exports = {
	connectRmq() {
		reconnecting = false;

		if (conn != null) {
			console.log("Using existing connection...");
			return createChannel();
		} else {
			console.log("Creating new connection...");
			amqp.connect('amqp://rabbitmq')
				.then((c) => {
					conn = c;
					conn.on('error', () => {
						conn = null;
						if(!reconnecting) reconnect.bind(this)});
					conn.on("close", (err) => {
						conn = null;
						if (err) {
							return reconnecting ? null : reconnect();
						}
					});
					return createChannel();
			}, function connectionFailed() {
					conn = null;
				return reconnecting ? null : reconnect();
			}).catch(() => {
				conn = null;
				return reconnecting ? null : reconnect();
			})
	}},
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
			channel.prefetch(1);
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