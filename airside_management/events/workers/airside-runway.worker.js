let queue;

module.exports.init = (queueName) => {
	queue = queueName;
};

module.exports.messageReceivedEvent = (message) => {
	console.log(' [x] Worker ' + queue + ' has received message: ' + message);
};