<template>
    <div id="app">
        <router-view></router-view>
    </div>
</template>

<script>
export default {
    name: 'App',
    data: function() {
        return {};
    }
};
</script>

<style lang="less" scoped>
#app {
    .body-container {
        min-height: 800px;
        position: relative;
        .body-aside {
            background-color: #dddddd;
        }
        .body-main {
            padding: 0;
        }
    }
}
.el-header {
    background-color: #B3C0D1;
    color: #333;
    line-height: 60px;
  }
</style>
