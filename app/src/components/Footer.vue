<template>
  <div class="footer-container">
    <RouterLink to="/app" class="p-2">
      <Icon icon="mdi-account" title="Account" class="footer-link" />
    </RouterLink>
    <RouterLink to="/app/settings" class="p-2">
      <Icon icon="mdi-cog" title="Settings" class="footer-link" />
    </RouterLink>

    <RouterLink to="/app/deploy" class="p-2">
      <Icon icon="mdi-rocket" title="Deployments" class="footer-link" />
    </RouterLink>

        <RouterLink to="/app/monitoring" class="p-2">
      <Icon icon="mdi-chart-line" title="Metrics" class="footer-link" />
    </RouterLink>
  </div>
</template>
