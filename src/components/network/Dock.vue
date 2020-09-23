<template>
    <div>
        <el-container>
            <el-header></el-header>
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
                        </template>
                    </el-table-column>
                </el-table>
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
import api from '../../api/api';
import Yaml from 'js-yaml';
import data from '../../pkg/data';
import Graph from '../Graph';

export default {
    name: 'Dock',
    components: { Graph },
    methods: {
        handleClick(row) {
            // console.log(row.name)
            this.$router.push({
                name: 'DeviceInfo',
                params: {
                    deviceName: row.id
                }
            });
        }
    },
    data() {
        return {
            Docklists: [],
            nodes: [],
            edges: []
        };
    },
    created() {
        //console.log(this.$route.params.netName)
        api.getDockerList(this.$route.params.netName).then(res => {
            this.Docklists = res.data.data;
        });
        api.getNetTopo(this.$route.params.netName).then(res => {
            // console.log(res.data.data);
            let nodes_string = res.data.data.match(/(?<=links:\n).*/);
            let nodes_array = Yaml.safeLoad(nodes_string[0])[0].endpoints;
            // console.log(nodes_array);
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
            console.log(nodes);
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
