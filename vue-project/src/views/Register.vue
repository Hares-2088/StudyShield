<template>
    <div class="register-container bg-[#bde0fe] p-6 rounded-lg shadow-lg max-w-md mx-auto">
        <h2 class="text-2xl font-bold text-[#cdb4db] mb-4">Register</h2>
        <form @submit.prevent="handleRegister" class="space-y-4">
            <div class="form-group">
                <label for="name" class="block text-[#a2d2ff] font-medium">Name</label>
                <input v-model="name" type="text" id="name" placeholder="Your name" required
                    class="w-full px-4 py-2 border border-[#ffc8dd] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ffafcc] text-black" />
            </div>
            <div class="form-group">
                <label for="email" class="block text-[#a2d2ff] font-medium">Email</label>
                <input v-model="email" type="email" id="email" required
                    class="w-full px-4 py-2 border border-[#ffc8dd] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ffafcc] text-black" />
            </div>
            <div class="form-group">
                <label for="password" class="block text-[#a2d2ff] font-medium">Password</label>
                <input v-model="password" type="password" id="password" required
                    class="w-full px-4 py-2 border border-[#ffc8dd] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ffafcc] text-black" />
            </div>
            <button type="submit" :disabled="loading"
                class="w-full bg-gradient-to-r from-[#ffc8dd] to-[#cdb4db] text-white py-2 rounded-lg hover:from-[#ffc8dd]/90 hover:to-[#cdb4db]/90 transition-all duration-300 shadow-md">
                {{ loading ? 'Registering...' : 'Register' }}
            </button>
            <p v-if="error" class="error text-[#ffafcc] text-sm mt-2">{{ error }}</p>
            <p v-if="success" class="success text-[#a2d2ff] text-sm mt-2">Registration successful! You can now login.
            </p>
        </form>
        <p class="text-sm text-[#a2d2ff] mt-4">
            Already have an account? <router-link to="/login" class="text-[#ffafcc] underline">Login here</router-link>
        </p>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/api/authService';

export default defineComponent({
    setup() {
        const { register, login } = useAuth();
        const router = useRouter();

        const name = ref('');
        const email = ref('');
        const password = ref('');
        const loading = ref(false);
        const error = ref('');
        const success = ref(false);

        const handleRegister = async () => {
            loading.value = true;
            error.value = '';
            success.value = false;

            try {
                await register({
                    name: name.value,
                    email: email.value,
                    password: password.value
                });
                await login(email.value, password.value); // Automatically log in the user
                router.push('/dashboard'); // Redirect to the dashboard
            } catch (err: any) {
                error.value = 'Registration failed: ' + (err.response?.data?.detail || err.message);
            } finally {
                loading.value = false;
            }
        };

        return {
            name,
            email,
            password,
            loading,
            error,
            success,
            handleRegister
        };
    }
});
</script>

<style scoped>
.register-container {
    margin-top: 50px;
}

.error {
    color: red;
}

.success {
    color: green;
}

/* Ensure text color is visible in input fields */
input {
    color: black;
}
</style>