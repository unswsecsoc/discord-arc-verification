export interface APIResponse<T> {
    data?: T;
    error?: string;
}

export interface NewVerification {
    url: string;
    expires: number;
}