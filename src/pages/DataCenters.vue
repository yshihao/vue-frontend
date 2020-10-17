<template>
    <el-container>
        <el-aside width="200px">
            <el-menu text-color="#000000">
                <el-menu-item
                    v-for="item in dataCenters"
                    :key="item"
                    :index="item"
                    @click="$router.push('/data_centers/' + item)"
                >
                    {{ item }}
                </el-menu-item>
            </el-menu>
        </el-aside>
        <el-main class="body-main">
            <router-view></router-view>
        </el-main>
    </el-container>
</template>

<script>
import api from '../api/api';

export default {
    name: 'DataCenters',
    data() {
        return {
            dataCenters: []
        };
    },
    mounted() {
        api.getDataCenters()
            .then(res => {
                // console.log(res);
                this.dataCenters = res.data.data;
            })
            .catch(err => {
                console.log(err);
            });
    }
};
</script>

<style lang="less" scoped>
.body-main {
    border: 0;
}
</style>
