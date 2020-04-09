import { FastifyInstance } from 'fastify';
import { M2M_SECRET } from '../config';
import { v4 as uuidv4 } from 'uuid';

export default async function(fastify: FastifyInstance): Promise<void> {
    fastify.addSchema({
        $id: 'common.json',
        type: 'object',
        properties: {
            snowflake: {
                type: 'string',
                minLength: 16,
                maxLength: 20,
                pattern: '^\\d+$'
            }
        }
    });

    // request tracing
    fastify.addHook('onRequest', async (request, reply) => {
        reply.headers({
            'x-request-id': uuidv4()
        });
    });

    fastify.addHook('onRequest', async (request, reply) => {
        // good enough(tm) security for now
        if (request.headers['authorization'] !== `Bearer srv.${M2M_SECRET}`) {
            return reply.code(401).send({
                error: "NotAuthorized"
            });
        }
        return
    });
}