<template>
    <div>
      <!-- Desktop Navigation -->
      <div class="hidden md:flex items-center space-x-4">
        <RouterLink
          v-if="isAuthenticated"
          to="/dashboard"
          class="px-3 py-1.5 rounded-lg hover:text-[#FFAFCC] transition-colors duration-300 relative group"
          active-class="text-white bg-[#FFAFCC]/90 shadow-md"
        >
          Dashboard
          <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-[#FFAFCC] transition-all duration-300 group-hover:w-full"></span>
        </RouterLink>
        <RouterLink
          v-if="isAuthenticated"
          to="/shop"
          class="px-3 py-1.5 rounded-lg hover:text-[#FFAFCC] transition-colors duration-300 relative group"
          active-class="text-white bg-[#FFAFCC]/90 shadow-md"
        >
          Shop
          <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-[#FFAFCC] transition-all duration-300 group-hover:w-full"></span>
        </RouterLink>
        <RouterLink
          v-if="isAuthenticated"
          to="/challenges"
          class="px-3 py-1.5 rounded-lg hover:text-[#FFAFCC] transition-colors duration-300 relative group"
          active-class="text-white bg-[#FFAFCC]/90 shadow-md"
        >
          Challenges
          <span class="absolute bottom-0 left-0 w-0 h-0.5 bg-[#FFAFCC] transition-all duration-300 group-hover:w-full"></span>
        </RouterLink>
        
        <div class="ml-auto flex items-center space-x-4">
          <RouterLink
            v-if="isAuthenticated"
            to="/start-session"
            class="bg-gradient-to-r from-[#FFC8DD] to-[#CDB4DB] text-white px-5 py-2 rounded-lg hover:from-[#FFC8DD]/90 hover:to-[#CDB4DB]/90 transition-all duration-300 shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-95 flex items-center"
            active-class="from-[#FFC8DD]/90 to-[#CDB4DB]/90 shadow-xl"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Start Session
          </RouterLink>
          
          <RouterLink
            v-if="isAuthenticated"
            to="/profile"
            class="ml-4 text-white hover:text-[#FFAFCC] transition-colors duration-300 p-1 rounded-full hover:bg-white/10"
            title="Profile"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A4 4 0 0112 15a4 4 0 016.879 2.804M15 11a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </RouterLink>
          
          <button 
            @click="logout" 
            class="text-white hover:text-[#FFAFCC] transition-colors duration-300 p-1 rounded-full hover:bg-white/10 relative group"
            title="Logout"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7" />
            </svg>
            <span class="absolute -bottom-7 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap">
              Logout
            </span>
          </button>
        </div>
      </div>
  
      <!-- Mobile Toggle -->
      <button
        @click="$emit('toggle-menu')"
        class="md:hidden text-white focus:outline-none hover:text-[#FFAFCC] transition-colors duration-300 p-1.5 rounded-full hover:bg-white/10"
        :aria-expanded="isMobileMenuOpen"
        aria-label="Toggle menu"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path
            v-if="!isMobileMenuOpen"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16"
          />
          <path
            v-else
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
  
      <!-- Mobile Navigation -->
      <transition
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 scale-95"
        enter-to-class="opacity-100 scale-100"
        leave-active-class="transition-all duration-200 ease-in"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
      >
        <div
          v-if="isMobileMenuOpen"
          class="mt-4 space-y-3 max-w-7xl mx-auto bg-[#BDE0FE]/30 backdrop-blur-sm rounded-xl p-4 border border-[#CDB4DB]/50 shadow-xl"
        >
          <RouterLink
            v-if="isAuthenticated"
            to="/dashboard"
            class="block py-2.5 px-4 rounded-lg hover:text-[#FFAFCC] transition-colors duration-300 hover:bg-white/10 flex items-center"
            active-class="text-white bg-[#FFAFCC]/90"
            @click="$emit('toggle-menu')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
            Dashboard
          </RouterLink>
          <RouterLink
            v-if="isAuthenticated"
            to="/shop"
            class="block py-2.5 px-4 rounded-lg hover:text-[#FFAFCC] transition-colors duration-300 hover:bg-white/10 flex items-center"
            active-class="text-white bg-[#FFAFCC]/90"
            @click="$emit('toggle-menu')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            Shop
          </RouterLink>
          <RouterLink
            v-if="isAuthenticated"
            to="/challenges"
            class="block py-2.5 px-4 rounded-lg hover:text-[#FFAFCC] transition-colors duration-300 hover:bg-white/10 flex items-center"
            active-class="text-white bg-[#FFAFCC]/90"
            @click="$emit('toggle-menu')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Challenges
          </RouterLink>
          <RouterLink
            v-if="isAuthenticated"
            to="/start-session"
            class="block text-center py-3 rounded-lg bg-gradient-to-r from-[#FFC8DD] to-[#CDB4DB] text-white hover:from-[#FFC8DD]/90 hover:to-[#CDB4DB]/90 transition-all duration-300 shadow-lg hover:shadow-xl mt-4 flex items-center justify-center"
            active-class="from-[#FFC8DD]/90 to-[#CDB4DB]/90 shadow-xl"
            @click="$emit('toggle-menu')"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            Start Session
          </RouterLink>
          <div class="mt-3 border-t border-[#CDB4DB]/50 pt-3 space-y-2">
            <RouterLink
              v-if="isAuthenticated"
              to="/profile"
              class="block py-2 px-4 rounded-lg hover:text-[#FFAFCC] transition-colors duration-300 hover:bg-white/10 flex items-center"
              @click="$emit('toggle-menu')"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Profile
            </RouterLink>
            <button
              v-if="isAuthenticated"
              @click="() => { logout(); $emit('toggle-menu') }"
              class="w-full text-left py-2 px-4 rounded-lg hover:text-[#FFAFCC] transition-colors duration-300 hover:bg-white/10 flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7" />
              </svg>
              Logout
            </button>
          </div>
        </div>
      </transition>
    </div>
  </template>
  
  <script setup lang="ts">
  import { RouterLink } from 'vue-router';
  import { defineProps, defineEmits } from 'vue';
  import { useAuth } from '@/api/authService';
  
  defineProps<{
      isMobileMenuOpen: boolean;
  }>();
  
  defineEmits<{
      (e: 'toggle-menu'): void;
  }>();
  
  const { isAuthenticated, logout } = useAuth();
  </script>
  
  <style scoped>
  /* Enhanced gradient animation */
  .bg-gradient-to-r {
      background-size: 200% auto;
      background-position: left center;
      transition: background-position 0.5s ease, transform 0.2s ease, box-shadow 0.3s ease;
  }
  
  .bg-gradient-to-r:hover {
      background-position: right center;
      transform: translateY(-1px);
  }
  
  /* Smooth transitions for all interactive elements */
  .router-link-active, button {
      transition: all 0.3s ease;
  }
  
  /* Improved glass effect */
  .backdrop-blur-sm {
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
  }
  </style>