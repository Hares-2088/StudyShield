<template>
  <div class="login-container bg-[#bde0fe] p-6 rounded-lg shadow-lg max-w-md mx-auto">
    <h2 class="text-2xl font-bold text-[#cdb4db] mb-4">Login</h2>
    <form @submit.prevent="handleLogin" class="space-y-4">
      <div class="form-group">
        <label for="email" class="block text-[#a2d2ff] font-medium">Email</label>
        <input v-model="email" type="email" id="email" required
          class="w-full px-4 py-2 border border-[#ffc8dd] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ffafcc]" />
      </div>
      <div class="form-group">
        <label for="password" class="block text-[#a2d2ff] font-medium">Password</label>
        <input v-model="password" type="password" id="password" required
          class="w-full px-4 py-2 border border-[#ffc8dd] rounded-lg focus:outline-none focus:ring-2 focus:ring-[#ffafcc]" />
      </div>
      <button type="submit" :disabled="loading"
        class="w-full bg-gradient-to-r from-[#ffc8dd] to-[#cdb4db] text-white py-2 rounded-lg hover:from-[#ffc8dd]/90 hover:to-[#cdb4db]/90 transition-all duration-300 shadow-md">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>
      <p v-if="error" class="error text-[#ffafcc] text-sm mt-2">{{ error }}</p>
    </form>
    <p class="text-sm text-[#a2d2ff] mt-4">
      Don't have an account? <router-link to="/register" class="text-[#ffafcc] underline">Register here</router-link>
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/api/authService';

export default defineComponent({
  setup() {
    const { login, isAuthenticated } = useAuth();
    const router = useRouter();

    const email = ref('');
    const password = ref('');
    const loading = ref(false);
    const error = ref('');

    const handleLogin = async () => {
      loading.value = true;
      error.value = '';

      try {
        const success = await login(email.value, password.value);
        if (success) {
          router.push('/dashboard');
        } else {
          error.value = 'Invalid email or password';
        }
      } catch (err) {
        error.value = 'Login failed. Please try again.';
      } finally {
        loading.value = false;
      }
    };

    return {
      email,
      password,
      loading,
      error,
      handleLogin
    };
  }
});
</script>

<style scoped>
.login-container {
  margin-top: 50px;
}

.error {
  color: red;
}
</style>