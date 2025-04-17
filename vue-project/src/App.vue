<script setup lang="ts">
import { RouterView, RouterLink } from 'vue-router'
import { ref, onMounted } from 'vue'
import Navigation from './components/Navigation.vue'
import { gsap } from 'gsap'

// NEW imports for auto‑hydration
import { useAuth } from '@/api/authService'
import { useUserStore } from '@/stores/userStore'

const isMobileMenuOpen = ref(false)
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

// auto‑hydrate Pinia store
const auth = useAuth()
const userStore = useUserStore()

onMounted(async () => {
  const particlesContainer = document.querySelector('.particles-container')
  if (particlesContainer) {
    for (let i = 0; i < 20; i++) {
      const particle = document.createElement('div')
      particle.className = 'particle absolute rounded-full'
      const colors = ['#cdb4db', '#ffc8dd', '#ffafcc', '#bde0fe', '#a2d2ff']
      Object.assign(particle.style, {
        width: `${Math.random() * 6 + 2}px`,
        height: `${Math.random() * 6 + 2}px`,
        background: colors[Math.floor(Math.random() * colors.length)],
        left: `${Math.random() * 100}%`,
        top: `${Math.random() * 100}%`,
        opacity: Math.random() * 0.6 + 0.1
      })
      particlesContainer.appendChild(particle)
      gsap.to(particle, {
        x: `${Math.random() * 200 - 100}px`,
        y: `${Math.random() * 200 - 100}px`,
        duration: Math.random() * 20 + 10,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
      })
    }
  }

  if (auth.checkAuth()) {
    try {
      await auth.fetchUser()                      
      const me = auth.user.value
      if (me?.id) {
        await userStore.fetchUserData()
        await userStore.fetchStudySessions()
      }
    } catch (err) {
      console.error('Failed to hydrate on start:', err)
    }
  }
})
</script>

<template>
  <div class="min-h-screen flex flex-col w-full relative">
    <!-- Animated Background -->
    <div class="fixed inset-0 -z-10">
      <div
        class="absolute inset-0 bg-gradient-to-br from-[#cdb4db] via-[#ffc8dd] to-[#a2d2ff] opacity-70 animate-gradient">
      </div>
      <div class="particles-container absolute inset-0 overflow-hidden"></div>
    </div>

    <!-- Content Container with Glass Effect -->
    <div class="flex-grow flex flex-col backdrop-blur-sm bg-white-5">
      <!-- Header -->
      <header class="bg-pink-600/90 text-white shadow-lg w-full">
        <div class="w-full px-4 py-3 md:py-4">
          <nav class="flex items-center justify-between max-w-7xl mx-auto">
            <!-- Logo/Title as Home Link -->
            <RouterLink to="/"
              class="text-xl md:text-2xl font-bold hover:text-pink-200 transition-colors flex items-center">
              <span class="drop-shadow-md">Focus Buddy</span>
              <span class="ml-2 text-lg">🌱</span>
            </RouterLink>

            <!-- Navigation Component -->
            <Navigation :isMobileMenuOpen="isMobileMenuOpen" @toggle-menu="toggleMobileMenu" />
          </nav>
        </div>
      </header>

      <!-- Main Content -->
      <main class="flex-grow w-full px-4 py-5 md:py-8">
        <RouterView />
      </main>

      <!-- Footer -->
      <footer class="bg-pink-600/90 text-white py-3 md:py-4 mt-6 md:mt-8 w-full">
        <div class="w-full px-4 md:px-6 text-center max-w-7xl mx-auto">
          <p class="text-sm drop-shadow-md">
            Made with ❤️ by <span class="font-semibold">Your Name</span>
          </p>
        </div>
      </footer>
    </div>
  </div>
</template>

<style>
@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

.animate-gradient {
  background-size: 300% 300%;
  animation: gradient 15s ease infinite;
}

html,
body,
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
  /* Removed overflow-hidden to allow scrolling */
}

body {
  overflow-y: auto;
  /* Enable vertical scrolling */
}

#app {
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #cdb4db, #ffc8dd, #ffafcc, #bde0fe, #a2d2ff);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
}

#app>div {
  width: 100%;
  flex: 1;
  margin: 0;
  padding: 0;
}

/* Glass effect for content */
.backdrop-blur-sm {
  backdrop-filter: blur(8px);
}

.bg-white-5 {
  background-color: rgba(255, 255, 255, 0.05);
}

/* Particle styling */
.particle {
  will-change: transform;
}

/* Header and footer transparency */
.bg-pink-600\/90 {
  background-color: rgba(219, 39, 119, 0.9);
  /* Your pink-600 with 90% opacity */
}

/* Container fix */
.container {
  width: 100%;
  max-width: 100%;
}

/* Text shadow for better readability */
.drop-shadow-md {
  filter: drop-shadow(0 2px 2px rgba(0, 0, 0, 0.1));
}
</style>