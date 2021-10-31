<template>
  <menu>
    <li>
      <a href="javascript:;" @click="$emit('add-new-concern')"
        >Add new concern</a
      >
    </li>
    <li><router-link to="/">Home</router-link></li>
  </menu>
</template>

<script>
// Menu for concerns
export default {
  name: "ConcernMenu",
  emits: ["add-new-concern"],
};
</script>
