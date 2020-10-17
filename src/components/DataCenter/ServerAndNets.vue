<template>
    <div>
        <!-- <h2>
            {{ dataCenter }}
        </h2> -->
        <el-container>
            <el-aside width="200px">
                <el-menu>
                    <el-menu-item
                        v-for="item in servers"
                        :key="item"
                        :index="item"
                    >
                        {{ item }}
                    </el-menu-item>
                    <el-menu-item
                        v-for="item in nets"
                        :key="item"
                        :index="item"
                        @click="$router.push('/network_info/2S/docker_list')"
                    >
                        {{ item }}
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </div>
</template>

<script>
import api from '../../api/api';

export default {
    name: 'ServerAndNets',
    data() {
        return {
            servers: [],
            nets: []
        };
    },
    computed: {
        dataCenter() {
            return this.$route.params['datacenter'];
        }
    },
    mounted() {
        api.getServerAndNets(this.dataCenter)
            .then(res => {
                // console.log(res);
                this.servers = res.data.data.servers;
                this.nets = res.data.data.nets;
            })
            .catch(err => {
                console.log(err);
            });
    }
};
</script>
