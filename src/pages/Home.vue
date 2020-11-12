
<template>
    <div id="app">
        <el-container style="border: 1px solid #eee" class="body-container">
            <el-header style="text-align: right; font-size: 15px height:100px">
                <el-dropdown>
                    <i class="el-icon-setting" style="margin-right: 15px"></i>
                    <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item>查看</el-dropdown-item>
                    <el-dropdown-item>新增</el-dropdown-item>
                    <el-dropdown-item>删除</el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
                <span>用户名</span>
            </el-header>
            <el-container>
            <el-aside width="250px" class="body-aside">
                <el-menu>
                    <el-menu-item
                        index="1"
                        @click="$router.push('/docker_images')"
                    >
                        <span slot="title">
                            <i class="el-icon-message"></i>
                            名称空间
                        </span>
                    </el-menu-item>
                    <el-submenu index="2">
                        <template slot="title"><i class="el-icon-message"></i>应用程序</template>
                        <el-submenu index="/con">
                        <template slot="title">控制器</template>
                        <el-menu-item @click="$router.push('/home/deploy')">Deployment</el-menu-item>
                        </el-submenu>
                        <el-submenu index="/ddd">
                        <template slot="title">容器组</template>
                        <el-menu-item index="/">选项4-1</el-menu-item>
                        </el-submenu>
                        <el-submenu index="/dss">
                        <template slot="title">公布应用</template>
                        <el-menu-item index="/">选项4-1</el-menu-item>
                        <el-menu-item index="/">选项4-2</el-menu-item>
                        </el-submenu>
                        
                    </el-submenu>
                    <el-submenu index="3">
                        <template slot="title"><i class="el-icon-message"></i>资源</template>
                        <el-menu-item
                        index="4"
                        @click="$router.push('/docker_images')"
                        >
                        <span slot="title">
                            <i class="el-icon-message"></i>
                            配置字典
                        </span>
                        </el-menu-item>
                        <el-menu-item
                        index="5"
                        @click="$router.push('/docker_images')"
                        >
                        <span slot="title">
                            <i class="el-icon-message"></i>
                            密文
                        </span>
                        </el-menu-item>
                        
                        
                    </el-submenu>
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
                </el-menu>
            </el-aside>
            <el-main class="body-main">
                <router-view></router-view>
            </el-main>
            </el-container>
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
            background-color:white;
            height: 800px;
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
