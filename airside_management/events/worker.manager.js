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
	return fuelWorker.init('airside-fuel', fuelWorkerCallback.messageReceivedEvent)
	console.log('Worker Fuel started.');
}

function runwayWorkerInit() {
	return runwayWorker.init('airside-runway', runwayWorkerCallback.messageReceivedEvent)
	console.log('Worker Runway started.');
}

function taxiwayWorkerInit() {
	return taxiwayWorker.init('airside-taxiway', taxiwayWorkerCallback.messageReceivedEvent)
	console.log('Worker Taxiway started.');
}