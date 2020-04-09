import { Message } from "discord.js";

export interface Handler {
    (arg: string, ctx: Message): void;
    help?: {
        guild?: string;
        user?: string;
    };
}

export enum DiscordObjectType {
    USER = 'user',
    GUILD = 'guild',
}

