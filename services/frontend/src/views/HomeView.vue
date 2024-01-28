<template>
  <section>
    <p>Home page.</p>

    <div v-if="isLoggedIn">
      <h2>Click <a href="/board">here</a> to view all notes</h2>
    </div>
    <div v-else>
      <h2><a href="/register">Register</a></h2>
      <h2> or </h2>
      <h2><a href="/login">Log In</a></h2>
    </div>
  </section>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: "HomeView",
  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isAuthenticated
    }
  }
})
</script>
