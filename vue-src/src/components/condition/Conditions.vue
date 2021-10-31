<template>
  <div class="l-ul">
    <div class="l-item" v-for="condition in conditions" :key="condition.id">
      <a
        href="javascript:;"
        @click="$emit('delete-condition', condition.id)"
        class="delete"
        ><i class="fas fa-times"></i
      ></a>
      <h3>
        <a
          href="javascript:;"
          @click="$emit('display-edit-condition', condition)"
          >{{ condition.name }}</a
        >
      </h3>
      <p><strong>Duration: </strong> {{ condition.duration }}</p>
      <p>
        <strong>Clinitian: </strong> {{ condition.doctor.name }} (<em>{{
          condition.doctor.specialism
        }}</em
        >)
      </p>
    </div>
  </div>
</template>

<script>
// This component list conditions and emits delete/update actions
export default {
  name: "Conditions",
  emits: ["delete-condition", "edit-condition", "display-edit-condition"],
  props: {
    conditions: Array,
  },
};
</script>
