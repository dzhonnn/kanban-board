<template>
    <section>
        <form @submit.prevent="submit">
            <div class="mb-3">
                <label for="email" class="form-label">Email:</label>
                <input type="email" name="email" v-model="form.email" class="form-control" required>
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
                email: '',
            }
        }
    },
    methods: {
        ...mapActions(["reset"]),
        async submit() {
            await this.reset(this.form.email)
            alert(`Reset message sended on mail: ${this.form.email}`)
        }
    }
})
</script>