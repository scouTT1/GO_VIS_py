<template>
    <div class="lines-map-container" id="main">

    </div>
</template>

<script>
    import eventBus from '../eventBus';
    //import { extent } from 'd3'
    
    // import echarts from 'echarts/lib/echarts';
    //import 'echarts/lib/chart/line'
    //import * as d3 from 'd3';
    import * as echarts from 'echarts';


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
                    for(var i=0;i<playerInfo.match_list.length;i++){
                        if (playerInfo.match_list[i].opponent_name.indexOf("AlphaGo")!=-1){
                            playerInfo.match_list.splice(i,1);
                            i--;
                        }
                    }
                    this.playerInfo=playerInfo;
                    this.draw(this.playerInfo);
                });
            },
            draw(data1 = ""){
                //console.log("aaadfsfdas")
                //console.log(data1.name_zh);
                //console.log(data1.match_list.length)
                var TimeList=[]
                var ScoreList=[]
                var temp=0;
                var minvalue=9999;
                var maxvalue=-2;
                var tempmatchlist=[];
                Object.assign(tempmatchlist,data1.match_list);
                tempmatchlist.reverse();
                console.log(data1.match_list)
                console.log(tempmatchlist)
                //var average=0;
                //var infolist=['比赛结果','对手姓名','对手性别','对手国籍','对手分数'];
                //var keylist=[3,4,6,7,1]
                var index=-1;
                var i;

                //时间越新字符串的值越大
                /*if(tempmatchlist[0].match_time>tempmatchlist[tempmatchlist.length- 1].match_time){
                    tempmatchlist.reverse();
                }
                console.log(tempmatchlist,data1.match_list);*/
                for(i=0;i<tempmatchlist.length;i++){
                    tempmatchlist[i].my_score>0;
                    index =i;
                    break;
                }


                if(index>=0){
                    temp=tempmatchlist[index].my_score;
                }
                for(i=0;i<data1.match_list.length;i++){
                    // console.log("进入循环")
                    TimeList[i]=tempmatchlist[i].match_time
                    // console.log(TimeList[i])
                    //if(TimeList[i]=="2009-01-11")console.log("2009-01-11"+data1.match_list[i].my_score)
                    if(parseInt(tempmatchlist[i].my_score)<=0){ 
                        //console.log("有问题")                       
                        ScoreList[i]=temp;
                        //average=average+temp;
                        continue;
                    }
                    
                    ScoreList[i]=tempmatchlist[i].my_score
                    temp=ScoreList[i];
                    if(minvalue>ScoreList[i]){
                        minvalue=ScoreList[i];
                    }
                    else if(maxvalue<ScoreList[i]){
                        maxvalue=ScoreList[i];
                    }
                    //console.log(ScoreList[i])
                    //temp=ScoreList[i]
                    //average=average+temp;
                }
                //average=parseInt(average/data1.match_list.length);
                
                //console.log("最小有值点未"+minvalue+" 最大值"+maxvalue);
                //const scale = this.getScales();
                //console.log(data1.name_ch);
                /*const path = d3.line()
                    .x((d, i) => scale.x(i))
                    .y(d => scale.y(d));
                this.line = path(this.data);*/
                var charDom=document.getElementById("main");
                
                //console.log("aaaa"+charDom)
                
                var myChart=echarts.init(charDom)
                var option;
                option={
                    title:{
                        text:"棋手名称:"+data1.name_zh,
                        textStyle:{
                        //文字颜色
                        color:'#ccc',
                        //字体风格,'normal','italic','oblique'
                        fontStyle:'normal',
                        //字体粗细 'normal','bold','bolder','lighter',100 | 200 | 300 | 400...
                        fontWeight:'bold',
                        //字体系列
                        fontFamily:'sans-serif',
                        //字体大小
                        fontSize:18,
                        }
                    },

                    tooltip: {
                        textStyle:{
                            //字体颜色
                            color:'#fff',
                            //字体风格
                            fontStyle:'normal',
                            //字体大小
                            fontWeight:'bold'

                        },
                        trigger: 'axis',
                        //颜色未定
                        backgroundColor:'rgba(50,50,50,0.7)',
                        //边框颜色
                        borderColor:'#333',
                        //边框宽度
                        borderWidth:3,
                        formatter:function(params){
                            var res=""
                            console.log("templist"+tempmatchlist[0].opponent_name)
                            
                            var tempvalue=tempmatchlist[params[0].dataIndex];

                            res+='<p>对局结果:'+tempvalue.my_result+'</p>'
                            res+='<p>对手姓名:'+tempvalue.opponent_name+'</p>'

                            res+='<p>对手国籍:'+tempvalue.opponent_country+'</p>'
                            res+='<p>对手分数:'+tempvalue.opponent_score+'</p>'
                            res+='<p>对手性别:'+tempvalue.opponent_sex+'</p>'
                            res+='<p>起手:'+tempvalue.my_color+'</p>'

                            //console.log(params.value)

                            return res;
                            
                        }
                    },
                    textStyle:{
                        fontSize:15,
                        color:'#fff'
                    },
                    xAxis:{
                        type:'category',
                        data:TimeList

                    },
                    yAxis:{
                        type:'value',
                        min:minvalue-minvalue%100,
                        max:maxvalue+20,
                        splitLine: {
                            show: true,
                            lineStyle: {
                                color: 'rgba(255,255,255,0.01)'
                            }
                        },
                        axisLine: {
                            show: false,
                        },
                        axisTick: {
                            show: false,
                        },
                    },
                   
                    series:[{
                        data:ScoreList,
                        type:'line',
                        smooth:true
                    }],
                    
                    //下方拖动条
                    dataZoom: [{
                        type: 'slider',
                        backgroundColor: 'rgba(31, 108, 117, .1)',
                        fillerColor: 'rgba(18, 38, 106, .6)',
                        height: 15,
                        bottom: 5,
                        left: 'center',
                        borderColor: 'rgba(18, 38, 106, .5)',
                        handleIcon: 'image://data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+PHN2ZyB0PSIxNTkxOTQ4OTgzMzYzIiBjbGFzcz0iaWNvbiIgdmlld0JveD0iMCAwIDEwMjQgMTAyNCIgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHAtaWQ9IjMwMDAwIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiPjxkZWZzPjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+PC9zdHlsZT48L2RlZnM+PHBhdGggZD0iTTUxMiAwYTUxMiA1MTIgMCAxIDAgNTEyIDUxMkE1MTIgNTEyIDAgMCAwIDUxMiAweiBtLTQ0LjQ4IDY1NmE0NC40OCA0NC40OCAwIDEgMS04OS4xMiAwVjM2OGE0NC40OCA0NC40OCAwIDEgMSA4OS4xMiAwdjI4OHogbTE3OC4wOCAwYTQ0LjQ4IDQ0LjQ4IDAgMSAxLTg5LjEyIDBWMzY4YTQ0LjQ4IDQ0LjQ4IDAgMSAxIDg5LjEyIDB2Mjg4eiIgZmlsbD0iIzFlM2ZmYSIgcC1pZD0iMzAwMDEiPjwvcGF0aD48L3N2Zz4=',
                        showDetail: true,
                        start: 0,
                        end: 100,
                        minSpan: 5,
                        textStyle:{
                            color:'#0ff',
                            fontStyle:'normal',
                            fontWeight:'bold'
                        }
                    }]
                };
                this.myChart=myChart;
                this.myChart.setOption(option);
                }
        },
        mounted() {
            this.initMap();
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