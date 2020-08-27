// class-node
function Node(id, label) {
    return {
        id: id,
        label: label,
        degree: 0
    };
}

//class-edge
function Edge(source, sourceSeq, target, targetSeq) {
    return {
        source: source,
        sourceSeq: sourceSeq,
        target: target,
        targetSeq: targetSeq
    };
}

export default { Node, Edge };
