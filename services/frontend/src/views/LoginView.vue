<template>
    <section>
        <form @submit.prevent="submit">
            <div class="mb-3">
                <label for="email" class="form-label">Email:</label>
                <input type="email" name="email" v-model="form.email" class="form-control" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password:</label>
                <input type="password" name="Password" v-model="form.password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        <br>
        <a href="/reset">Forgot password?</a>
    </section>
</template>

<script>
import { defineComponent } from 'vue';
import { mapActions } from 'vuex';

export default defineComponent({
    name: "Login",
    data() {
        return {
            form: {
                email: '',
                password: ''
            }
        }
    },
    methods: {
        ...mapActions(["logIn"]),
        async submit() {
            await this.logIn(this.form)
            this.$router.push("/board")
        }
    }
})
</script>