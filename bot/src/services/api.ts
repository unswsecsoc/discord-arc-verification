import axios, { AxiosResponse } from 'axios';
import { APIResponse, NewVerification, Club } from '../lib/api_schemas';
import { API_URL, M2M_SECRET } from '../config';
import { setupCache } from 'axios-cache-adapter';

export class APIError extends Error {
    constructor(public code: APIErrorMessage) {
        super(code);

        Object.setPrototypeOf(this, APIError.prototype);
    }
}
export enum APIErrorMessage {
    BannedVerification = "BannedVerification",
    AlreadyVerified = "AlreadyVerified",
}

// 5 second cache should be plenty
const cache = setupCache({
    maxAge: 5000
});

const client = axios.create({
    baseURL: API_URL,
    timeout: 2000,
    headers: {
        authorization: `Bearer srv.${M2M_SECRET}`
    },
    adapter: cache.adapter
});


export async function createVerification(user_id: string, guild_id: string): Promise<NewVerification> {
    try { 
        const response: AxiosResponse<APIResponse<NewVerification>> = await client.post('/priv/verifications', {
            user_id,
            guild_id
        });
        return response.data.data;
    } catch (e) {
        if (e.response.status === 404) return null;
        if (e.response.data.error) throw new APIError(e.response.data.error);
        throw(e);
    }
}

export async function getClub(guildId: string): Promise<Club> {
    try { 
        const response: AxiosResponse<APIResponse<Club>> = await client.get(`/priv/clubs_by_guild/${guildId}`);
        return response.data.data;
    } catch (e) {
        if (e.response.status === 404) return null;
        if (e.response.data.error) throw new APIError(e.response.data.error);
        throw(e);
    }
}

export async function updateClub(guildId: string, key: string, value: (string|number|boolean)): Promise<void> {
    try { 
        await client.put(`/priv/clubs_by_guild/${guildId}`, {
            key,
            value
        });
        return;
    } catch (e) {
        if (e.response.status === 404) return null;
        if (e.response.data.error) throw new APIError(e.response.data.error);
        throw(e);
    }
}