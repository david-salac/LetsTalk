<template>
  <menu>
    <li>
      <a href="javascript:;" @click="$emit('add-new-appointment')"
        >Add new appointment</a
      >
    </li>
    <li><router-link to="/">Home</router-link></li>
  </menu>
</template>

<script>
// Menu for appointments
export default {
  name: "AppointmentsMenu",
  emits: ["add-new-appointment"],
};
</script>
