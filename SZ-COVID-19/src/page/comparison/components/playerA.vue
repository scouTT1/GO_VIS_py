<template>
    <div class="table-container" ref="container">
    </div>
    
</template>

<script>
    //import _ from 'lodash'
    //import PartJSON from '@/data/part'
    //import Scatter from './scatter'
    import eventBus from '../eventBus'

    export default {
        name: 'List',
        data() {
            return {
                data: [],
                height: 200,
            }
        },
        methods: {
            initData() {
                eventBus.$on();
            }
        },
        mounted() {
            this.initData();
        }
    }
</script>

<style lang="less">
    .table-container{
        height: 100%;
    }
</style>