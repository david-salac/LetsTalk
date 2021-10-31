<template>
  <ConcernForm
    v-if="show_add"
    @add-concern="addConcern"
    @edit-concern="editConcern"
    @cancel-form="hideAddForm"
    :edited_item="edited_concern"
    :conditions_array="conditions"
  />
  <div v-if="!show_add">
    <h2>Concerns</h2>
    <ConcernsMenu @add-new-concern="displayAddForm" />
    <Concerns
      :concerns="concerns"
      @delete-concern="deleteConcern"
      @display-edit-concern="displayEditConcern"
    />
  </div>
</template>

<script>
import Concerns from "../components/concern/Concerns.vue";
import ConcernForm from "../components/concern/ConcernForm.vue";
import ConcernsMenu from "../components/concern/ConcernsMenu.vue";

export default {
  name: "App",
  components: {
    Concerns,
    ConcernForm,
    ConcernsMenu,
  },
  data() {
    return {
      concerns: [],
      show_add: false,
      edited_concern: null,
      conditions: [],
    };
  },
  methods: {
    async fetchConcerns() {
      const resp = await fetch("api/concern-with-condition");
      const data = await resp.json();
      return data;
    },
    async deleteConcern(concern_id) {
      if (confirm("Are you sure?")) {
        const res = await fetch(`api/concern/${concern_id}`, {
          method: "DELETE",
        });
        if (res.status === 204) {
          this.concerns = this.concerns.filter(
            (concern) => concern.id !== concern_id
          );
        }
      }
    },
    async addConcern(concern_state) {
      const res = await fetch("api/concern-with-condition", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify(concern_state),
      });
      const data = await res.json();
      if (res.status === 201) {
        this.concerns = [...this.concerns, data];
        this.show_add = false;
      }
    },
    async editConcern(concern_state) {
      const res = await fetch(`api/concern-with-condition`, {
        method: "PUT",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify(concern_state),
      });
      const data = await res.json();
      if (res.status === 200) {
        // Update data (state)
        this.concerns = this.concerns.map((concern) =>
          concern.id === data.id ? data : concern
        );
        this.show_add = false;
        this.edited_concern = null;
      }
    },
    displayAddForm() {
      this.show_add = true;
    },
    displayEditConcern(concern) {
      this.edited_concern = concern;
      this.show_add = true;
    },
    hideAddForm() {
      this.show_add = false;
      this.edited_concern = null;
    },
    async fetchConditions() {
      // Fetch all conditions to make selection available
      const resp = await fetch("api/condition");
      const data = await resp.json();
      return data;
    },
  },
  async created() {
    this.concerns = await this.fetchConcerns();
    this.conditions = await this.fetchConditions();
  },
};
</script>
