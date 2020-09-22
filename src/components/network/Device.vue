<template>
    <div>
        <el-row>
            <div style="text-align:center">
                <el-col>Device 详细信息</el-col>
                <br />
                <br />
                <p>
                    <label>Architecture:</label>
                    <input type="text" v-model="arch" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>CPU op-mode(s):</label>
                    <input type="text" v-model="cpuop" disabled="true" />
                    <br />
                </p>

                <p>
                    <label>Byte Order:</label>
                    <input type="text" v-model="byteorder" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>CPU(s):</label>
                    <input type="text" v-model="cpus" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>
                        On-line CPU(s) list:
                    </label>
                    <input type="text" v-model="cpulist" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>Thread(s) per core:</label>
                    <input
                        type="text"
                        v-model="threadpercore"
                        disabled="true"
                    />
                    <br />
                </p>
                <p>
                    <label>Core(s) per socket:</label>
                    <input type="text" v-model="corepersoc" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>Socket(s):</label>
                    <input type="text" v-model="socket" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>NUMA node(s):</label>
                    <input type="text" v-model="numanode" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>Vendor ID:</label>
                    <input type="text" v-model="vendorid" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>CPU family:</label>
                    <input type="text" v-model="cpuf" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>Model:</label>
                    <input type="text" v-model="model" disabled="true" />
                    <br />
                </p>

                <p>
                    <label>Model name:</label>
                    <input type="text" v-model="modelname" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>Stepping:</label>
                    <input type="text" v-model="stepping" disabled="true" />
                    <br />
                </p>

                <p>
                    <label>CPU Mhz:</label>
                    <input type="text" v-model="cpumhz" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>CPU mx MHz:</label>
                    <input type="text" v-model="cpumaxhz" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>CPU min MHz:</label>
                    <input type="text" v-model="cpuminhz" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>BogoMIPS:</label>
                    <input type="text" v-model="bogomip" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>Virtualiztion:</label>
                    <input type="text" v-model="virtual" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>L1d cache:</label>
                    <input type="text" v-model="l1dcache" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>L1i cache:</label>
                    <input type="text" v-model="l1icache" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>L2 cache:</label>
                    <input type="text" v-model="l2cache" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>L3 cache:</label>
                    <input type="text" v-model="l3cache" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>NUMA node0 CPU(s):</label>
                    <input type="text" v-model="numanode0" disabled="true" />
                    <br />
                </p>
                <p>
                    <label>NUMA node1 CPU(s):</label>
                    <input type="text" v-model="numanode1" disabled="true" />
                    <br />
                </p>
            </div>
        </el-row>
    </div>
</template>
<script>
export default {
    name: 'Ddvice',
    data() {
        return {
            arch: 'x86',
            cpuop: '32 bit',
            byteorder: 'little endian',
            cpus: '20',
            cpulist: 'd',
            threadpercore: '1',
            corepersoc: 10,
            socket: 2,
            numanode: 2,
            vendorid: 'dd',
            cpuf: 6,
            model: 79,
            modelname: 'inter(r) Xeon(R) CPU E5-2630 v4',
            stepping: 1,
            cpumhz: 1200.232,
            cpumaxhz: 2200.0,
            cpuminhz: 1200.0,
            bogomip: 4399.78,
            virtual: 'VT-x',
            l1dcache: '32k',
            l1icache: '32k',
            l2cache: '256k',
            l3cache: '25600k',
            numanode0: '0,2,4',
            numanode1: '1,3,5'
        };
    },
    created() {
        this.id = this.$route.params.id;
        console.log(this.id);
    }
};
</script>

<style scoped>
input {
    font-size: 24px;
    border: none;
    width: 10cm;
    background: white;
    text-align: center;
}
label {
    cursor: pointer;
    display: inline-block;
    padding: 3px 6px;
    text-align: right;
    width: 150px;
    vertical-align: top;
}
</style>
