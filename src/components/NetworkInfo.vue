<template>
    <div class="network_info">
        <el-container class="container">
            <el-header>
                <el-breadcrumb separator-class="el-icon-arrow-right">
                    <el-breadcrumb-item :to="{ path: '/network_info' }">
                        network list
                    </el-breadcrumb-item>
                </el-breadcrumb>
            </el-header>
            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </div>
</template>

<script>
import api from '../api/api.js';

export default {
    name: 'NetworkInfo',
    data() {
        return {
            netList: []
        };
    },
    mounted() {
        api.getNetworkInfo().then(res => {
            // console.log(res.data.data);
            this.netList.push(...res.data.data);
            // console.log(this.netList);
        });
    }
};
</script>

<style lang="less" scoped>
.network_info {
    max-width: 800px;
    .container {
        min-height: 800px;
        .net-item {
            margin-top: 20px;
        }
    }
}
</style>
