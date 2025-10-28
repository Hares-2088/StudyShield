<template>
  <div
    class="bg-white/70 backdrop-blur-md p-8 rounded-2xl shadow-xl max-w-md w-full animate-fadeIn center mx-auto mt-20">
    <h2 class="text-3xl font-extrabold text-pink-700 mb-6 text-center">Welcome Back</h2>
    <form @submit.prevent="handleLogin" class="space-y-6">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
        <div class="mt-1 relative">
          <span class="absolute inset-y-0 left-0 pl-3 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-pink-300" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12H8m0 0l4-4m-4 4l4 4" />
            </svg>
          </span>
          <input v-model="email" type="email" id="email" required placeholder="you@example.com"
            class="block w-full pl-10 pr-4 py-2 bg-white text-gray-900 placeholder-gray-400 border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent transition" />
        </div>
      </div>

      <div>
        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
        <div class="mt-1 relative">
          <span class="absolute inset-y-0 left-0 pl-3 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-pink-300" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 11c1.105 0 2 .895 2 2v2H10v-2c0-1.105.895-2 2-2z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4" />
              <rect width="12" height="8" x="6" y="11" rx="2" ry="2" />
            </svg>
          </span>
          <input v-model="password" type="password" id="password" required placeholder="••••••••"
            class="block w-full pl-10 pr-4 py-2 bg-white text-gray-900 placeholder-gray-400 border border-pink-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-transparent transition" />
        </div>
      </div>

      <button type="submit" :disabled="loading"
        class="w-full flex justify-center items-center bg-gradient-to-r from-pink-400 to-purple-400 text-white py-2 rounded-lg hover:from-pink-500 hover:to-purple-500 transition duration-300 shadow-md disabled:opacity-50 disabled:cursor-not-allowed">
        <span v-if="!loading">Login</span>
        <span v-else class="flex items-center">
          <svg class="animate-spin h-5 w-5 mr-2 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
          </svg>
          Logging in...
        </span>
      </button>

      <p v-if="error" class="text-center text-sm text-red-500 mt-2 flex items-center justify-center">
        <svg class="h-4 w-4 mr-1 text-red-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
          stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 8v4m0 4h.01M12 2a10 10 0 110 20 10 10 0 010-20z" />
        </svg>
        {{ error }}
      </p>

      <p class="text-center text-sm text-gray-600 mt-6">
        Don&apos;t have an account?
        <router-link to="/register" class="text-pink-500 hover:underline">
          Register here
        </router-link>
      </p>
    </form>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/api/authService';
import { useUserStore } from '@/stores/userStore';

const { login } = useAuth();
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
      // Check for active session after successful login
      const userStore = useUserStore();
      await userStore.checkForActiveSession();
      router.push('/dashboard');
    }
    else error.value = 'Invalid email or password';
  } catch {
    error.value = 'Login failed. Please try again.';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.5s ease-out;
}
</style>
