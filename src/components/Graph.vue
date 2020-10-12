<template>
    <div id="mountNode">
        <!-- <button @click="graph.fitView([20])">fits</button> -->
    </div>
</template>
<script>
import G6 from '@antv/g6';
import { mapGetters } from 'vuex';

export default {
    name: 'Graph',
    data() {
        return {
            graph: {},
            colors: { sw: 'steelblue', usr: 'grey', ctr: 'red' }
        };
    },
    computed: {
        datas() {
            // if (this.nodes != []) {
            var nodes = this.nodes;
            nodes.forEach(node => {
                node.size = 40;
                node.style = {
                    lineWidth: 4,
                    fill: '#fff',
                    stroke: this.colors[node.type]
                };
            });
            console.log(this.nodes, this.edges);
            console.log('data complete');
            return {
                nodes: nodes,
                edges: this.edges
            };
        },
        ...mapGetters(['graphHeight', 'graphWidth'])
    },
    watch: {
        datas() {
            // console.log('data changes');
            this.graph.changeData(this.datas);
            // this.graph.refreshLayout();
            // this.graph.fitView(20);
            setTimeout(this.adjustGraph, 300);
        },
        graphHeight() {
            this.graph.changeSize(this.graphWidth, this.graphHeight);
        },
        graphWidth() {
            this.graph.changeSize(this.graphWidth, this.graphHeight);
        }
    },
    methods: {
        adjustGraph() {
            this.graph.fitView(20);
            let zoom = this.graph.getZoom();
            if (zoom > 3) {
                this.graph.zoomTo(3);
            }
            console.log(zoom, this.graph.getZoom());
        }
    },
    props: ['nodes', 'edges'],
    mounted: function() {
        this.graph = new G6.Graph({
            container: 'mountNode',
            width: 1000,
            height: 800,
            // fitView: true,
            // fitViewPadding: 20,
            modes: {
                default: ['drag-canvas', 'drag-node']
            },
            layout: {
                type: 'force',
                linkDistance: 70,
                preventOverlap: true
                // nodeSize: 50,
                // sortBy: 'type',
                // sortStrength: 50
            },
            defaultEdge: {
                size: 1,
                color: '#e3e3e3',
                style: {
                    endArrow: {
                        path: ''
                    }
                }
            }
        });
        // console.log('graph mounted');
        this.graph.data(this.datas);
        this.graph.render();

        // setTimeout(() => {
        //     this.graph.changeSize(this.graphWidth, this.graphHeight);
        // }, 100);
    }
};
</script>
