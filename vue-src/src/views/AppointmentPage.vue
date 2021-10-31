<template>
  <AppointmentForm
    v-if="show_add"
    @add-appointment="addAppointment"
    @edit-appointment="editAppointment"
    @cancel-form="hideAddForm"
    :edited_item="edited_appointment"
    :conditions_array="conditions"
  />
  <div v-if="!show_add">
    <h2>Appointments</h2>
    <AppointmentsMenu @add-new-appointment="displayAddForm" />
    <Appointments
      :appointments="appointments"
      @delete-appointment="deleteAppointment"
      @display-edit-appointment="displayEditAppointment"
    />
  </div>
</template>

<script>
import Appointments from "../components/appointment/Appointments.vue";
import AppointmentForm from "../components/appointment/AppointmentForm.vue";
import AppointmentsMenu from "../components/appointment/AppointmentsMenu.vue";

export default {
  name: "App",
  components: {
    Appointments,
    AppointmentForm,
    AppointmentsMenu,
  },
  data() {
    return {
      appointments: [],
      show_add: false,
      edited_appointment: null,
      conditions: [],
    };
  },
  methods: {
    async fetchAppointments() {
      const resp = await fetch("api/appointment-with-condition");
      const data = await resp.json();
      return data;
    },
    async deleteAppointment(appointment_id) {
      if (confirm("Are you sure?")) {
        const res = await fetch(`api/appointment/${appointment_id}`, {
          method: "DELETE",
        });
        if (res.status === 204) {
          this.appointments = this.appointments.filter(
            (appointment) => appointment.id !== appointment_id
          );
        }
      }
    },
    async addAppointment(appointment_state) {
      const res = await fetch("api/appointment-with-condition", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify(appointment_state),
      });
      const data = await res.json();
      if (res.status === 201) {
        this.appointments = [...this.appointments, data];
        this.show_add = false;
      }
    },
    async editAppointment(appointment_state) {
      const res = await fetch(`api/appointment-with-condition`, {
        method: "PUT",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify(appointment_state),
      });
      const data = await res.json();
      if (res.status === 200) {
        // Update data (state)
        this.appointments = this.appointments.map((appointment) =>
          appointment.id === data.id ? data : appointment
        );
        this.show_add = false;
        this.edited_appointment = null;
      }
    },
    displayAddForm() {
      this.show_add = true;
    },
    displayEditAppointment(appointment) {
      this.edited_appointment = appointment;
      this.show_add = true;
    },
    hideAddForm() {
      this.show_add = false;
      this.edited_appointment = null;
    },
    async fetchConditions() {
      // Fetch all conditions to make selection available
      const resp = await fetch("api/condition");
      const data = await resp.json();
      return data;
    },
  },
  async created() {
    this.appointments = await this.fetchAppointments();
    this.conditions = await this.fetchConditions();
  },
};
</script>
