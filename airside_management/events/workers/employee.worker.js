let queue;
let Employee = require('../../models/employee.model');

module.exports.init = (queueName) => {
	queue = queueName;
};

module.exports.messageReceivedEvent = (message) => {
	console.log(' [x] Employee worker message: ' + message);
	let jsonMessage = JSON.parse(message);
	let data = jsonMessage.data;
	let oldData = jsonMessage.old_data;
	
	switch (jsonMessage.type) {
		case 'CREATE':
			Employee.create(data)
				.then((employee) => {
					console.log('New employee added successfully:');
					console.log(employee);
				}).catch((error) => console.log('Error: ' + error));
			break;
			
		case 'PATCH':
			Employee.findOne({_id: data._id})
				.then((employee) => {
					if (data.first_name)
						employee.first_name = data.first_name;
					
					if (data.last_name)
						employee.last_name = data.last_name;
					
					employee.save()
						.then((updatedEmployee) => {
							console.log('Employee updated successfully:');
							console.log(updatedEmployee);
						}).catch((error) => console.log('Error: ' + error));
				}).catch((error) => console.log('Error: ' + error));
			break;
			
		case 'DELETE':
			Employee.findOneAndDelete({_id: oldData._id})
				.then((employee) => {
					console.log('Employee deleted successfully.');
				}).catch((error) => console.log('Error: ' + error));
			break;
	}
};