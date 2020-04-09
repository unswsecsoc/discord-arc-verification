import { FastifyInstance,  } from 'fastify';
import DiscordClient from '../services/discord';
import { DiscordAPIError } from 'discord.js';
import fastify = require('fastify');
import { ServerResponse } from 'http';

export default async function (fastify: FastifyInstance): Promise<void> {

    fastify.addSchema({
        $id: 'RoleController.user-role',
        type: 'object',
        properties: {
            user_id: {
                $ref: 'common.json#/properties/snowflake'
            },
            guild_id: {
                $ref: 'common.json#/properties/snowflake'
            },
            role_ids: { 
                type: 'array',
                items: {
                    $ref: 'common.json#/properties/snowflake'
                }
            }
        },
        required: ['user_id', 'role_ids']
    });

    function addRemoveRole(action: boolean) {
        return async (request: fastify.FastifyRequest, reply: fastify.FastifyReply<ServerResponse>) => {
            const {role_ids, guild_id, user_id} = request.body;

            const guild = DiscordClient.guilds.resolve(guild_id);
            if (!guild) return reply.status(400).send({error: 'GuildNotFound'});
            const member = guild.members.resolve(user_id);
            if (!member) return reply.status(400).send({error: 'MemberNotFound'});

            try {
                if (action) member.roles.add(role_ids);
                else member.roles.remove(role_ids);
                reply.send({ data: true });
            } catch (e) {
                if (e instanceof DiscordAPIError) {
                    reply.status(400).send({error: 'DiscordAPIError'});
                    
                    // TODO: find admin channel and send error if error == 50013
                    return;
                }
                reply.status(500).send({error: 'InternalServerError'});
                throw e;
            }
        }
    }

    fastify.route({
        method: 'POST',
        url: '/add-roles',
        schema: {
            body: {
                $ref: 'RoleController.user-role'
            }
        },
        handler: addRemoveRole(true)
    });

    fastify.route({
        method: 'POST',
        url: '/remove-roles',
        schema: {
            body: {
                $ref: 'RoleController.user-role'
            }
        },
        handler: addRemoveRole(false)
    });
}