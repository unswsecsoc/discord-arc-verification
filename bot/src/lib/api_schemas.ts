export interface APIResponse<T> {
    data?: T;
    error?: string;
}

export interface NewVerification {
    url: string;
    expires: number;
}

export interface Club {
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