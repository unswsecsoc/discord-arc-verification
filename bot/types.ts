import { Message } from "discord.js";

export interface IHandler {
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

