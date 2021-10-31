<template>
  <div class="l-ul">
    <div
      class="l-item"
      v-for="appointment in appointments"
      :key="appointment.id"
    >
      <a
        href="javascript:;"
        @click="$emit('delete-appointment', appointment.id)"
        class="delete"
        ><i class="fas fa-times"></i
      ></a>
      <h3>
        <a
          href="javascript:;"
          @click="$emit('display-edit-appointment', appointment)"
          >Condition: {{ appointment.condition.name }})</a
        >
      </h3>
      <p v-if="appointment.details">
        <strong>Details: </strong> {{ appointment.details }}
      </p>
      <p>
        <strong>Date and time: </strong>
        {{ formattedDateTime(appointment.date_and_time) }}
      </p>
    </div>
  </div>
</template>

<script>
// This component list appointments and emits delete/update actions
export default {
  name: "Appointments",
  emits: ["delete-appointment", "edit-appointment", "display-edit-appointment"],
  props: {
    appointments: Array,
  },
  methods: {
    formattedDateTime(iso_8601_date_time) {
      const date_time_obj = new Date(String(iso_8601_date_time));
      return (
        String(date_time_obj.getDate()) +
        "." +
        String(date_time_obj.getMonth() + 1) +
        "." +
        String(date_time_obj.getFullYear()) +
        " at " +
        String(date_time_obj.getHours()) +
        ":" +
        String(date_time_obj.getMinutes())
      );
    },
  },
};
</script>
