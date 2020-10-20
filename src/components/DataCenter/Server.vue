<template>
    <div>
        <el-container>
             <el-header>  
            </el-header>
            <el-main>
                <el-table :data="Docklists" border style="width: 100%">
                    <el-table-column
                        prop="id"
                        fixed
                        label="docker id"
                        width="140"
                    ></el-table-column>
                    <el-table-column
                        prop="image"
                        label="docker 镜像"
                        width="140"
                    ></el-table-column>
                    <el-table-column
                        prop="name"
                        label="docker 名"
                        width="140"
                    ></el-table-column>
                    <el-table-column
                        prop="command"
                        label="docker 启用命令"
                        width="120"
                    ></el-table-column>
                    <el-table-column
                        prop="created"
                        label="创建时间"
                    ></el-table-column>
                </el-table>
            </el-main>
        </el-container>
    </div>
</template>

<script>
import api from '../../api/api';
export default {
    name: 'ServerDock',
   // components: { Graph },
    methods: {
        handleClick(row) {
             console.log(row.name)
            this.$router.push({
                name: 'DeviceInfo',
                params: {
                    deviceName: row.id
                }
            });
        },
       
    },
    data() {
       
        return {
            Docklists: []
        };
    },
    created() {
        //console.log(this.$route.params.netName)
        api.getDockerList(this.$route.params.netName).then(res => {
            this.Docklists = res.data.data;
        });
       
    }
};
</script>

<style scoped>
.dockValue {
    background-color: cyan;
}
</style>
