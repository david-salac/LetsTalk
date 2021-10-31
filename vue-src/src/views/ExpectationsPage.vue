<template>
  <ExpectationForm
    v-if="show_add"
    @add-expectation="addExpectation"
    @edit-expectation="editExpectation"
    @cancel-form="hideAddForm"
    :edited_item="edited_expectation"
    :conditions_array="conditions"
  />
  <div v-if="!show_add">
    <h2>Expectations</h2>
    <ExpectationsMenu @add-new-expectation="displayAddForm" />
    <Expectations
      :expectations="expectations"
      @delete-expectation="deleteExpectation"
      @display-edit-expectation="displayEditExpectation"
    />
  </div>
</template>

<script>
import Expectations from "../components/expectation/Expectations.vue";
import ExpectationForm from "../components/expectation/ExpectationForm.vue";
import ExpectationsMenu from "../components/expectation/ExpectationsMenu.vue";

export default {
  name: "App",
  components: {
    Expectations,
    ExpectationForm,
    ExpectationsMenu,
  },
  data() {
    return {
      expectations: [],
      show_add: false,
      edited_expectation: null,
      conditions: [],
    };
  },
  methods: {
    async fetchExpectations() {
      const resp = await fetch("api/expectation-with-condition");
      const data = await resp.json();
      return data;
    },
    async deleteExpectation(expectation_id) {
      if (confirm("Are you sure?")) {
        const res = await fetch(`api/expectation/${expectation_id}`, {
          method: "DELETE",
        });
        if (res.status === 204) {
          this.expectations = this.expectations.filter(
            (expectation) => expectation.id !== expectation_id
          );
        }
      }
    },
    async addExpectation(expectation_state) {
      const res = await fetch("api/expectation-with-condition", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify(expectation_state),
      });
      const data = await res.json();
      if (res.status === 201) {
        this.expectations = [...this.expectations, data];
        this.show_add = false;
      }
    },
    async editExpectation(expectation_state) {
      const res = await fetch(`api/expectation-with-condition`, {
        method: "PUT",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify(expectation_state),
      });
      const data = await res.json();
      if (res.status === 200) {
        // Update data (state)
        this.expectations = this.expectations.map((expectation) =>
          expectation.id === data.id ? data : expectation
        );
        this.show_add = false;
        this.edited_expectation = null;
      }
    },
    displayAddForm() {
      this.show_add = true;
    },
    displayEditExpectation(expectation) {
      this.edited_expectation = expectation;
      this.show_add = true;
    },
    hideAddForm() {
      this.show_add = false;
      this.edited_expectation = null;
    },
    async fetchConditions() {
      // Fetch all conditions to make selection available
      const resp = await fetch("api/condition");
      const data = await resp.json();
      return data;
    },
  },
  async created() {
    this.expectations = await this.fetchExpectations();
    this.conditions = await this.fetchConditions();
  },
};
</script>
