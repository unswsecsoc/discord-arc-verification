<template>
  <div>
    <section class="hero">
      <div class="hero-body">
        <div class="container">
          <h1 class="title is-1">Account Verification Form</h1>
          <article v-if="error" class="message is-danger">
            <div class="message-body">
              <b>Error:</b> Server returned: {{error}}
            </div>
          </article>
          <article v-if="success" class="message is-success">
            <div class="message-body">
              <b>Success!</b> You have been verified!
            </div>
          </article>
        </div>
      </div>
    </section>

    <div v-if="!success">
      <div class="container">
        Please type in your verification token that was sent to you via email
      </div>
      <form class="container">
        <b-field label="One time token from email" required>
          <b-input v-model="token"></b-input>
        </b-field>
      </form>
      <br />
      <div class="container">
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


export default Vue.extend({
  data: () => ({
    error: '',
    submitting: false,
    success: false,
    token: '',
  }),
  methods: {
    submit() {
      this.submitting = true;
      setTimeout(() => { this.submitting = false; }, 5000);
      API.postValidation(this.token)
        .then((data) => {
          if (data.error) {
            this.error = data.error;
            this.submitting = false;
            return;
          }
          this.error = '';
          this.success = true;
        })
        .catch(() => {
          this.error = 'an unknown error occurred';
          this.submitting = false;
        });
    },
  },
});
</script>
