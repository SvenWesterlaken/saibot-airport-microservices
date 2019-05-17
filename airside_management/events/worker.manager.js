const fuelWorker = require('./workers/worker');
const fuelWorkerCallback = require('./workers/airside-fuel.worker');

const runwayWorker = require('./workers/worker');
const runwayWorkerCallback = require('./workers/airside-runway.worker');

const taxiwayWorker = require('./workers/worker');
const taxiwayWorkerCallback = require('./workers/airside-taxiway.worker');

module.exports.init = () => {
	fuelWorkerCallback.init('airside-fuel');
	runwayWorkerCallback.init('airside-runway');
	taxiwayWorkerCallback.init('airside-taxiway');
	
	fuelWorkerInit();
	runwayWorkerInit();
	taxiwayWorkerInit();
};

function fuelWorkerInit() {
	return fuelWorker.init('airside-fuel', 'fuel.create', fuelWorkerCallback.messageReceivedEvent);
}

function runwayWorkerInit() {
	return runwayWorker.init('airside-runway', 'runway.#', runwayWorkerCallback.messageReceivedEvent);
}

function taxiwayWorkerInit() {
	return taxiwayWorker.init('airside-taxiway', 'taxiway.#', taxiwayWorkerCallback.messageReceivedEvent);
}