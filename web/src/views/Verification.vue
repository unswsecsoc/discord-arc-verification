<template>
  <div v-if="!loaded" class="container">
    <section class="hero">
      <div class="hero-body">
        <div class="container">
          <article v-if="error" class="message is-danger">
            <div class="message-body">
              <b>Error:</b> Server returned: {{error}}
            </div>
          </article>
          <h1 v-else class="title is-1">Loading data...</h1>
        </div>
      </div>
    </section>
  </div>
  <div v-else>
    <section class="hero">
      <div class="hero-body">
        <div class="container">
          <h1 class="title is-1">Account Verification Form</h1>
          <article v-if="error" class="message is-danger">
            <div class="message-body">
              <b>Error:</b> Server returned: {{error}}
            </div>
          </article>
        </div>
      </div>
    </section>

    <div class="container" v-if="submitted">
      <p v-if="userVerified">
        You have been successfully verified. Just close this window and enjoy your new privileges
        on the server.
      </p>
      <p v-else>
        Please check your email for further instructions. If there's an issue, please contact the
        server admin.
      </p>
    </div>
    <div v-else>
      <div class="container" v-if="userVerified">
        Looks like you've done this before, so no need to fill out your details again!
      </div>
      <form class="container" v-else>
        <b-field label="Given Name" required>
          <b-input v-model="givenName"></b-input>
        </b-field>
        <b-field label="Family Name">
          <b-input v-model="familyName"></b-input>
        </b-field>

        <b-field label="Are you a student/staff of UNSW?">
          <b-switch v-model="unswMember">
            {{ unswMember ? 'Yes' : 'No' }}
          </b-switch>
        </b-field>

        <b-field label="Are you an ARC member?" v-if="unswMember">
          <b-switch v-model="arcMember">
            {{ arcMember ? 'Yes' : 'No' }}
          </b-switch>
        </b-field>
        <b-field label="zID" v-if="unswMember">
          <b-input v-model="zid"></b-input>
        </b-field>

        <b-field label="Email Address" v-if="!unswMember">
          <b-input type="email" v-model="email"></b-input>
        </b-field>

        <b-field label="Phone Number" v-if="!unswMember">
          <b-input type="phone" v-model="phone"></b-input>
        </b-field>
      </form>
      <br />
      <div class="container">
        <h2 class="title is-2">Declaration</h2>
        <p>
          By clicking submit, I am granting <b>{{ clubName }}</b> access to my personal data in accordance with <a href="https://www.arc.unsw.edu.au/privacy-policy">ARC's privacy policy</a>
          for the purpose of verifying my identity.
        </p>
        <b-button type="is-success" v-on:click="submit" :disabled="submitting" expanded>
          Submit
        </b-button>
      </div>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import API from '../api';
import { RetrieveVerificationResponse } from '../api/responses';


export default Vue.extend({
  data: () => ({
    loaded: false,
    error: '',
    submitting: false,
    submitted: false,
    token: '',

    userVerified: false,
    clubName: '',
    givenName: '',
    familyName: '',
    unswMember: true,
    arcMember: true,
    zid: '',
    email: '',
    phone: '',
  }),
  mounted() {
    this.token = this.$route.params.token;
    API.getVerification(this.$route.params.token)
      .then((data) => {
        if (data.error) {
          this.loaded = false;
          this.error = data.error;
          return;
        }
        this.loaded = true;
        this.userVerified = data.user_verified;
        this.clubName = data.club.name;
      });
  },
  methods: {
    submit() {
      this.submitting = true;
      setTimeout(() => { this.submitting = false; }, 5000);
      API.postVerification(this.token, !this.userVerified ? {
        given_name: this.givenName,
        family_name: this.familyName,
        arc_member: this.arcMember,
        zid: this.unswMember ? this.zid : undefined,
        email: !this.unswMember ? this.email : undefined,
        phone: !this.unswMember ? this.phone : undefined,
      } : undefined).then((data) => {
        if (!data.error) {
          this.error = '';
          this.submitted = true;
          this.userVerified = data.user_verified;
        } else {
          this.error = data.error;
        }
      });
    },
  },
});
</script>
