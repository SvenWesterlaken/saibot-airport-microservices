let queue;
let Employee = require('../../models/employee.model');

module.exports.init = (queueName) => {
	queue = queueName;
};

module.exports.messageReceivedEvent = (message) => {
	console.log(' [x] Employee worker message: ' + message);
	let jsonMessage = JSON.parse(message);
	let data = jsonMessage.data;
	
	switch (jsonMessage.type) {
		case 'CREATE':
			Employee.create(data)
				.then((employee) => {
					console.log('New employee added successfully:');
					console.log(employee);
				}).catch((error) => console.log('Error: ' + error));
			break;
			
		case 'UPDATE':
			//TODO UPDATE
			break;
			
		case 'DELETE':
			//TODO DELETE
			break;
	}
}