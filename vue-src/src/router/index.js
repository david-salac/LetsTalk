import { createRouter, createWebHistory } from 'vue-router'
import ConditionsPage from '../views/ConditionsPage.vue'
import ConcernsPage from '../views/ConcernsPage.vue'
import ExpectationsPage from '../views/ExpectationsPage.vue'
import AppointmentPage from '../views/AppointmentPage.vue'
import HomePage from '../views/HomePage.vue'
import LicensePage from '../views/LicensePage.vue'

const routes = [
    {
        path: '/conditions',
        name: 'Conditions',
        component: ConditionsPage
    },
    {
        path: '/concerns',
        name: 'Concerns',
        component: ConcernsPage
    },
    {
        path: '/expectations',
        name: 'Expectations',
        component: ExpectationsPage
    },
    {
        path: '/appointment',
        name: 'Appointment',
        component: AppointmentPage
    },
    {
        path: '/license',
        name: 'License',
        component: LicensePage
    },
    {
        path: '/',
        name: 'Home',
        component: HomePage
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
