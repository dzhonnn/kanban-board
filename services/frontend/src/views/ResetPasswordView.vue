<template>
    <section>
        <form @submit.prevent="submit">
            <div class="mb-3">
                <label for="password" class="form-label">New password:</label>
                <input type="password" @onchange.prevent="validatePassword()" name="password" v-model="form.new_password" class="form-control" id="password" required>
                <br>
                <label for="password" class="form-label">Confirm new password:</label>
                <input type="password" @onkeyup.prevent="validatePassword()" name="password" class="form-control" id="confirm_password" required>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </section>
</template>

<script>
import { defineComponent } from 'vue';
import { mapActions } from 'vuex';

export default defineComponent({
    name: "Reset",
    data() {
        return {
            form: {
                new_password: "",
                access_token: this.$route.query.access_token
            }
        }
    },
    methods: {
        ...mapActions(["resetPass"]),
        async submit() {
            await this.resetPass(this.form)
            alert(`Password reseted`)
            this.$router.push("/login")
        },
        validatePassword() {
            let password = this.$el.querySelector('#password')
            let confirm_password = this.$el.querySelector('#confirm_password')
            if (password.value != confirm_password.value) {
                confirm_password.setCustomValidity('Password does not match.')
            } else {
                confirm_password.setCustomValidity('')
            }
        }
    }
})
</script>