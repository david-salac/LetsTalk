<template>
  <menu>
    <li>
      <a href="javascript:;" @click="$emit('add-new-expectation')"
        >Add new expectation</a
      >
    </li>
    <li><router-link to="/">Home</router-link></li>
  </menu>
</template>

<script>
// Menu for expectations
export default {
  name: "ExpectationMenu",
  emits: ["add-new-expectation"],
};
</script>
