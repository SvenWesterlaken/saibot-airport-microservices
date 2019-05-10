const fuelWorker = require('./workers/worker');
const fuelWorkerCallback = require('./workers/airside-fuel.worker');

const runwayWorker = require('./workers/worker');
const runwayWorkerCallback = require('./workers/airside-runway.worker');

const taxiwayWorker = require('./workers/worker');
const taxiwayWorkerCallback = require('./workers/airside-taxiway.worker');

const delay = ms => new Promise(res => setTimeout(res, ms));

module.exports.init = () => {
	fuelWorkerCallback.init('airside-fuel');
	runwayWorkerCallback.init('airside-runway');
	taxiwayWorkerCallback.init('airside-taxiway');
	
	fuelWorkerInit();
	runwayWorkerInit();
	taxiwayWorkerInit();
};

function fuelWorkerInit() {
	console.log('Fuel worker started');
	return fuelWorker.init('airside-fuel', fuelWorkerCallback.messageReceivedEvent)
		.then(() => {
			console.log('Worker Fuel started.');
		})
		.catch((error) => {
			console.log('Worker Fuel error.');
			console.log(error);
			
			delay(10000)
				.then(() => {
					fuelWorkerInit();
				});
		});
}

function runwayWorkerInit() {
	return runwayWorker.init('airside-runway', runwayWorkerCallback.messageReceivedEvent)
		.then(() => {
			console.log('Worker Runway started.');
		})
		.catch((error) => {
			console.log('Worker Runway error.');
			console.log(error);
			
			delay(10000)
				.then(() => {
					runwayWorkerInit();
				});
		});
}

function taxiwayWorkerInit() {
	return taxiwayWorker.init('airside-taxiway', taxiwayWorkerCallback.messageReceivedEvent)
		.then(() => {
			console.log('Worker Taxiway started.');
		})
		.catch((error) => {
			console.log('Worker Taxiway error.');
			console.log(error);
			
			delay(5000)
				.then(() => {
					taxiwayWorkerInit();
				});
		});
}