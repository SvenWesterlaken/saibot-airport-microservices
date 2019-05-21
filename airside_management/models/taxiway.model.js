const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const TaxiwaySchema = new Schema({
    identifier: {
        type: String,
        required: true
    },
    from_point: {
        type: String,
        required: true
    },
    to_point: {
        type: String,
        required: true
    }
}, {
    timestamps: true
});

const Taxiway = mongoose.model('taxiway', TaxiwaySchema);

module.exports = Taxiway;