<template>
    <div>
        <el-container>
            <el-header>
                <el-row :gutter="20">
                <el-col :span="2">
                    <el-button @click="queryDocker">查询:</el-button>
                </el-col>
                <el-col :span="17">
                    <el-input v-model="input" placeholder="请输入docker名"></el-input>
                </el-col>
                <el-col :span="5">
                    <el-button @click="addDocker">新增</el-button>
                </el-col>
                </el-row>
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
                     <el-table-column fixed="right" label="操作" width="100">
                        <template slot-scope="scope">
                            <el-button
                                @click="handleClick(scope.row)"
                                type="text"
                                size="small"
                            >
                                查看
                            </el-button>
                            <el-button type="text" @click="dialogVisible = true">删除</el-button>
                            <el-dialog
                            title="提示"
                            :visible.sync="dialogVisible"
                            width="30%"
                            :modal-append-to-body='false'
                            >
                            <span>确定删除该docker节点嘛</span>
                            <span slot="footer" class="dialog-footer">
                                <el-button @click="dialogVisible = false">取 消</el-button>
                                <el-button @click="onClick(scope.row)">确 定</el-button>
                            </span>
                            </el-dialog>
                        </template>
                    </el-table-column>
                </el-table>
                 <el-dialog
                        title="增加节点"
                        :visible.sync="adddialogVisible"
                        width="30%"
                        :modal-append-to-body='false'
                        >
                        <el-row :gutter="12">
                            <el-col :span="6">
                                docker id：
                            </el-col>
                            <el-col :span="14">
                                <el-input v-model="dockerid" placeholder="请输入docker id"></el-input>
                            </el-col>
                            <br>
                        </el-row>
                         <el-row :gutter="14">
                            <el-col :span="6">
                                docker 名：
                            </el-col>
                            <el-col :span="14">
                                <el-input v-model="dockername" placeholder="请输入docker名"></el-input>
                            </el-col>
                            <br>
                        </el-row>
                         <el-row :gutter="14">
                            <el-col :span="6">
                                docker 镜像：
                            </el-col>
                            <el-col :span="14">
                                <el-input v-model="dockerimage" placeholder="请输入docker镜像"></el-input>
                            </el-col>
                            <br>
                        </el-row>
                         <el-row :gutter="14">
                            <el-col :span="6">
                                docker 启动命令：
                            </el-col>
                            <el-col :span="14">
                                <el-input v-model="dockercommand" placeholder="请输入docker启动命令"></el-input>
                            </el-col>
                        </el-row>
                        <span slot="footer" class="dialog-footer">
                            <el-button @click="adddialogVisible = false">取 消</el-button>
                            <el-button @click="addonClick">确 定</el-button>
                        </span>
                </el-dialog>
                <el-card class="box-card">
                    <div slot="header" class="clearfix">
                        <span>结点图</span>
                    </div>
                    <Graph :nodes="nodes" :edges="edges"></Graph>
                </el-card>
            </el-main>
        </el-container>
    </div>
</template>

<script>
import api from '@/api/api';
import Yaml from 'js-yaml';
import data from '@/pkg/data';
import Graph from '@/components/old/Graph';

export default {
    name: 'Dock',
    components: { Graph },
    props:['Docklists'],
    methods: {
        handleClick(row) {
            // console.log(row.name)
            this.$router.push({
                name: 'DeviceInfo',
                params: {
                    deviceName: row.id
                }
            });
        },
         onClick(row) {
            this.dialogVisible = false;
            console.log(row.name)
        },
        queryDocker() {
            //this.Docklists = ""
            console.log(this.input)
        },
        addDocker() {
            this.adddialogVisible = true
        },
        addonClick() {
            this.adddialogVisible = false;
            console.log(this.dockername)
        },
        search(keyword) {
            var newlist =[]
            this.Docklists.forEach(item=>{
                if(item.name.indexOf(keyword)!=-1) {
                    newlist.push(item)
                }
            })
            return newlist
        }
    },
    data() {
        return {
            nodes: [],
            edges: [],
            dialogVisible:false,
            adddialogVisible:false,
            input:"",
            
            dockerid:"",
            dockerimage:"",
            dockername:"",
            dockercommand:"",

        };
    },
    created() {
        api.getNetTopo(this.$route.params.netName).then(res => {
            console.log(res.data.data);
            let nodes_string = res.data.data.match(/(?<=links:\n).*/);
            //console.log(nodes_string);
            let nodes_array = Yaml.safeLoad(nodes_string[0])[0].endpoints;
            console.log(nodes_array);
            let nodes = [];
            for (let i of nodes_array) {
                let id = i.match(/\w+-\d+/);
                let type = i.match(/\w+/);
                // console.log(id, type);
                nodes.push(data.Node(id[0], type[0], id[0]));
            }
            let edges_string = res.data.data.match(
                /(?<=bridge\n)(.*\s)+(?=VERSION)/
            );
            console.log(edges_string)
            let edges_array = Yaml.safeLoad(edges_string[0]);
            let edges = [];
            for (let i of edges_array) {
                edges.push(
                    data.Edge(
                        i.endpoints[0].match(/\w+-\d+/)[0],
                        0,
                        i.endpoints[1].match(/\w+-\d+/)[0],
                        0
                    )
                );
                // console.log(i.endpoints[0], i.endpoints[1]);
            }
            this.nodes = nodes;
            this.edges = edges;
            // console.log(Yaml.safeLoad(edges_string[0]));
            // console.log(edges);
            // let json = Yaml.safeLoad(res.data.data);
            // console.log(json);
        });
    }
};
</script>

<style scoped>
.dockValue {
    background-color: cyan;
}
</style>
