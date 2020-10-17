<template>
    <div>
        <el-container class="body-container">
            <el-aside width="200px" class="body-aside">
                <el-menu>
                    <el-menu-item
                        v-for="item in dataCenters"
                        :key="item"
                        :index="item"
                        @click="handleDataCenterClick(item)"
                    >
                        {{ item }}
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main class="body-main">
                <ServerAndNets
                    :servers="servers"
                    :nets="nets"
                    :dataCenterVisible="dataCenterVisible"
                ></ServerAndNets>
            </el-main>
        </el-container>
    </div>
</template>

<script>
import api from '../api/api';
import ServerAndNets from '../components/DataCenter/ServerAndNets';

export default {
    name: 'DataCenters',
    components: {
        ServerAndNets
    },
    data() {
        return {
            dataCenters: [],

            servers: [],
            nets: [],
            dataCenterVisible: false
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
    },
    methods: {
        handleDataCenterClick(item, e) {
            api.getServerAndNets(item)
                .then(res => {
                    // console.log(res.data.data.servers, res.data.data.nets);
                    this.servers = res.data.data.servers;
                    this.nets = res.data.data.nets;
                    this.dataCenterVisible = true;
                })
                .catch(err => {
                    console.log(err);
                });
        }
    }
};
</script>

<style lang="less" scoped>
.body-container {
    min-height: 800px;
    .body-aside {
        background-color: #e0e0e0;
    }
    .body-main {
        border: 0;
        padding: 0;
    }
}
</style>
