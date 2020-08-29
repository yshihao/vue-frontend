// const nodes = [
//     { id: 'sw-1', degree: 0 },
//     { id: 'sw-2', degree: 0 },
//     { id: 'sw-3', degree: 0 },
//     { id: 'usr-1', degree: 0 },
//     { id: 'usr-2', degree: 0 },
//     { id: 'usr-3', degree: 0 },
//     { id: 'ctr', degree: 0 }
// ];

// const edges = [
//     { source: 'sw-1', sourceSeq: 1, target: 'usr-1', targetSeq: 1 },
//     { source: 'sw-2', sourceSeq: 1, target: 'usr-2', targetSeq: 1 },
//     { source: 'sw-3', sourceSeq: 1, target: 'usr-3', targetSeq: 1 },
//     { source: 'sw-1', sourceSeq: 2, target: 'sw-2', targetSeq: 2 },
//     { source: 'sw-1', sourceSeq: 3, target: 'sw-3', targetSeq: 2 },
//     { source: 'sw-1', sourceSeq: 4, target: 'ctr', targetSeq: 1 }
// ];

//constants
const infos =
    'VERSION: 2\n\
driver: veth\n\
PREFIX: 1S\n\
CONF_DIR: ./config\n\
MY_IMAGE: "tovs:1.1.4"\n\
PUBLISH_BASE: 9005\n\
SUBNET: "10.31.100.0/24"\n\
GATEWAY: "10.31.100.254:\n\
AUX_ADDRESSES:["10.31.100.1", "10.31.100.2"]';

// 勉强算个解耦，烂得一匹
function FormatNode(node2) {
    return '"' + node2.id + ':eth0' + '"';
}

function NodeToString(nodes) {
    var ret = '  - endpoints: [';
    for (var i = 0, len = nodes.length; i < len - 1; ++i) {
        ret += FormatNode(nodes[i]) + ',';
    }
    ret += FormatNode(nodes[len - 1]) + ']';
    return ret;
}

function FormatEdge(edge) {
    return (
        '["' +
        edge.source +
        ':eth' +
        edge.sourceSeq +
        '", "' +
        edge.target +
        ':eth' +
        edge.targetSeq +
        '"]'
    );
}

function EdgeToString(edges) {
    var ret = '';
    for (var i = 0, len = edges.length; i < len; ++i) {
        ret += '  - endpoints: ' + FormatEdge(edges[i]) + '\n';
    }
    return ret;
}

function Links(nodes, edges) {
    var ret = 'links:\n';
    ret += NodeToString(nodes);
    ret += '\n    driver: bridge';
    ret += '\n';
    ret += EdgeToString(edges);
    return ret;
}

function FormatYaml(nodes, edges) {
    var ret = '';
    ret += Links(nodes, edges);
    ret += infos;
    return ret;
}
export default { FormatYaml };

// console.log(FormatYaml(nodes, edges));

// console.log(NodeToString(nodes))
// console.log(EdgeToString(edges))
