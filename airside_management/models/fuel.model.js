const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const FuelSchema = new Schema({
	fuel_level: {
		type: Number,
		required: true
	},
	fuel_capacity: {
		type: Number,
		required: true
	}
}, {
	timestamps: true
});

const Fuel = mongoose.model('fuel', FuelSchema);

module.exports = Fuel;