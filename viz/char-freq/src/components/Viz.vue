<template>
  <div>
    <View3D
      ref="view3d"
      src="blocks.glb"
      @ready="this.onReady"
    />
  </div>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import { View3D } from "@egjs/vue3-view3d";
export default defineComponent({
  components: {
    View3D
  },
  methods: {
    onReady: evt => {
      evt.target.animator.play(1);
      console.log("clicked")
    },
    onClick: function() {
      console.log("clicked");
      this.$refs.view3d.animator.play(2);
    }
  }
})
</script>
<style scoped>


canvas.view3d-canvas {
  width: 100%;
  height: 100vh;
}
/* .view3d-wrapper {
  width: 100%;
  height: 100vh;
} */

</style>