const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const EmployeeSchema = new Schema({
	first_name: {
		type: String,
		required: true
	},
	last_name: {
		type: String,
		required: true
	},
	dob: {
		type: Date,
		required: true
	}
}, {
	timestamps: true
});

const Employee = mongoose.model('employee', EmployeeSchema);

module.exports = Employee;