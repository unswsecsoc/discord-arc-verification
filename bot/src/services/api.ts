import axios, { AxiosResponse } from 'axios';
import { APIResponse, NewVerification } from '../lib/api_schemas';
import { API_URL, M2M_SECRET } from '../config';

export class APIError extends Error {}
export enum APIErrorMessages {
    BannedVerification,
    AlreadyVerified
}

const client = axios.create({
    url: API_URL,
    timeout: 2000,
    headers: {
        authorization: `Bearer m2m.${M2M_SECRET}`
    }
});

export async function createVerification(id: string, guild_id: string): Promise<NewVerification> {
    const response: AxiosResponse<APIResponse<NewVerification>> = await client.post('/verifications', {
        id,
        guild_id
    });
    if (response.data.error) throw new APIError(response.data.error);
    return response.data.data;
}