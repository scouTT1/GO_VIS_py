<template>
    <div class="lines-map-container">
        <svg width="100%" height="100%">
            <g style="transform: translate(0,10px);">
                <path :d="line" />
            </g>
        </svg>
    </div>
</template>

<script>
    import eventBus from '../eventBus';
    //import { extent } from 'd3'
    //import echarts from 'echarts/lib/echarts';
    //import 'echarts/lib/chart/line'
    import * as d3 from 'd3';

    export default {
        name: 'Map',
        data() {
            return {
                playerInfo: [],
                data: [99,71,78,25,36,92],
                line: ''
            }
        },
        methods: {
            initMap() {
                eventBus.$on('selectPlayerInfo',({playerInfo})=>{
                    this.playerInfo=playerInfo
                    //console.log(this.playerInfo.name_zh);
                    this.draw(this.playerInfo);
                });
            },
            getScales() {
                const x = d3.scaleTime().range([0, 430]);
                const y = d3.scaleLinear().range([210, 0]);
                d3.axisLeft().scale(x);
                d3.axisBottom().scale(y);
                x.domain(d3.extent(this.data, (d, i) => i));
                y.domain([0, d3.max(this.data, d => d)]);
                return { x, y };
            },
            draw(data1 = ""){
                console.log(data1.name_en);
                const scale = this.getScales();
                const path = d3.line()
                    .x((d, i) => scale.x(i))
                    .y(d => scale.y(d));
                this.line = path(this.data);
            }
        },
        mounted() {
            this.initMap();
        },
        beforeDestroy() {
        }
    }
</script>

<style lang="less">
    .lines-map-container {
        position: relative;
        padding: 0;
        margin: 0;
        width: 100%;
    }
    .svg{
        margin: 25px;
    }
    .path{
        fill: none;
        stroke: #76BF8A;
        stroke-width: 3px;
    }
</style>