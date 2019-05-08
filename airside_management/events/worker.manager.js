const fuelWorker = require('./workers/worker');
const fuelWorkerCallback = require('./workers/fuel.worker');

const runwayWorker = require('./workers/worker');
const runwayWorkerCallback = require('./workers/runway.worker');

const taxiwayWorker = require('./workers/worker');
const taxiwayWorkerCallback = require('./workers/taxiway.worker');

module.exports.init = () => {
	fuelWorkerCallback.init('airside-fuel');
	runwayWorkerCallback.init('airside-runway');
	taxiwayWorkerCallback.init('airside-taxiway');
	
	fuelWorker.init('airside-fuel', fuelWorkerCallback.messageReceivedEvent);
	runwayWorker.init('airside-runway', runwayWorkerCallback.messageReceivedEvent);
	taxiwayWorker.init('airside-taxiway', taxiwayWorkerCallback.messageReceivedEvent);
};