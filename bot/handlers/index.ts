import { IHandler } from '../types';
import * as VerificationHandler from './verification';
import HelpHandler from './help';

const handlers: {[key: string]: IHandler} = {
    'verify': VerificationHandler.initFromGuild,
    'avhelp': HelpHandler
}

export default handlers;
export const MAX_LENGTH = Math.max(...Object.keys(handlers).map((i => i.length))) + 2;