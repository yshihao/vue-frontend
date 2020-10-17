<template>
    <div id="app">
        <el-container style="border: 1px solid #eee" class="body-container">
            <el-aside width="200px" class="body-aside">
                <el-menu>
                    <el-menu-item
                        index="1"
                        @click="$router.push('/docker_images')"
                    >
                        <span slot="title">
                            <i class="el-icon-message"></i>
                            Docker Images
                        </span>
                    </el-menu-item>
                    <el-menu-item
                        index="2"
                        @click="$router.push('/data_centers')"
                    >
                        <span slot="title">
                            <i class="el-icon-menu"></i>
                            Data Centers
                        </span>
                    </el-menu-item>
                    <!-- <el-submenu index="3">
                        <template slot="title">
                            <i class="el-icon-setting"></i>
                            关于我们
                        </template>
                        <el-menu-item-group>
                            <el-menu-item index="3-1">我们</el-menu-item>
                            <el-menu-item index="3-2">联系我们</el-menu-item>
                        </el-menu-item-group>
                    </el-submenu> -->
                </el-menu>
            </el-aside>
            <el-main class="body-main">
                <router-view></router-view>
            </el-main>
        </el-container>
    </div>
</template>

<script>
// import VueRouter from 'vue-router';
import { mapMutations } from 'vuex';
export default {
    name: 'App',
    data: function() {
        return {};
    },
    methods: {
        ...mapMutations(['updateHeight', 'updateWeight'])
    },
    //映射为update
    components: {},
    mounted() {
        window.onresize = () => {
            this.$store.commit(
                'updateHeight',
                document.documentElement.clientHeight
            );
            this.$store.commit(
                'updateWidth',
                document.documentElement.clientWidth
            );
        };
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
</style>
