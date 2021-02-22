<!-- 
    为主界面
-->

<template>
    <div id="app">
        <el-container style="border: 1px solid #eee" class="body-container">
            <el-header style="text-align: right; font-size: 15px height:100px">
                <el-dropdown size="medium">
                    <span>
                        {{ user }}
                        <i
                            class="el-icon-setting"
                            style="margin-right: 30px;"
                        ></i>
                    </span>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item>查看个人信息</el-dropdown-item>
                        <el-dropdown-item @click.native="lagout">
                            退出
                        </el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
                <span></span>
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
                            <template slot="title">
                                <i class="el-icon-message"></i>
                                应用程序
                            </template>
                            <el-submenu index="/con">
                                <template slot="title">控制器</template>
                                <el-menu-item
                                    @click="$router.push('/home/deploy')"
                                >
                                    Deployment
                                </el-menu-item>
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
                            <template slot="title">
                                <i class="el-icon-message"></i>
                                资源
                            </template>
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
import api from '@/api/api';
export default {
    name: 'App',
    data: function() {
        return {
            user: ''
        };
    },
    methods: {
        ...mapMutations(['updateHeight', 'updateWeight']),
        lagout() {
            console.log('lagout');
            this.$store.commit('del_token');
            this.$router.push('/login');
        }
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
        api.getusername()
            .then(res => {
                this.user = res.data.username;
            })
            .catch(err => {
                console.log(err.response.status);
            });
    }
};
</script>

<style lang="less" scoped>
#app {
    .body-container {
        margin: 0;
        min-height: 800px;
        position: relative;
        .body-aside {
            background-color: white;
            height: 800px;
        }
        .body-main {
            padding: 0;
        }
    }
}
.el-header {
    background-color: #b3c0d1;
    color: #333;
    line-height: 60px;
}
.dropdown-container {
    width: 300px;
}

.el-icon-message {
    position: relative;
    top: -2px;
}
</style>
