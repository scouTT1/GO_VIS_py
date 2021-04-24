<template>
    <div class="heatmap">
        <el-select v-model="default_value" filterable clearable placeholder="请选择" size="mini" class="btn" @change="handleChange">
            <el-option
                v-for="(item,index) in player_other"
                :label="item.name_zh"
                :key="index"
                :value="item">
            </el-option>
        </el-select>
        <div id="chart"></div>
    </div>
</template>

<script>
    import PlayerData from '@/data/player_all_list.json'
    import MatchData from '@/data/match_pair_index.json'
    import eventBus from '../eventBus'
    import * as echarts from 'echarts';
    import 'echarts/extension/bmap/bmap'
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
                default_value: '',
                matches_pair: undefined,
                win_lose_pair: undefined,
            }
        },
        methods: {
            generateData(){
                this.data=[];
                this.days=[];
                this.hours=[];
                for (var i = 0; i < this.player_label.length; i++){
                    this.days.push(this.player_label[i].name_zh);
                    this.hours.push(this.player_label[i].name_zh);
                    for (var j = 0; j < this.player_label.length; j++){
                        if (i==j){
                            this.data.push([i,j,'-']);
                        }else{
                            var temp=this.player_label[i].name_zh+"::"+this.player_label[j].name_zh;
                            var n1=this.matches_pair[temp]==undefined?0:this.matches_pair[temp];
                            this.data.push([i,j,n1]);
                            if (n1>this.num_max){
                                this.num_max=n1;
                            }
                        }
                    }
                }
            },
            draw(){
                var chartDom = document.getElementById('chart');
                var option;
                this.generateData();
                var chart_data = this.data;
                var temp=this;

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
                        min: 0,
                        max: this.num_max,
                        calculable: true,
                        orient: 'horizontal',
                        left: 'center',
                        bottom: '15%',
                        color: ['#FF4E51','#FC9039','#F9D423','#EDE574','#EEF563'],
                        //color:['#d73027','#fc8d59','#fee08b','#ffffbf','#d9ef8b','#91cf60','#1a9850']
                    },
                    series: [{
                        name: '净胜',
                        type: 'heatmap',
                        data: chart_data,
                        label: {
                            color: "#000000",
                            fontSize: 15,
                            show: true
                        },
                        tooltip: {
                            formatter: function (val){
                                var p1=temp.player_label[parseInt(val.value[1])].name_zh;
                                var p2=temp.player_label[parseInt(val.value[0])].name_zh;
                                var num=temp.win_lose_pair[p1+"::"+p2];
                                if(num>0){
                                    return [
                                    "<span style='font-weight:15'>"+p1+'</span>',
                                    '<span style="color:#FF603F">净胜</span>',
                                    "<span style='font-weight:15'>"+p2+'</span><hr size=1 style="margin: 3px 0">',
                                    num,'局'].join('');
                                }else if(num<0){
                                    return [
                                    "<span style='font-weight:15'>"+p1+'</span>',
                                    '<span style="color:#36FA53">净负</span>',
                                    "<span style='font-weight:15'>"+p2+'</span><hr size=1 style="margin: 3px 0">',
                                    -num,'局'].join('');
                                }
                            },
                            backgroundColor: 'rgba(50,50,50,0.7)',
                            borderColor: '#FAF41F',
                            textStyle: {
                                fontSize: 18,
                            }
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
                this.matches_pair=MatchData.match_pair;
                this.win_lose_pair=MatchData.win_lose_pair;
                for (var i=0; i<this.playerdata.length; i++){
                    if(this.playerdata[i].match_list.length == 0){
                        continue;
                    }
                    if(this.player_label.length<this.default_num){
                        this.player_label.push(this.playerdata[i]);
                    }else{
                        this.player_other.push(this.playerdata[i]);
                    }
                }
                this.draw()
                var that = this;
                this.myChart.on('click',function(params){
                    if (params.componentType == "series"){
                        // params.value[0]\[1]\[2] ,纵向 横向 值
                        eventBus.$emit('player_compare_info',{
                            player_a: that.player_label[params.value[1]],
                            player_b: that.player_label[params.value[0]]
                        });
                    }else if(params.componentType=="xAxis" || params.componentType=="yAxis"){
                        that.$confirm("确认从图中删除"+params.value+"?",'提示',{
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'})
                            .then(() => {
                                that.$message({
                                    type: 'success',
                                    message: '删除成功!'
                                });
                                for (var i=0; i<that.player_label.length; i++){
                                    if (that.player_label[i].name_zh==params.value){
                                    that.player_other.push(that.player_label[i]);  //添加到备选框中
                                    that.player_label.splice(i,1);
                                    break;
                                    }
                                }
                                that.draw();
                            }).catch(() => {
                                that.$message({
                                    type: 'info',
                                    message: '已取消删除'
                                })
                            });
                    }
                });
            },
            handleChange(item){
                if (item!=""){
                    // 不是清空操作
                    this.default_value=item.name_zh;
                    var temp_index=-1;
                    for (var i=0; i<this.player_other.length; i++){
                        if (item.name_zh==this.player_other[i].name_zh){
                            temp_index=i;
                            break;
                        }
                    }
                    if (temp_index!=-1){
                        this.player_label.push(item);
                        this.player_other.splice(temp_index,1);
                    }
                    this.draw();
                }
            }
        },
        mounted() {
            this.initData();
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