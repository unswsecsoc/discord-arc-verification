import * as fastify from 'fastify';
import Roles from '../http_handlers/roles';
import Middleware from '../lib/middleware';


/*
 * Set up HTTP
 */
const server = fastify();

// add middleware
Middleware(server);

// Handlers
server.register(Roles);
server.listen(3000, '0.0.0.0');

console.log('HTTP endpoint listening on port 3000.');

export default server;
