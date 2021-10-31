<template>
  <h2>{{ operationTitle }}</h2>
  <form @submit="onSubmit">
    <input
      v-model="concern_id"
      name="concern_id"
      id="concern_id"
      type="hidden"
      v-if="!adding_item"
    />

    <label for="creator">Patient or Doctor's concern?<sup>*</sup>:</label>
    <select v-model="creator" id="creator" name="creator">
      <option value="patient">Patient</option>
      <option value="doctor">Doctor</option>
    </select>

    <label for="details">Details of concern:</label>
    <textarea
      v-model="details"
      id="details"
      name="details"
      cols="25"
      rows="5"
      placeholder="Details"
    ></textarea>

    <label for="symptoms">Any specific symptoms?<sup>*</sup>:</label>
    <input
      v-model="symptoms"
      id="symptoms"
      name="symptoms"
      type="text"
      placeholder="Specific symptoms*"
    />

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

    <label for="level"
      >How concerned are you (5 is most and 1 is least)?<sup>*</sup>:</label
    >
    <select v-model="level" id="level" name="level">
      <option value="1">1 (Normal)</option>
      <option value="2">2 (Minor)</option>
      <option value="3">3 (Moderate)</option>
      <option value="4">4 (Serious)</option>
      <option value="5">5 (Severe)</option>
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
  name: "ConcernForm",
  emits: ["add-concern", "cancel-form", "edit-concern"],
  computed: {
    operationTitle() {
      // Decide what the title/button text is
      return this.adding_item ? "Add new concern" : "Edit the concern";
    },
  },
  methods: {
    onSubmit(e) {
      e.preventDefault();
      if (
        // Validate if all required fields are filled
        this.creator &&
        this.symptoms &&
        this.condition &&
        this.level
      ) {
        // Construct the body for request
        const concern_state = {
          creator: this.creator,
          symptoms: this.symptoms,
          condition_id: this.condition,
          level: parseInt(this.level),
          details: !this.details ? null : this.details,
        };
        // Emit data for POST/PUT upwards
        if (this.adding_item) {
          this.$emit("add-concern", concern_state);
        } else {
          // Add IDs for update (PUT)
          concern_state.id = this.concern_id;
          this.$emit("edit-concern", concern_state);
        }
        // Clear the form
        this.creator = "";
        this.details = "";
        this.symptoms = "";
        this.condition = "";
        this.level = "";
        this.concern_id = "";
      } else {
        alert("You have to fill all required values!");
        return;
      }
    },
  },
  data() {
    return {
      // If adding_item is true: add new concern; if false: update existing
      adding_item: true,
      // Fields matching to the form
      creator: "",
      details: "",
      symptoms: "",
      condition: "",
      level: "",
      // For editing (hidden fields containing IDs)
      concern_id: "",
    };
  },
  props: {
    // This Concern object is edited (if not null)
    edited_item: Object,
    // Conditions for listing
    conditions_array: Array,
  },
  async created() {
    if (this.edited_item) {
      // Initialize form from concern object (when editing)
      this.adding_item = false;
      this.creator = this.edited_item.creator;
      this.details = this.edited_item.details;
      this.symptoms = this.edited_item.symptoms;
      this.level = this.edited_item.level;
      this.concern_id = this.edited_item.id;
      this.condition = this.edited_item.condition.id;
    }
  },
};
</script>
