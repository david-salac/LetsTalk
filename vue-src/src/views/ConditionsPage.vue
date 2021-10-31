<template>
  <ConditionForm
    v-if="show_add"
    @add-condition="addCondition"
    @edit-condition="editCondition"
    @cancel-form="hideAddForm"
    :edited_item="edited_condition"
  />
  <div v-if="!show_add">
    <h2>Conditions</h2>
    <ConditionsMenu @add-new-condition="displayAddForm" />
    <Conditions
      :conditions="conditions"
      @delete-condition="deleteCondition"
      @display-edit-condition="displayEditCondition"
    />
  </div>
</template>

<script>
import Conditions from "../components/condition/Conditions.vue";
import ConditionForm from "../components/condition/ConditionForm.vue";
import ConditionsMenu from "../components/condition/ConditionsMenu.vue";

export default {
  name: "App",
  components: {
    Conditions,
    ConditionForm,
    ConditionsMenu,
  },
  data() {
    return {
      conditions: [],
      show_add: false,
      edited_condition: null,
    };
  },
  methods: {
    async fetchConditions() {
      const resp = await fetch("api/condition-with-doctor");
      const data = await resp.json();
      return data;
    },
    async deleteCondition(condition_id) {
      if (confirm("Are you sure?")) {
        const res = await fetch(`api/condition/${condition_id}`, {
          method: "DELETE",
        });
        if (res.status === 204) {
          this.conditions = this.conditions.filter(
            (condition) => condition.id !== condition_id
          );
        }
      }
    },
    async addCondition(condition_state) {
      const res = await fetch("api/condition-with-doctor", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify(condition_state),
      });
      const data = await res.json();
      if (res.status === 201) {
        this.conditions = [...this.conditions, data];
        this.show_add = false;
      }
    },
    async editCondition(condition_state) {
      const res = await fetch("api/condition-with-doctor", {
        method: "PUT",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify(condition_state),
      });
      const data = await res.json();
      if (res.status === 200) {
        // Update data (state)
        this.conditions = this.conditions.map((condition) =>
          condition.id === data.id ? data : condition
        );
        this.show_add = false;
        this.edited_condition = null;
      }
    },
    displayAddForm() {
      this.show_add = true;
    },
    displayEditCondition(condition) {
      this.edited_condition = condition;
      this.show_add = true;
    },
    hideAddForm() {
      this.show_add = false;
      this.edited_condition = null;
    },
  },
  async created() {
    this.conditions = await this.fetchConditions();
  },
};
</script>
