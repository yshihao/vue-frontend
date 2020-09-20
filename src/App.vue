<template>
    <div id="app">
        <el-container style="border: 1px solid #eee">
            <el-aside
                width="200px"
                style="background-color: rgb(238, 241, 246)"
            >
                <el-menu :default-openeds="['1']">
                    <el-menu-item
                        index="1"
                        @click="$router.push('/create_net')"
                    >
                        <span slot="title">
                            <i class="el-icon-message"></i>
                            create network
                        </span>
                    </el-menu-item>
                    <el-menu-item
                        index="2"
                        @click="$router.push('/network_info')"
                    >
                        <span slot="title">
                            <i class="el-icon-menu"></i>
                            network info
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
            <el-main>
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

<style scoped>
/* p {
    background: red;
}
button {
    background: white;
}

* {
    margin: 0%;
    padding: 0%;
}
.size {
    font-size: 100px;
}
.color {
    color: red;
}
.active {
    background: yellow;
} */
</style>
