<template>

</template>

<script>
    import * as d3 from 'd3';
    export default {
        name: 'heatmap',
        mounted() {
            console.log("123");
            this.initData();
        },
        methods: {
            initData() {

            }
        },
};
</script>

<style>
.path{
    fill: yellow;
    stroke-width: 10px;
}
.line{
    stroke: red;
    fill: orange;
    stroke-width:10px;
}
.svg{
    margin: 25px;
    background-color: white;
}
.g{
    background-color: white;
}
</style>