<template>
    <div>
        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-6">
            <!-- Removed Home Link -->
            <RouterLink v-if="isAuthenticated" to="/dashboard"
                class="hover:text-[#FFAFCC] transition-colors px-3 py-1 rounded-lg"
                active-class="text-white bg-[#FFAFCC]/90 shadow-md">
                Dashboard
            </RouterLink>
            <RouterLink v-if="isAuthenticated" to="/shop"
                class="hover:text-[#FFAFCC] transition-colors px-3 py-1 rounded-lg"
                active-class="text-white bg-[#FFAFCC]/90 shadow-md">
                Shop
            </RouterLink>
            <RouterLink v-if="isAuthenticated" to="/challenges"
                class="hover:text-[#FFAFCC] transition-colors px-3 py-1 rounded-lg"
                active-class="text-white bg-[#FFAFCC]/90 shadow-md">
                Challenges
            </RouterLink>

            <!-- Start Session Button -->
            <RouterLink v-if="isAuthenticated" to="/start-session"
                class="ml-auto bg-gradient-to-r from-[#FFC8DD] to-[#CDB4DB] text-white px-5 py-2 rounded-lg hover:from-[#FFC8DD]/90 hover:to-[#CDB4DB]/90 transition-all duration-300 shadow-lg hover:shadow-xl"
                active-class="from-[#FFC8DD]/90 to-[#CDB4DB]/90 shadow-xl">
                Start Session
            </RouterLink>

            <!-- Profile and Logout -->
            <div v-if="isAuthenticated" class="flex items-center space-x-4">
                <RouterLink to="/profile" class="hover:text-[#FFAFCC] transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M5.121 17.804A4 4 0 0112 15a4 4 0 016.879 2.804M15 11a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                </RouterLink>
                <button @click="logout" class="hover:text-[#FFAFCC] transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1m0-10V5" />
                    </svg>
                </button>
            </div>
        </div>

        <!-- Mobile Menu Button -->
        <button @click="$emit('toggle-menu')"
            class="md:hidden text-white focus:outline-none hover:text-[#FFAFCC] transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path v-if="!isMobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 6h16M4 12h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>

        <!-- Mobile Navigation -->
        <div v-if="isMobileMenuOpen"
            class="md:hidden mt-4 pb-4 space-y-3 max-w-7xl mx-auto bg-[#BDE0FE]/30 backdrop-blur-sm rounded-xl p-4 border border-[#CDB4DB]/50">
            <!-- Removed Home Link -->
            <RouterLink v-if="isAuthenticated" to="/dashboard"
                class="block hover:text-[#FFAFCC] transition-colors py-2 px-3 rounded-lg"
                active-class="text-white bg-[#FFAFCC]/90" @click="$emit('toggle-menu')">
                Dashboard
            </RouterLink>
            <RouterLink v-if="isAuthenticated" to="/shop"
                class="block hover:text-[#FFAFCC] transition-colors py-2 px-3 rounded-lg"
                active-class="text-white bg-[#FFAFCC]/90" @click="$emit('toggle-menu')">
                Shop
            </RouterLink>
            <RouterLink v-if="isAuthenticated" to="/challenges"
                class="block hover:text-[#FFAFCC] transition-colors py-2 px-3 rounded-lg"
                active-class="text-white bg-[#FFAFCC]/90" @click="$emit('toggle-menu')">
                Challenges
            </RouterLink>

            <!-- Start Session Button -->
            <RouterLink v-if="isAuthenticated" to="/start-session"
                class="block bg-gradient-to-r from-[#FFC8DD] to-[#CDB4DB] text-white text-center py-2.5 rounded-lg hover:from-[#FFC8DD]/90 hover:to-[#CDB4DB]/90 transition-all duration-300 shadow-lg hover:shadow-xl mt-4"
                active-class="from-[#FFC8DD]/90 to-[#CDB4DB]/90 shadow-xl" @click="$emit('toggle-menu')">
                Start Session
            </RouterLink>
        </div>
    </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { defineProps, defineEmits } from 'vue';
import { useAuth } from '@/api/authService'; // Import useAuth for authentication checks

defineProps<{
    isMobileMenuOpen: boolean;
}>();

defineEmits<{
    (e: 'toggle-menu'): void;
}>();

const { isAuthenticated, logout } = useAuth(); // Access authentication state and logout function
</script>

<style scoped>
/* Smooth transitions */
.router-link-active {
    transition: all 0.3s ease;
}

/* Gradient animation */
.bg-gradient-to-r {
    background-size: 200% auto;
    transition: background-position 0.5s ease;
}

.bg-gradient-to-r:hover {
    background-position: right center;
}

/* Glass effect for mobile menu */
.backdrop-blur-sm {
    backdrop-filter: blur(8px);
}
</style>