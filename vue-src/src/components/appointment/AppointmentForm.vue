<template>
  <h2>{{ operationTitle }}</h2>
  <form @submit="onSubmit">
    <input
      v-model="appointment_id"
      name="appointment_id"
      id="appointment_id"
      type="hidden"
      v-if="!adding_item"
    />

    <label for="date_and_time">Date and time of appointment<sup>*</sup>:</label>
    <input
      v-model="date_and_time"
      id="date_and_time"
      name="date_and_time"
      type="datetime-local"
      placeholder="Date and time*"
    />

    <label for="details">Details of appointment:</label>
    <textarea
      v-model="details"
      id="details"
      name="details"
      cols="25"
      rows="5"
      placeholder="Details"
    ></textarea>

    <label for="condition">Any related condition?<sup>*</sup>:</label>
    <select v-model="condition" id="condition" name="condition">
      <option
        v-for="condition in conditions_array"
        :key="condition.id"
        :value="condition.id"
      >
        {{ condition.name }}
      </option>
    </select>

    <input type="submit" v-model="operationTitle" />

    <input
      type="button"
      @click="$emit('cancel-form')"
      class="cancel"
      value="Cancel"
    />
  </form>
</template>

<script>
export default {
  name: "AppointmentForm",
  emits: ["add-appointment", "cancel-form", "edit-appointment"],
  computed: {
    operationTitle() {
      // Decide what the title/button text is
      return this.adding_item ? "Add new appointment" : "Edit the appointment";
    },
  },
  methods: {
    onSubmit(e) {
      e.preventDefault();
      if (
        // Validate if all required fields are filled
        this.date_and_time &&
        this.condition
      ) {
        // Construct the body for request
        const appointment_state = {
          date_and_time: this.date_and_time,
          condition_id: this.condition,
          details: !this.details ? null : this.details,
        };
        // Emit data for POST/PUT upwards
        if (this.adding_item) {
          this.$emit("add-appointment", appointment_state);
        } else {
          // Add IDs for update (PUT)
          appointment_state.id = this.appointment_id;
          this.$emit("edit-appointment", appointment_state);
        }
        // Clear the form
        this.date_and_time = "";
        this.details = "";
        this.condition = "";
        this.appointment_id = "";
      } else {
        alert("You have to fill all required values!");
        return;
      }
    },
  },
  data() {
    return {
      // If adding_item is true: add new appointment; if false: update existing
      adding_item: true,
      // Fields matching to the form
      date_and_time: "", // In ISO 8601
      details: "",
      condition: "",
      // For editing (hidden fields containing IDs)
      appointment_id: "",
    };
  },
  props: {
    // This Appointment object is edited (if not null)
    edited_item: Object,
    // Conditions for listing
    conditions_array: Array,
  },
  async created() {
    if (this.edited_item) {
      // Initialize form from appointment object (when editing)
      this.adding_item = false;
      this.date_and_time = this.edited_item.date_and_time;
      this.details = this.edited_item.details;
      this.appointment_id = this.edited_item.id;
      this.condition = this.edited_item.condition.id;
    }
  },
};
</script>
