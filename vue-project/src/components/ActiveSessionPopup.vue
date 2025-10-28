<template>
    <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white/90 backdrop-blur-md p-8 rounded-2xl shadow-xl max-w-md w-full animate-fadeIn">
            <div class="text-center">
                <!-- Icon/Image -->
                <div
                    class="w-16 h-16 mx-auto mb-4 bg-gradient-to-r from-pink-400 to-purple-400 rounded-full flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                </div>

                <!-- Title -->
                <h3 class="text-xl font-semibold text-gray-800 mb-2">Active Study Session Found!</h3>

                <!-- Message -->
                <p class="text-gray-600 mb-6 text-sm leading-relaxed">
                    We found a study session that was started but never completed. Would you like to resume where you
                    left off or mark it as complete?
                </p>

                <!-- Session Details -->
                <div v-if="session" class="bg-pink-50 p-4 rounded-lg mb-6">
                    <p class="text-sm text-gray-700 mb-1">
                        <span class="font-medium">Planned Duration:</span> {{ session.plannedDuration }} minutes
                    </p>
                    <p class="text-sm text-gray-700 mb-1">
                        <span class="font-medium">Tasks:</span> {{ session.tasks?.length || 0 }} task(s)
                    </p>
                    <p class="text-sm text-gray-500">
                        <span class="font-medium">Started:</span> {{ formatDate(session.startTime) }}
                    </p>
                </div>

                <!-- Action Buttons -->
                <div class="flex space-x-3">
                    <button @click="handleResume" :disabled="loading"
                        class="flex-1 bg-gradient-to-r from-green-400 to-green-500 text-white py-3 px-4 rounded-lg font-medium hover:from-green-500 hover:to-green-600 transition duration-300 shadow-md disabled:opacity-50 disabled:cursor-not-allowed">
                        <span v-if="!loading">Resume</span>
                        <span v-else class="flex items-center justify-center">
                            <svg class="animate-spin h-4 w-4 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none"
                                viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
                            </svg>
                            Resuming...
                        </span>
                    </button>

                    <button @click="handleComplete" :disabled="loading"
                        class="flex-1 bg-gradient-to-r from-purple-400 to-purple-500 text-white py-3 px-4 rounded-lg font-medium hover:from-purple-500 hover:to-purple-600 transition duration-300 shadow-md disabled:opacity-50 disabled:cursor-not-allowed">
                        <span v-if="!loading">Complete</span>
                        <span v-else class="flex items-center justify-center">
                            <svg class="animate-spin h-4 w-4 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none"
                                viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
                            </svg>
                            Completing...
                        </span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import type { StudySession } from '@/models/StudySession';

interface Props {
    show: boolean;
    session: StudySession | null;
}

const props = defineProps<Props>();
const emit = defineEmits<{
    close: [];
    resume: [session: StudySession];
    complete: [session: StudySession];
}>();

const router = useRouter();
const userStore = useUserStore();
const loading = ref(false);

const formatDate = (dateString: string | undefined) => {
    if (!dateString) return 'Unknown';
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch {
        return 'Unknown';
    }
};

const handleResume = async () => {
    if (!props.session) return;

    loading.value = true;
    try {
        // Set the current session in the store
        userStore.currentSession = props.session;

        // If the session was paused, resume it
        if (props.session.isPaused) {
            await userStore.resumeCurrentSession();
        }

        // Navigate to the active study session page
        await router.push(`/active-session/${props.session._id}`);

        // Emit resume event
        emit('resume', props.session);
        emit('close');
    } catch (error) {
        console.error('Failed to resume session:', error);
    } finally {
        loading.value = false;
    }
};

const handleComplete = async () => {
    if (!props.session) return;

    loading.value = true;
    try {
        // Calculate actual duration based on start time and current time
        const startTime = new Date(props.session.startTime || '').getTime();
        const now = Date.now();
        const actualDurationMinutes = Math.floor((now - startTime) / (1000 * 60));

        // Complete the session
        await userStore.completeStudySession(
            props.session._id,
            actualDurationMinutes
        );

        // Emit complete event
        emit('complete', props.session);
        emit('close');
    } catch (error) {
        console.error('Failed to complete session:', error);
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-10px) scale(0.95);
    }

    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.animate-fadeIn {
    animation: fadeIn 0.3s ease-out;
}
</style>
