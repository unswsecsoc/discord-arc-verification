export interface APIBaseResponse {
  error?: string;
}

export interface ClubResponse extends APIBaseResponse {
  _id: string;
  description: string;
  email: string;
  name: string;
  permalink: string;
  website: string;
  is_enabled: boolean;
}

export interface RetrieveVerificationResponse extends APIBaseResponse  {
  user_verified: boolean;
  club: ClubResponse;
}