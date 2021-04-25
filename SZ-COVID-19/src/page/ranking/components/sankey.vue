<template>
    <div id="sankey">

    </div>
</template>

<script>
    import echarts from 'echarts/lib/echarts';
    import 'echarts/lib/chart/sankey'
    import history_ranking from "@/data/history_ranking.json"
    /*json文件url，本地的就写本地的位置，如果是服务器的就写服务器的路径*/
    export default {
        name: 'SanKey',
        methods: {
            initChart() {
                var CHlist=[42];
                var JPlist=[42];
                var KOlist=[42];
                var OTlist=[43];
                var i;
                var TimeList=[];
                for(var js in history_ranking){
                    var templist=history_ranking[js];
                    TimeList.push(js.toString()+"-01-01");
                    var CH=0;
                    var JP=0;
                    var KO=0;
                    for(i=0;i<templist.length;i++){
                        if(templist[i].country=="日本"){
                            JP=JP+1;
                        }
                        else if(templist[i].country=="中国"){
                            CH=CH+1;
                        }
                        else if(templist[i].country=="韩国"){
                            KO=KO+1;
                        }
                    }
                    CHlist[parseInt(js)-1980]=CH;
                    JPlist[parseInt(js)-1980]=JP;
                    KOlist[parseInt(js)-1980]=KO;
                    OTlist[parseInt(js)-1980]=100-CH-JP-KO;
                }
                var dataList=[];
                for(i=0;i<42;i++){
                    dataList.push([TimeList[i],CHlist[i],"中国"]);
                }
                for(i=0;i<42;i++){
                    dataList.push([TimeList[i],JPlist[i],"日本"]);
                }
                for(i=0;i<42;i++){
                    dataList.push([TimeList[i],KOlist[i],"韩国"]);
                }
                for(i=0;i<42;i++){
                    dataList.push([TimeList[i],OTlist[i],"其他"]);
                }
                const option={
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'line',
                            lineStyle: {
                                color: 'rgba(0,0,0,0.2)',
                                width: 1,
                                type: 'solid'
                            },
                        },
                    },

                    legend: {
                        data: ['中国', '日本', '韩国', '其他'],
                        textStyle:{
                            //字体颜色
                            color:'#fff',
                            //字体风格
                            fontStyle:'normal',
                            //字体大小
                        },
                    },

                    singleAxis: {
                        top: 50,
                        bottom: 50,
                        axisTick: {},
                        axisLabel: {},
                        type: 'time',
                        axisPointer: {
                            animation: true,
                            label: {
                                show: true
                            }
                        },
                        splitLine: {
                            show: true,
                            lineStyle: {
                                type: 'dashed',
                                opacity: 0.2
                            }
                        }
                    },
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
                        textStyle:{
                            color:'#0ff',
                            //字体风格
                            fontStyle:'normal',
                            //字体大小
                            fontWeight:'bold'
                        }
                    }] ,

                    series: [{
                        type: 'themeRiver',
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 20,
                                shadowColor: 'rgba(0, 0, 0, 0.8)'
                            }
                        },
                        color:['#ff0000','#dec674','#6495ED','#8A2BE2'],
                        data: dataList
                    }]
                };
                const myChart = echarts.init(document.getElementById('sankey'), 'light');
                myChart.setOption(option)
            }
        },
        mounted() {
            setTimeout(this.initChart);
        }
    }
</script>

<style lang="less" scoped>
    #sankey{
        height: 600px;
    }
</style>