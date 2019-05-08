const express = require('express');
const parser = require('body-parser');
const workerManager = require('./events/worker.manager');

require('dotenv').config();

const app = express();

workerManager.init();

app.use(parser.json());
app.use(parser.urlencoded({extended:true}));

app.set('port', (process.env.API_PORT || 8181));

app.use('/api/v1', require('./routes/v1/api.v1'));

app.use((err, req, res, next) => {
	let error = {
		message: err.message,
		code: err.code,
		name: err.name,
		status: err.status
	};
	
	res.status(401).json(error);
});

app.use('*', (req, res) => {
	res.status(400).json({'error': 'Invalid URL.'});
});

app.listen(app.get('port'), () => {
	console.log('Application started on port ' + app.get('port'));
});