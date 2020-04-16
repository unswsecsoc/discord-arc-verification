import axios, { AxiosInstance } from 'axios';
import { removeEmpty } from '@/lib';
import { RetrieveVerificationResponse } from './responses';
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
      family_name: data.family_name,
      arc_member: data.arc_member,
      zid: data.zid,
      email: data.email,
      phone: data.phone,
    };

    return this.axios.post(`/verifications/${token}`, { user: removeEmpty(user) })
      .then((res) => res.data.data as RetrieveVerificationResponse)
      .catch((err) => err.response.data as RetrieveVerificationResponse);
  }
}

export default new API();
