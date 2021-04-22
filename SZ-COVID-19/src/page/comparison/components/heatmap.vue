<template>
    <div class="heatmap">
        <el-dropdown class="btn">
            <el-button type="primary" size="mini">
                增<i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <template #dropdown>
                <el-dropdown-menu>
                    <el-dropdown-item 
                        v-for="(item, index) in player_other"
                        @click.native="handleClick(item,index)">{{item.name_zh}}
                    </el-dropdown-item>
                </el-dropdown-menu>
            </template>
        </el-dropdown>
        <div id="chart"></div>
        <!--<div class="map_row">
            <el-tag class="small_box_row" 
                closable
                v-for="(item,index) in player_label"
                @close="handleChange(item,index)">{{ item.name_zh }}
            </el-tag>
        </div>
        <div class="map_col">
            <el-tag class="small_box_col" 
                closable
                v-for="(item,index) in player_label"
                @close="handleChange(item,index)">{{ item.name_zh }}
            </el-tag>
        </div>-->
    </div>
</template>

<script>
    import * as echarts from 'echarts';
    import 'echarts/extension/bmap/bmap'
    import PlayerData from '@/data/player'
    export default {
        name: 'heatmap',
        components: {},
        data() {
            return {
                playerdata: [],
                default_num: 3,
                player_label: [],
                player_other: [],
                days:[],
                hours:[],
                data:[],
                num_max: 1,
            }
        },
        mounted() {
            //console.log("123");
            this.initData();
        },
        methods: {
            computeWinData(player1,player2){
                var name2=player2.name_zh;
                var num_win=0;
                var num_lose=0;
                for (var i = 0; i < player1.match_list.length; i++){
                    if(player1.match_list[i].opponent_name==name2){
                        if (player1.match_list[i].my_result=="负"){
                            num_lose++;
                        }else if(player1.match_list[i].my_result=="胜"){
                            num_win++;
                        }
                    }
                }
                return num_win-num_lose;
            },
            generateData(){
                this.data=[];
                this.days=[];
                this.hours=[];
                for (var i = 0; i<this.player_label.length; i++){
                    this.days.push(this.player_label[i].name_zh);
                    this.hours.push(this.player_label[i].name_zh);
                }
                for (var i = 0; i < this.player_label.length; i++){
                    for (var j = 0; j < this.player_label.length; j++){
                        if (i==j){
                            this.data.push([i,j,0]);
                        }else{
                            var temp=this.computeWinData(this.player_label[i],this.player_label[j]);
                            this.data.push([i,j,temp]);
                            if (temp>this.num_max){
                                this.num_max=temp;
                            }
                        }
                    }
                }
            },
            draw(){
                var chartDom = document.getElementById('chart');
                var option;
                this.generateData();
                var chart_data = this.data.map(function (item) {
                    return [item[1], item[0], item[2] || '-'];
                });

                option = {
                    tooltip: {
                        position: 'top'
                    },
                    grid: {
                        height: '60%',
                        width: '80%',
                        top: '12%'
                    },
                    xAxis: {
                        type: 'category',
                        position: 'top',
                        data: this.hours,
                        splitArea: {
                            show: true
                        },
                        axisLabel: {
                            show: true,
                            textStyle: {
                                color: '#c3dbff',  //更改坐标轴文字颜色
                                fontSize : 14,      //更改坐标轴文字大小
                            },
                            interval: 0,
                            rotate:-45,//倾斜度 -90 至 90 默认为0
                            margin:8
                        },
                        triggerEvent: true
                    },
                    yAxis: {
                        type: 'category',
                        data: this.days,
                        inverse: true,
                        splitArea: {
                            show: true
                        },
                        axisLabel: {
                            show: true,
                            textStyle: {
                                color: '#c3dbff',  //更改坐标轴文字颜色
                                fontSize : 14      //更改坐标轴文字大小
                            }
                        },
                        triggerEvent: true
                    },
                    visualMap: {
                        min: -1*this.num_max,
                        max: this.num_max,
                        calculable: true,
                        orient: 'horizontal',
                        left: 'center',
                        bottom: '15%'
                    },
                    series: [{
                        name: 'Punch Card',
                        type: 'heatmap',
                        data: chart_data,
                        label: {
                            show: true
                        },
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowColor: 'rgba(0, 0, 0, 0.5)'
                            }
                        }
                    }]
                };
                this.myChart = echarts.init(chartDom);
                this.myChart.setOption(option);

            },
            initData() {
                this.playerdata=PlayerData;
                for (var i=0; i<this.playerdata.length; i++){
                    if(i<this.default_num){
                        this.player_label.push(this.playerdata[i]);
                    }else{
                        this.player_other.push(this.playerdata[i]);
                    }
                };
                this.draw();
                var temp_label=this.player_label;
                var temp_other=this.player_other;
                var flag=false;
                var myChart=this.myChart;
                var name=this.myChart.on('click',function(params){
                    this.$emit('click')
                    var result=confirm("确认从图中删除"+params.value+"?");
                    if (result){
                        for (var i=0; i<temp_label.length; i++){
                            if (temp_label[i].name_zh==params.value){
                                flag=true;
                                alert(flag);
                                console.log(temp_label);
                                console.log(temp_other);
                                console.log("###############");
                                temp_other.push(temp_label[i]);  //添加到备选框中
                                temp_label.splice(i,1);
                                console.log(temp_label);
                                console.log(temp_other);
                                break;
                            }
                        }
                        
                    }
                    console.log(params.value,name);
                    return params.value;
                });
                console.log(name);
                this.draw();
            },
            handleClick(item,index) {
                this.player_label.push(item);
                this.player_other.splice(index,1);
                this.draw();
            }
        },
};
</script>

<style lang="less">
    .heatmap{
        width: 100%;
        height: 100%;
        .btn{
            float: right;
            .el-dropdown {
                vertical-align: top;
            }
            .el-dropdown + .el-dropdown {
                margin-left: 15px;
            }
            .el-icon-arrow-down {
                font-size: 12px;
            }
        }
        .map_row{
            width: 80%;
            display: flex;
            flex-direction: row;
            text-align: center;
            .small_box_row{
                width: 100%;
                height: 100%;
            }
        }
        .map_col{
            height: 80%;
            width: 5%;
            display: flex;
            flex-direction: column;
            .small_box_col{
                width: 100%;
                height: 100%;
                text-align: center;
                writing-mode: vertical-lr;
            }
        }
    }
</style>