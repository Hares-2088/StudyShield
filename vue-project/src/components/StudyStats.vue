<template>
    <div class="bg-white p-4 md:p-6 rounded-lg shadow-md mb-4 md:mb-6">
        <h2 class="text-lg md:text-xl font-semibold text-pink-700 mb-3 md:mb-4">Study Statistics</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <Card>
                <CardHeader class="pb-2">
                    <CardTitle class="text-sm font-medium text-muted-foreground">Day Streak</CardTitle>
                </CardHeader>
                <CardContent>
                    <div class="text-2xl font-bold text-pink-700">{{ dayStreak }}</div>
                    <p class="text-xs text-muted-foreground mt-1">
                        days in a row
                    </p>
                    <Progress class="mt-2" :value="(dayStreak / 30) * 100" :class="{ 'bg-pink-300': true }" />
                </CardContent>
            </Card>

            <Card>
                <CardHeader class="pb-2">
                    <CardTitle class="text-sm font-medium text-muted-foreground">Weekly Hours</CardTitle>
                </CardHeader>
                <CardContent>
                    <div class="text-2xl font-bold text-pink-700">{{ weeklyHours }}</div>
                    <p class="text-xs text-muted-foreground mt-1">
                        hours this week
                    </p>
                    <Progress class="mt-2" :value="(weeklyHours / 40) * 100" :class="{ 'bg-pink-300': true }" />
                </CardContent>
            </Card>
        </div>

        <!-- Today's Focus Time -->
        <div class="mb-6">
            <Card>
                <CardHeader class="flex flex-row items-center justify-between pb-2">
                    <CardTitle class="text-sm font-medium text-muted-foreground">Today's Focus Time</CardTitle>
                    <Badge variant="outline" class="bg-pink-50 text-pink-700">{{ Math.floor(focusTime / 60) }}h {{
                        focusTime % 60 }}m</Badge>
                </CardHeader>
                <CardContent>
                    <Progress class="mt-2" :value="(focusTime / (8 * 60)) * 100" :class="{ 'bg-pink-300': true }" />
                </CardContent>
            </Card>
        </div>

        <!-- Study Calendar with Navigation -->
        <div class="mt-6">
            <h3 class="text-md font-medium text-pink-700 mb-3">Study Activity</h3>

            <!-- Month Navigation -->
            <div class="flex justify-between items-center mb-3">
                <button @click="previousMonth" class="bg-pink-100 hover:bg-pink-200 text-pink-700 px-3 py-1 rounded-md">
                    <span>&larr;</span> Previous
                </button>
                <span class="font-semibold text-pink-700">{{ monthNames[viewedMonth] }} {{ viewedYear }}</span>
                <button @click="nextMonth" class="bg-pink-100 hover:bg-pink-200 text-pink-700 px-3 py-1 rounded-md"
                    :disabled="isCurrentMonth">
                    Next <span>&rarr;</span>
                </button>
            </div>

            <div class="study-calendar border rounded-lg p-4 bg-white">
                <div class="grid grid-cols-7 gap-1">
                    <!-- Calendar header -->
                    <div v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']" :key="day"
                        class="text-center text-xs text-gray-500 font-medium py-1">
                        {{ day }}
                    </div>

                    <!-- Calendar days -->
                    <div v-for="(day, index) in calendarDays" :key="index"
                        class="aspect-square flex items-center justify-center rounded-md text-xs"
                        :class="day.isStudyDay ? 'bg-pink-500 text-white' : day.isCurrentMonth ? 'bg-pink-100' : 'bg-gray-100 text-gray-400'">
                        {{ day.date }}
                    </div>
                </div>
            </div>

            <!-- Today button -->
            <div class="mt-3 flex justify-center">
                <button @click="goToCurrentMonth" class="text-pink-700 text-sm hover:underline">
                    Back to Current Month
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useUserStore } from '../stores/userStore';

// Direct imports as an alternative
import Card from './ui/card/Card.vue';
import CardHeader from './ui/card/CardHeader.vue';
import CardTitle from './ui/card/CardTitle.vue';
import CardContent from './ui/card/CardContent.vue';
import Progress from './ui/progress/Progress.vue';
import Badge from './ui/badge/Badge.vue';

