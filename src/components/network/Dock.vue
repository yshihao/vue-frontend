<template>
    <div>
        <el-container>
            <el-header>

            </el-header>
            <el-main >
                <el-table :data="Docklists" border style="width: 100%">
                    <el-table-column prop="id" fixed label="docker id" width="140">
                    </el-table-column>
                    <el-table-column prop="image" label="docker 镜像" width="140">
                    </el-table-column>
                    <el-table-column prop="name" label="docker 名" width="140">
                    </el-table-column>
                    <el-table-column prop="command" label="docker 启用命令" width="120">
                    </el-table-column>
                    <el-table-column prop="created" label="创建时间">
                    </el-table-column>
                    <el-table-column
                        fixed="right"
                        label="操作"
                        width="100">
                        <template slot-scope="scope">
                        <el-button @click="handleClick(scope.row)" type="text" size="small">查看</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-main>
        </el-container>
        
    </div>
</template>

<script>

export default{
    name: 'Dock',
    methods:{
        handleClick(row) {
           // console.log(row.name)
            this.$router.push({name:'DeviceInfo',
            params:{
                id:row.id
            }})
        }
    },
    data() {
        const Docklist = {
            id :"dockerid",
            image: "dockerimage",
            name: "docker1",
            command:"/bin/bash",
            created:"createdtime"
        }
        return {
            Docklists:[Docklist,Docklist]
        };
    }


};


</script>



<style scoped>
.dockValue {
    background-color:cyan,

    
}
</style>