const express = require('express');
const parser = require('body-parser');
const mongodb = require('./config/mongodb');

require('dotenv').config();

const app = express();

app.use(parser.json());
app.use(parser.urlencoded({extended:true}));

app.set('port', (process.env.API_PORT || 8183));

mongodb.connect()
	.once('open', () => console.log('Connected to Mongo'))
	.on('error', (error) => console.warn('Warning', error.toString()));

app.use('/api/v1/employee', require('./routes/v1/employee.v1'));

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