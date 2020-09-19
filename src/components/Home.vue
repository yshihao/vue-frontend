<template>
    <div>
        <el-container style="border: 1px solid #eee">
            <el-aside
                width="200px"
                style="background-color: rgb(238, 241, 246)"
            >
                <el-menu :default-openeds="['1', '3']">
                    <el-menu-item index="1">
                        <span slot="title">
                            <i class="el-icon-message"></i>
                            管理结点
                        </span>
                    </el-menu-item>
                    <el-submenu index="2">
                        <template slot="title">
                            <i class="el-icon-menu"></i>
                            docker结点
                        </template>
                        <el-menu-item-group>
                            <el-menu-item index="2-1">查看</el-menu-item>
                            <el-menu-item index="2-2">查询</el-menu-item>
                        </el-menu-item-group>
                    </el-submenu>
                    <el-submenu index="3">
                        <template slot="title">
                            <i class="el-icon-setting"></i>
                            关于我们
                        </template>
                        <el-menu-item-group>
                            <el-menu-item index="3-1">我们</el-menu-item>
                            <el-menu-item index="3-2">联系我们</el-menu-item>
                        </el-menu-item-group>
                    </el-submenu>
                </el-menu>
            </el-aside>

            <el-container class="mainBody">
                <el-header
                    class="bodyHeader"
                    style="text-align: right; font-size: 20px"
                >
                    <el-page-header content="详情页面"></el-page-header>
                </el-header>

                <el-main class="bodyBody">
                    <div class="buttonGroup">
                        <el-row>
                            <el-button
                                type="primary"
                                round
                                @click.prevent.native="
                                    addNodeDialogVisible = true
                                "
                            >
                                增加结点
                            </el-button>
                            <el-button
                                type="primary"
                                round
                                @click.prevent.native="
                                    addEdgeDialogVisible = true
                                "
                            >
                                增加边
                            </el-button>
                            <el-button
                                type="primary"
                                round
                                @click="handleSubmit"
                            >
                                提交
                            </el-button>
                        </el-row>
                    </div>
                    <el-card class="box-card">
                        <div slot="header" class="clearfix">
                            <span>结点图</span>
                        </div>
                        <Graph :nodes="nodes" :edges="edges"></Graph>
                    </el-card>
                    <el-dialog
                        title="增加节点"
                        :visible.sync="addNodeDialogVisible"
                    >
                        <el-input
                            v-model="nodeLabel"
                            placeholder="NodeName"
                        ></el-input>
                        <el-select v-model="nodeType" placeholder="NodeType">
                            <el-option
                                v-for="item in nodeTypes"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value"
                            ></el-option>
                        </el-select>
                        <span slot="footer">
                            <el-button @click="addNodeDialogVisible = false">
                                cancel
                            </el-button>
                            <el-button @click="handleAddNode">
                                confirm
                            </el-button>
                        </span>
                    </el-dialog>
                    <el-dialog
                        title="增加边"
                        :visible.sync="addEdgeDialogVisible"
                    >
                        <div class="nodeSelectors">
                            <el-row>
                                <el-select
                                    v-model="sourceNode"
                                    placeholder="请选择结点1"
                                    value-key="id"
                                >
                                    <el-option
                                        v-for="node in availableSourceNodes"
                                        :key="node.id"
                                        :label="node.label"
                                        :value="node"
                                    ></el-option>
                                </el-select>
                                <el-select
                                    v-model="targetNode"
                                    placeholder="请选择结点2"
                                    value-key="id"
                                >
                                    <el-option
                                        v-for="node in availableTargetNodes"
                                        :key="node.id"
                                        :label="node.label"
                                        :value="node"
                                    ></el-option>
                                </el-select>
                            </el-row>
                        </div>
                        <span slot="footer" class="dilog-footer">
                            <el-button @click="addEdgeDialogVisible = false">
                                cancel
                            </el-button>
                            <el-button @click="handleAddEdge">
                                confirm
                            </el-button>
                        </span>
                    </el-dialog>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script>
import data from '../pkg/data';
import format from '../pkg/format';
import api from '../api/api';
import Graph from './Graph';

export default {
    name: 'Home',
    components: { Graph: Graph },
    data: function() {
        return {
            //dialog tags
            addNodeDialogVisible: false,
            addEdgeDialogVisible: false,

            //nodes
            nodes: [],
            nodeSw: 0,
            nodeUsr: 0,
            nodeCtr: 0,
            nodeLabel: '',
            nodeTypes: [
                { value: 'sw', label: 'switch' },
                { value: 'usr', label: 'user' },
                { value: 'ctr', label: 'control' }
            ],
            nodeType: '',

            //edges
            edges: [],
            sourceNode: {},
            targetNode: {}
        };
    },
    computed: {
        // prevent the single-node-circle in the graph
        availableSourceNodes() {
            return this.nodes.filter(node => {
                return node !== this.targetNode;
            });
        },
        availableTargetNodes() {
            return this.nodes.filter(node => {
                return node !== this.sourceNode;
            });
        }
    },
    methods: {
        handleAddEdge() {
            if (!('id' in this.sourceNode) || !('id' in this.targetNode)) {
                this.$message.error('Empty input!');
                return;
            }
            this.edges.filter(edge => {
                if (
                    (edge.source === this.sourceNode.id &&
                        edge.target === this.targetNode.id) ||
                    (edge.source === this.targetNode.id &&
                        edge.target === this.sourceNode.id)
                ) {
                    this.$message.error('This edge already exists!');
                    return;
                }
            });
            this.sourceNode.degree++;
            this.targetNode.degree++;
            this.edges.push(
                data.Edge(
                    this.sourceNode.id,
                    this.sourceNode.degree,
                    this.targetNode.id,
                    this.targetNode.degree
                )
            );
            // console.log(this.edges);
            this.addEdgeDialogVisible = false;
        },
        handleAddNode() {
            var node_id;
            switch (this.nodeType) {
                case 'sw':
                    node_id = 'sw-' + ++this.nodeSw;
                    break;
                case 'usr':
                    node_id = 'usr-' + ++this.nodeUsr;
                    break;
                case 'ctr':
                    node_id = 'ctr-' + ++this.nodeCtr;
                    break;
            }
            this.nodes.push(data.Node(node_id, this.nodeType, this.nodeLabel));
            // console.log(this.nodes);
            this.addNodeDialogVisible = false;
        },
        handleSubmit() {
            if (this.nodes.length === 0) {
                this.$message.error('Nothing to submit!');
            } else {
                var formattedFile = format.FormatYaml(this.nodes, this.edges);
                console.log(formattedFile);
                api.sendYaml(formattedFile).then(res => {
                    console.log(res);
                });
            }
        }
    }
};
</script>

<style lang="less" scoped>
.mainBody {
    .bodyHeader {
        // text-align: right;
        // font-size: 20px;
        background-color: #b3c0d1;
        color: #333;
        line-height: 60px;
    }
    .bodyBody {
        .buttonGroup {
            margin-bottom: 20px;
        }
        .box-card {
            // width: 1300px;
            // height: 700px;
        }
    }
}

// .el-aside {
//     color: #333;
// }
// .text {
//     font-size: 14px;
// }

// .item {
//     margin-bottom: 18px;
// }

.clearfix:before,
.clearfix:after {
    display: table;
    content: '';
}
.clearfix:after {
    clear: both;
}
</style>
