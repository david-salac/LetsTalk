<template>
  <div class="l-ul">
    <div :class='["l-item", concern.creator]' v-for="concern in concerns" :key="concern.id">
      <a
        href="javascript:;"
        @click="$emit('delete-concern', concern.id)"
        class="delete"
        ><i class="fas fa-times"></i
      ></a>
      <h3>
        <a href="javascript:;" @click="$emit('display-edit-concern', concern)"
          >Concern: {{ concern.condition.name }} (level {{ concern.level }})</a
        >
      </h3>
      <p><strong>Symptoms: </strong> {{ concern.symptoms }}</p>
      <p v-if="concern.details">
        <strong>Details: </strong> {{ concern.details }}
      </p>
    </div>
  </div>
</template>

<script>
// This component list concerns and emits delete/update actions
export default {
  name: "Concerns",
  emits: ["delete-concern", "edit-concern", "display-edit-concern"],
  props: {
    concerns: Array,
  },
};
</script>

<style scoped>
.patient {
  background-image: url("../../assets/patient.png");
  background-repeat: no-repeat;
}
.doctor {
  background-image: url("../../assets/doctor.png");
  background-repeat: no-repeat;
}
</style>