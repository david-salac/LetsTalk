<template>
  <h2>{{ operationTitle }}</h2>
  <form @submit="onSubmit">
    <input
      v-model="expectation_id"
      name="expectation_id"
      id="expectation_id"
      type="hidden"
      v-if="!adding_item"
    />

    <label for="name">Name of expectation<sup>*</sup>:</label>
    <input
      v-model="name"
      id="name"
      name="name"
      type="text"
      placeholder="Name of expectation*"
    />

    <label for="details">Details of expectation:</label>
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
  name: "ExpectationForm",
  emits: ["add-expectation", "cancel-form", "edit-expectation"],
  computed: {
    operationTitle() {
      // Decide what the title/button text is
      return this.adding_item ? "Add new expectation" : "Edit the expectation";
    },
  },
  methods: {
    onSubmit(e) {
      e.preventDefault();
      if (
        // Validate if all required fields are filled
        this.name &&
        this.condition
      ) {
        // Construct the body for request
        const expectation_state = {
          name: this.name,
          condition_id: this.condition,
          details: !this.details ? null : this.details,
        };
        // Emit data for POST/PUT upwards
        if (this.adding_item) {
          this.$emit("add-expectation", expectation_state);
        } else {
          // Add IDs for update (PUT)
          expectation_state.id = this.expectation_id;
          this.$emit("edit-expectation", expectation_state);
        }
        // Clear the form
        this.name = "";
        this.details = "";
        this.condition = "";
        this.expectation_id = "";
      } else {
        alert("You have to fill all required values!");
        return;
      }
    },
  },
  data() {
    return {
      // If adding_item is true: add new expectation; if false: update existing
      adding_item: true,
      // Fields matching to the form
      name: "",
      details: "",
      condition: "",
      // For editing (hidden fields containing IDs)
      expectation_id: "",
    };
  },
  props: {
    // This Expectation object is edited (if not null)
    edited_item: Object,
    // Conditions for listing
    conditions_array: Array,
  },
  async created() {
    if (this.edited_item) {
      // Initialize form from expectation object (when editing)
      this.adding_item = false;
      this.name = this.edited_item.name;
      this.details = this.edited_item.details;
      this.expectation_id = this.edited_item.id;
      this.condition = this.edited_item.condition.id;
    }
  },
};
</script>
