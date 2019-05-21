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

const RmqSchema = new Schema({
	id: String,
	message: String,
	from: String,
	type: String,
	old_data: FuelSchema,
	data: FuelSchema,
	key: String
});

const Fuel = mongoose.model('fuel', FuelSchema);
const RmqFuel = mongoose.model('rmqFuel', RmqSchema);

module.exports = Fuel;
module.exports.rmq =  RmqFuel;