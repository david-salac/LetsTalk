<template>
  <div class="l-ul">
    <div class="l-item" v-for="expectation in expectations" :key="expectation.id">
      <a
        href="javascript:;"
        @click="$emit('delete-expectation', expectation.id)"
        class="delete"
        ><i class="fas fa-times"></i
      ></a>
      <h3>
        <a href="javascript:;" @click="$emit('display-edit-expectation', expectation)"
          >{{ expectation.name }} (condition: {{ expectation.condition.name }})</a
        >
      </h3>
      <p v-if="expectation.details">
        <strong>Details: </strong> {{ expectation.details }}
      </p>
    </div>
  </div>
</template>

<script>
// This component list expectations and emits delete/update actions
export default {
  name: "Expectations",
  emits: ["delete-expectation", "edit-expectation", "display-edit-expectation"],
  props: {
    expectations: Array,
  },
};
</script>
