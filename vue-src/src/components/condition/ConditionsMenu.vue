<template>
  <menu>
    <li>
      <a href="javascript:;" @click="$emit('add-new-condition')"
        >Add new condition</a
      >
    </li>
    <li><router-link to="/">Home</router-link></li>
  </menu>
</template>

<script>
// Menu for conditions
export default {
  name: "ConditionsMenu",
  emits: ["add-new-condition"],
};
</script>
