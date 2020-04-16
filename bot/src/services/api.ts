import axios, { AxiosResponse } from 'axios';
import { APIResponse, NewVerification } from '../lib/api_schemas';
import { API_URL, M2M_SECRET } from '../config';

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

const client = axios.create({
    baseURL: API_URL,
    timeout: 2000,
    headers: {
        authorization: `Bearer srv.${M2M_SECRET}`
    }
});

export async function createVerification(user_id: string, guild_id: string): Promise<NewVerification> {
    try { 
        const response: AxiosResponse<APIResponse<NewVerification>> = await client.post('/priv/verifications', {
            user_id,
            guild_id
        });
        return response.data.data;
    } catch (e) {
        if (e.response.data.error) throw new APIError(e.response.data.error);
        throw(e);
    }

}