import { FastifyInstance } from 'fastify';
import DiscordClient from '../services/discord';
import { DiscordAPIError } from 'discord.js';

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

    fastify.route({
        method: 'POST',
        url: '/add-roles',
        schema: {
            body: {
                $ref: 'RoleController.user-role'
            }
        },
        handler: async (request, reply) => {
            try {
                const {role_ids, guild_id, user_id} = request.body;

                const guild = DiscordClient.guilds.resolve(guild_id);
                if (!guild) return reply.status(400).send({error: 'GuildNotFound'});
                const member = guild.members.resolve(user_id);
                if (!member) return reply.status(400).send({error: 'MemberNotFound'});
                member.roles.add(role_ids);

                reply.send({ data: true });
            } catch (e) {
                if (e instanceof DiscordAPIError) {
                    reply.status(400).send({error: 'DiscordAPIError'});
                    e.code
                    // TODO: find admin channel and send error

                    return;
                }
                reply.status(500).send({error: 'InternalServerError'});
                throw e;
            }
        }
    });

    fastify.route({
        method: 'POST',
        url: '/remove-roles',
        schema: {
            body: {
                $ref: 'RoleController.user-role'
            }
        },
        handler: async (request, reply) => {
            try {
                const {role_ids, guild_id, user_id} = request.body;

                const guild = DiscordClient.guilds.resolve(guild_id);
                if (!guild) return reply.status(400).send({error: 'GuildNotFound'});
                const member = guild.members.resolve(user_id);
                if (!member) return reply.status(400).send({error: 'MemberNotFound'});
                member.roles.remove(role_ids);

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
    });
}