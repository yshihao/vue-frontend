<template>
    <div class="network_info">
        <el-container class="container">
            <el-header>
                <el-breadcrumb separator-class="el-icon-arrow-right">
                    <el-breadcrumb-item :to="{ path: '/network_info/' }">
                        network list
                    </el-breadcrumb-item>
                    <el-breadcrumb-item
                        v-if="netNameActive"
                        :to="{ name: 'DockerList', netName: netName }"
                    >
                        {{ netName }}
                    </el-breadcrumb-item>
                    <el-breadcrumb-item v-if="deviceNameActive">
                        {{ deviceName }}
                    </el-breadcrumb-item>
                </el-breadcrumb>
            </el-header>
            <el-main>
                <router-view :netList="netList"></router-view>
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
    computed: {
        netNameActive() {
            return !!this.$route.params && 'netName' in this.$route.params;
        },
        netName() {
            return this.netNameActive ? this.$route.params.netName : '';
        },
        deviceNameActive() {
            return !!this.$route.params && 'deviceName' in this.$route.params;
        },
        deviceName() {
            return this.deviceNameActive ? this.$route.params.deviceName : '';
        }
    },
    // methods: {
    //     test() {
    //         console.log(this.$route);
    //     }
    // },
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
