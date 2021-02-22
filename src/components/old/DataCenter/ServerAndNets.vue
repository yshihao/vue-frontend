<template>
    <div v-show="dataCenterVisible">
        <!-- <h2>
            {{ dataCenter }}
        </h2> -->
        <el-container class="body-container">
            <el-aside width="200px" class="body-aside">
                <el-menu>
                    <el-menu-item
                        v-for="item in servers"
                        :key="item"
                        :index="item"
                        @click="handleServerClick(item)"
                    >
                        {{ item }}
                    </el-menu-item>
                    <el-menu-item
                        v-for="item in nets"
                        :key="item"
                        :index="item"
                        @click="handleNetClick(item)"
                    >
                        {{ item }}
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <Net v-show="netVisible" :Docklists="Docklists2"></Net>
                <Serverdock
                    v-show="serverVisible"
                    :Docklists="Docklists"
                ></Serverdock>
            </el-main>
        </el-container>
    </div>
</template>

<script>
import api from '@/api/api';
import Net from './Net';
import Serverdock from './Server';

export default {
    name: 'ServerAndNets',
    components: { Net, Serverdock },
    props: ['servers', 'nets', 'dataCenterVisible'],
    data() {
        return {
            netVisible: false,
            serverVisible: false,
            Docklists: [],
            Docklists2: []
        };
    },
    computed: {
        dataCenter() {
            return this.$route.params['datacenter'];
        }
    },
    methods: {
        handleServerClick(item) {
            this.netVisible = false;
            this.serverVisible = true;
            api.getDockerList(item, 1, 'phy').then(res => {
                this.Docklists = res.data.data;
                // console.log(this.Docklists)
            });
        },
        handleNetClick(item) {
            this.serverVisible = false;
            this.netVisible = true;
            api.getDockerList(item, 1, 'net').then(res => {
                this.Docklists2 = res.data.data;
                // console.log(this.Docklists2)
            });
        }
    },

    mounted() {
        //从交给router => 组件形式
        // api.getServerAndNets(this.dataCenter)
        //     .then(res => {
        //         // console.log(res);
        //         this.servers = res.data.data.servers;
        //         this.nets = res.data.data.nets;
        //     })
        //     .catch(err => {
        //         console.log(err);
        //     });
    }
};
</script>

<style lang="less" scoped>
.body-container {
    min-height: 800px;
    .body-aside {
        background-color: #efefef;
    }
}
</style>
