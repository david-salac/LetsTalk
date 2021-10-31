<template>
  <div id="wrapper">
    <Header />
    <router-view></router-view>
    <Footer />
  </div>
</template>

<script>
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "App",
  components: {
    Header,
    Footer,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
#wrapper {
  margin: auto;
  padding: 0;
  display: block;
  width: 90%;
  max-width: 400px;
}
a {
  color: #2c4f50;
  text-decoration: none;
}
a:hover {
  color: #40b7ad;
  text-decoration: none;
}
/* Style menu */
menu {
  list-style: none;
  padding: 0;
  display: block;
}
menu li a {
  color: white;
  background: #2c4f50;
  padding: 20px;
  display: block;
}
menu li a:hover {
  background: #40b7ad;
  color: white;
}
menu li {
  margin-bottom: 20px;
}
/* Enumeration style */
.l-ul {
  margin: auto;
}
.l-item {
  display: block;
  background: #f1f1f1;
  margin-bottom: 20px;
  box-sizing: border-box;
  padding: 20px;
  text-align: left;
}
.l-item h3 {
  font-size: 110%;
  margin-top: 0;
}
.l-item p:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
}
.l-item .delete i.fas {
  color: red;
}
.l-item .delete {
  float: right;
  display: block;
}
/* Form styling */
form {
  margin: auto;
}
label {
  float: left;
  clear: both;
}
input,
textarea,
select {
  display: block;
  width: 100%;
  margin-bottom: 20px;
  box-sizing: border-box;
  padding: 10px;
}
input[type="submit"],
input[type="button"] {
  color: white;
  background: #2c4f50;
  padding: 20px;
  display: block;
  border: 1px solid 40b7ad;
  box-sizing: border-box;
}
input[type="button"].cancel {
  background: #b74040;
  border: 1px solid #8c4444;
}
</style>
