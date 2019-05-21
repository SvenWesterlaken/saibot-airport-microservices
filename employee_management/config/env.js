const env = {
	dbPort: process.env.DB_PORT || '27017',
	dbHost: process.env.DB_HOST || 'mongo_employee_management',
	dbUser: process.env.DB_USER || '',
	dbPassword: process.env.DB_PASSWORD || '',
	dbDatabase: process.env.DB_DATABASE || 'saibot-employee',
	allowOrigin: process.env.ALLOW_ORIGIN || '*'
};

env.dbUrl = `mongodb://${env.dbHost}:${env.dbPort}/${env.dbDatabase}`;

module.exports = env;