const userStore = useUserStore();
const focusTime = computed(() => userStore.focusTime);
const dayStreak = computed(() => userStore.dayStreak || 0);
const weeklyHours = computed(() => userStore.weeklyStudyHours || 0);

// Calendar data and navigation
interface CalendarDay {
    date: number;
    isCurrentMonth: boolean;
    isStudyDay: boolean;
}

const calendarDays = ref<CalendarDay[]>([]);
const studyDays = ref<string[]>([]); // Format: 'YYYY-MM-DD'
const viewedMonth = ref(new Date().getMonth());
const viewedYear = ref(new Date().getFullYear());
const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
];

// Check if we're viewing the current month
const isCurrentMonth = computed(() => {
    const today = new Date();
    return viewedMonth.value === today.getMonth() && viewedYear.value === today.getFullYear();
});

// Navigate to previous month
const previousMonth = () => {
    if (viewedMonth.value === 0) {
        viewedMonth.value = 11;
        viewedYear.value--;
    } else {
        viewedMonth.value--;
    }
    generateCalendarDays();
};

// Navigate to next month
const nextMonth = () => {
    if (!isCurrentMonth.value) {
        if (viewedMonth.value === 11) {
            viewedMonth.value = 0;
            viewedYear.value++;
        } else {
            viewedMonth.value++;
        }
        generateCalendarDays();
    }
};

// Return to current month
const goToCurrentMonth = () => {
    const today = new Date();
    viewedMonth.value = today.getMonth();
    viewedYear.value = today.getFullYear();
    generateCalendarDays();
};

// Generate calendar days for the viewed month
const generateCalendarDays = () => {
    const year = viewedYear.value;
    const month = viewedMonth.value;

    // First day of the month
    const firstDay = new Date(year, month, 1);
    const startingDayOfWeek = firstDay.getDay(); // 0 = Sunday, 1 = Monday, etc.

    // Last day of the month
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();

    // Previous month's days needed to fill the calendar
    const daysFromPrevMonth = startingDayOfWeek;
    const prevMonthLastDay = new Date(year, month, 0).getDate();

    const days: CalendarDay[] = [];

    // Add previous month days
    for (let i = daysFromPrevMonth - 1; i >= 0; i--) {
        days.push({
            date: prevMonthLastDay - i,
            isCurrentMonth: false,
            isStudyDay: isStudyDay(new Date(year, month - 1, prevMonthLastDay - i))
        });
    }

    // Add current month days
    for (let i = 1; i <= daysInMonth; i++) {
        days.push({
            date: i,
            isCurrentMonth: true,
            isStudyDay: isStudyDay(new Date(year, month, i))
        });
    }

    // Add next month days to fill the calendar (6 rows x 7 days = 42 total cells)
    const daysNeeded = 42 - days.length;
    for (let i = 1; i <= daysNeeded; i++) {
        days.push({
            date: i,
            isCurrentMonth: false,
            isStudyDay: isStudyDay(new Date(year, month + 1, i))
        });
    }

    calendarDays.value = days;
};

// Check if a date is a study day
const isStudyDay = (date: Date) => {
    const dateString = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    return studyDays.value.includes(dateString);
};

// Fetch study days from userStore (dates come as ISO strings)
const fetchStudyDays = async () => {
    studyDays.value = userStore.studyStats.map((stat: { date: string | Date }) => {
        // If stat.date is a string, just slice; if Date, toISOString()
        const iso = typeof stat.date === 'string'
            ? stat.date
            : stat.date.toISOString();
        return iso.slice(0, 10); // "YYYY-MM-DD"
    });
    console.log('Study Days:', studyDays.value);
    console.log('Study Stats:', userStore.studyStats);
};

onMounted(async () => {
    if (!userStore.user) {
        await userStore.fetchUserData();
    }

    // Fetch study days and generate calendar days
    fetchStudyDays();
    generateCalendarDays();
});
</script>

<style scoped>
.study-calendar {
    width: 100%;
}
</style>
