<template>
    <div class="table-container" ref="container">
        <el-tabs v-model="activeName" class="tab">
            <el-tab-pane label="个人信息" name="first" class="tab-item1">
                <ul>
                    <li>姓名：{{player_b.name_zh}}</li>
                    <li>性别：{{player_b.sex}}</li>
                    <li>地区：{{player_b.country}}</li>
                    <li>对局数：{{num_all_matches}}</li>
                    <li>胜率：{{win_rate}}</li>
                    <li>执黑胜率：{{black_win_rate}}</li>
                    <li>执白胜率：{{white_win_rate}}</li>
                </ul>
            </el-tab-pane>
            <el-tab-pane label="对局信息" name="second" class="tab-item2">
                <ul>
                    <li v-for="item in matchList" 
                        v-bind:key="item">
                            <div style="width: 70%">{{item.match_name}}</div>
                            <div>{{item.my_color}}</div>
                            <div>{{item.my_result}}</div>
                            <div>{{item.result_info}}</div>
                    </li>
                </ul>
            </el-tab-pane>
        </el-tabs>
    </div>
    
</template>

<script>
    //import _ from 'lodash'
    //import PartJSON from '@/data/part'
    import eventBus from '../eventBus'

    export default {
        name: 'List',
        data() {
            return {
                player_b: [],
                matchList: [],
                num_all_matches: undefined,
                win_rate: undefined,
                black_win_rate: undefined,
                white_win_rate: undefined,
                activeName: 'first',
            }
        },
        methods: {
            initData() {
                eventBus.$on('player_compare_info',({player_a,player_b})=>{
                    this.player_a=player_a;
                    this.player_b=player_b;
                    this.num_all_matches=this.player_b.match_list.length;
                    this.matchList=[];
                    var bl_win=0;
                    var wh_win=0;
                    var bl_num=0;
                    var wh_num=0;
                    for(var i = 0; i < this.player_b.match_list.length; i++){
                        if (this.player_b.match_list[i].opponent_name==this.player_a.name_zh){
                            const r_info=this.player_b.match_list[i].result_info
                            if (r_info=='R'){
                                this.player_b.match_list[i].result_info='中盘';
                            }else if(r_info=='T'){
                                this.player_b.match_list[i].result_info='超时';
                            }else if(!isNaN(Number(r_info))){
                                this.player_b.match_list[i].result_info=r_info+'目';
                            }
                            this.matchList.push(this.player_b.match_list[i])
                        }
                        if (this.player_b.match_list[i].my_color=="执黑"){
                            if(this.player_b.match_list[i].my_result=="胜"){
                                bl_win+=1;
                            }
                            bl_num+=1;
                        }else if(this.player_b.match_list[i].my_color=="执白"){
                            if(this.player_b.match_list[i].my_result=="胜"){
                                wh_win+=1;
                            }
                            wh_num+=1;
                        }
                    }
                    function toPercent(point) {
                        var str = Number(point * 100).toFixed(2);
                        str += "%";
                        return str;
                    }
                    this.win_rate=toPercent((wh_win+bl_win)/this.player_b.match_list.length);
                    this.black_win_rate=toPercent(bl_win/bl_num);
                    this.white_win_rate=toPercent(wh_win/wh_num);
                });
            }
        },
        mounted() {
            this.initData();
        }
    }
</script>

<style lang="less">
    .el-tabs__item{
        color:white;
    }
    .table-container{
        height: 100%;
        width: 100%;
        .tab{
            width: 100%;
            .tab-item1{
                width: 100%;
                display: inline-block;
                ul {
                    padding-left: 0;
                    color: #aaa;
                    list-style-type: none;
                    font-size: 14px;
                    li {
                        display: flex;
                        justify-content: space-between;
                        border-bottom: 1px dotted #224ac0;
                        line-height: 2.5em;
                        span:nth-last-child(1) {
                            margin-right: 10px;
                        }
                    }
                }
            }
            .tab-item2{
                width: 100%;
                display: inline-block;
                color: #C8291C;
                ul {
                    padding-left: 0;
                    color: #aaa;
                    list-style-type: none;
                    font-size: 14px;
                    li {
                        display: flex;
                        justify-content: space-between;
                        border-bottom: 1px dotted #224ac0;
                        line-height: 2.5em;
                        span:nth-last-child(1) {
                            margin-right: 10px;
                        }
                    }
                }
            }
        }
    }
</style>