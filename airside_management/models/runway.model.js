const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const RunwaySchema = new Schema({
	side1: {
		type: String,
		required: true
	},
	side2: {
		type: String,
		required: true
	},
	length: {
		type: Number,
		required: true
	},
	width: {
		type: Number,
		required: true
	}
}, {
	timestamps: true
});

const Runway = mongoose.model('runway', RunwaySchema);

module.exports = Runway;