export interface APIResponse<T> {
    data?: T;
    error?: string;
}

export interface NewVerification {
    url: string;
    expires: number;
}

export interface Club {
    _id: string;
    name: string;
    permalink: string;
    description: string;
    email: string;
    website: string;
    admin_channel_id: string;
    admin_role_id: string;
    verified_role_id: string;
    discord_id: string;
    is_enabled: boolean;
    deleted_at: number;

    _expires?: string;
}

export interface User {
    _id: string;
    given_name: string;
    family_name: string;
    email: string;
    phone: string;
    zid: string;
    arc_member: string;
    is_verified: string;
    discord_id: string;
    created_at: number;
    updated_at: number;
    deleted_at: number;
    guilds: string[];
}