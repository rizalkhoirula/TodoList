<template>
  <div id="sidebar" class="bg-dark text-white" style="min-height: 100vh; width: 250px;">
    <div class="p-4">
      <h2 class="text-center">Dashboard</h2>
      <hr />
      <ul class="nav flex-column">
        <li class="nav-item">
          <router-link to="/home" class="nav-link text-white">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/tasks" class="nav-link text-white">Tasks</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/categories" class="nav-link text-white">Categories</router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
#sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 250px;
}
</style>
