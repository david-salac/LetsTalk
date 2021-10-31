<template>
  <h2>{{ operationTitle }}</h2>
  <form @submit="onSubmit">
    <input
      v-model="condition_id"
      name="condition_id"
      type="hidden"
      v-if="!adding_item"
    />
    <input
      v-model="doctor_id"
      name="doctor_id"
      type="hidden"
      v-if="!adding_item"
    />
    <label for="name">Name of condition<sup>*</sup>:</label>
    <input
      v-model="name"
      id="name"
      name="name"
      type="text"
      placeholder="Name of condition*"
    />
    <label for="duration">Duration of condition<sup>*</sup>:</label>
    <input
      v-model="duration"
      id="duration"
      name="duration"
      type="text"
      placeholder="Duration of condition*"
    />

    <label for="doc_name">Doctor Name<sup>*</sup>:</label>
    <input
      v-model="doc_name"
      id="doc_name"
      name="doc_name"
      type="text"
      placeholder="Doctor Name*"
    />

    <label for="doc_specialism">Doctor Specialism<sup>*</sup>:</label>
    <input
      v-model="doc_specialism"
      id="doc_specialism"
      name="doc_specialism"
      type="text"
      placeholder="Doctor Specialism*"
    />

    <label for="details">Details:</label>
    <textarea
      id="details"
      cols="25"
      rows="5"
      name="details"
      placeholder="Details"
      v-model="details"
    ></textarea>

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
  name: "ConditionForm",
  emits: ["add-condition", "cancel-form", "edit-condition"],
  computed: {
    operationTitle() {
      // Decide what the title/button text is
      return this.adding_item ? "Add new condition" : "Edit the condition";
    },
  },
  methods: {
    onSubmit(e) {
      e.preventDefault();
      if (
        // Validate if all required fields are filled
        this.name &&
        this.duration &&
        this.doc_name &&
        this.doc_specialism
      ) {
        // Construct the body for request
        const condition_state = {
          condition: {
            name: this.name,
            duration: this.duration,
            details: !this.details ? null : this.details,
          },
          doctor: { name: this.doc_name, specialism: this.doc_specialism },
        };
        // Emit data for POST/PUT upwards
        if (this.adding_item) {
          this.$emit("add-condition", condition_state);
        } else {
          // Add IDs for update (PUT)
          condition_state.condition.id = this.condition_id;
          condition_state.doctor.id = this.doctor_id;
          this.$emit("edit-condition", condition_state);
        }
        // Clear the form
        this.name = "";
        this.duration = "";
        this.doc_name = "";
        this.doc_specialism = "";
        this.details = "";
        this.condition_id = "";
        this.doctor_id = "";
      } else {
        alert("You have to fill all required values!");
        return;
      }
    },
  },
  data() {
    return {
      // If adding_item is true: add new condition; if false: update existing
      adding_item: true,
      // Fields matching to the form
      name: "",
      duration: "",
      doc_name: "",
      doc_specialism: "",
      details: "",
      // For editing (hidden fields containing IDs)
      condition_id: "",
      doctor_id: "",
    };
  },
  props: {
    // This Condition object is edited (if not null)
    edited_item: Object,
  },
  created() {
    if (this.edited_item) {
      // Initialize form from condition object (when editing)
      this.adding_item = false;
      this.name = this.edited_item.name;
      this.duration = this.edited_item.duration;
      this.doc_name = this.edited_item.doctor.name;
      this.doc_specialism = this.edited_item.doctor.specialism;
      this.details = this.edited_item.details;
      this.condition_id = this.edited_item.id;
      this.doctor_id = this.edited_item.doctor.id;
    }
  },
};
</script>
