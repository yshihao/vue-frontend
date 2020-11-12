<template>
    <div>
        <!-- <div>test</div> -->
        <el-card
            shadow="hover"
            v-for="item in netList"
            :key="item"
            class="net-item"
            @click.prevent.native="handleClick"
        >
            {{ item }}
        </el-card>
    </div>
</template>

<script>
import api from '@/api/api';

export default {
    name: 'NetList',
    props: ['netList'],
    methods: {
        handleClick(e) {
            let clickNetName = e.srcElement.innerHTML.trim();
            /*api.getDockerList(clickNetName).then(res => {
                console.log(res);
            });*/
            // e.srcElement.innerHTML is OK, too.
            // console.log(e.srcElement.firstChild.data);
            this.$router.push('/network_info/' + clickNetName + '/docker_list');
        }
    }
};
</script>

<style lang="less" scoped>
.net-item {
    margin-top: 20px;
}
</style>
