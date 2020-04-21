import axios, { AxiosInstance } from 'axios';
import { RetrieveVerificationResponse, APIBaseResponse } from './responses';
import { User } from './requests';


class API {
  private axios: AxiosInstance;

  constructor() {
    this.axios = axios.create({
      baseURL: '/api',
    });
  }

  getVerification(token: string) {
    return this.axios.get(`/verifications/${token}`)
      .then((res) => res.data.data as RetrieveVerificationResponse)
      .catch((err) => err.response.data as RetrieveVerificationResponse);
  }

  postVerification(token: string, data?: User) {
    if (!data) {
      return this.axios.post(`/verifications/${token}`, {})
        .then((res) => res.data.data as RetrieveVerificationResponse)
        .catch((err) => err.response.data as RetrieveVerificationResponse);
    }

    const user = {
      given_name: data.given_name,
      family_name: data.family_name || undefined,
      arc_member: data.arc_member,
      zid: data.zid || undefined,
      email: data.email || undefined,
      phone: data.phone || undefined,
    };

    return this.axios.post(`/verifications/${token}`, { user })
      .then((res) => res.data.data as RetrieveVerificationResponse)
      .catch((err) => err.response.data as RetrieveVerificationResponse);
  }

  postValidation(token: string) {
    return this.axios.post(`/validations/${token}`)
      .then((res) => res.data.data as APIBaseResponse)
      .catch((err) => err.response.data as APIBaseResponse);
  }
}

export default new API();
