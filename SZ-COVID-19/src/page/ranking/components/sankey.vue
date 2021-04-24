<template>
    <div id="sankey">

    </div>
</template>

<script>
    import _ from 'lodash'
    import echarts from 'echarts/lib/echarts';
    import 'echarts/lib/chart/sankey'
    import TrackJSON from '@/data/track'
    // import { scaleLinear } from 'd3'
    console.log("fasdfasdfsdf")
    /*
    window.onload=function(){
        var url="./history_ranking.json";
        var request=new XMLHttpRequest();
        request.open("get",url);
        request.send(null);
        request.onload=function(){
            if(request.status==200){
                var json=JSON.parse(request.responseText);
                console.log(json)
            }
        }

    }*/
    import history_ranking from "./history_ranking.json"

    /*json文件url，本地的就写本地的位置，如果是服务器的就写服务器的路径*/
    //console.log(history_ranking)

    var CHlist=[42];
    var JPlist=[42];
    var KOlist=[42];
    var OTlist=[43];
    var i;
    for(var js in history_ranking){
        var templist=history_ranking[js];
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
    //console.log(CHlist)
    //console.log(JPlist)
    //console.log(KOlist)
    //console.log(OTlist)
    //var ttlist=[];
    var TimeList=[42];
    for(i=0;i<42;i++){
        TimeList[i]=(i+1980).toString()+"-01-01";
    }
    //console.log(TimeList)
    var dataList=[[]];
    //var num=0;
    for(i=0;i<42;i++){
        var ttlist=[];
        ttlist[0]=TimeList[i];
        ttlist[1]=CHlist[i];
        ttlist[2]="中国";
        dataList[i]=ttlist;
        
    }
    for(i=0;i<42;i++){
       
        ttlist[0]=TimeList[i];
        ttlist[1]=JPlist[i];
        ttlist[2]="日本";
        dataList[i+42]=ttlist;
        
    }
    for(i=0;i<42;i++){
        
        ttlist[0]=TimeList[i];
        ttlist[1]=KOlist[i];
        ttlist[2]="韩国";
        dataList[i+84]=ttlist;
        
    }
    for(i=0;i<42;i++){
       
        ttlist[0]=TimeList[i];
        ttlist[1]=OTlist[i];
        ttlist[2]="其他";
        dataList[i+126]=ttlist;
        
    }
    console.log(dataList);
    const DIM = ['age_range', 'xb','period','origin', 'tran', ]
    const ITEM_STYLE = {
        xb(){
            return {
                '男': {
                    color: '#3a7ba5',
                },
                '女': {
                    color: '#9d4da7',
                },
            }
        }
    }

    const TRAN_ORDER = {
        '私家/专车': 0,
        '出租车': 1,
        '3A109航船': 2,
        '深圳湾口岸': 3,
        '航空': 4,
        '不明': 5,
    }

    const SORT_FUN = {
        'age_range': data => {
            return _.orderBy(data, d => {
                switch(d.name) {
                    case '婴幼儿/青少年(0~15)': return 0
                    case '青年(16~30)': return 1
                    case '中青年(30~45)': return 2
                    case '中年(45~60)': return 3
                    case '老年(>60)': return 4
                }
            })
        },
        'origin': data => {
            return data.sort(a => COUNTRY.indexOf(a.name) !== -1 ? 1 : -1)
        },
        'tran': data => {
            return _.orderBy(data, d => TRAN_ORDER[d.name])
        },
        'period': data => {
            return _.orderBy(data, d => {
                switch(d.name) {
                    case '疫情初期(~1/23)': return 0
                    case '发展期(1/23~2/6)': return 1
                    case '国内二次传播期(2/6~2/20)': return 2
                    case '国外输入期(2/20~)': return 3
                }
            })
        }
    }

    const COUNTRY = ["巴西", "法国", "柬埔寨", "澳门", "荷兰",
        "菲律宾", "俄罗斯", "新加坡", "西班牙", "瑞士", "泰国",
        "英国", "美国"]

    const getAgeCategory = age => {
        if (age >= 0 && age <= 15) {
            return '婴幼儿/青少年(0~15)'
        }
        if (age > 15 && age <= 30) {
            return '青年(16~30)'
        }
        if (age > 30 && age <= 45) {
            return '中青年(30~45)'
        }
        if (age > 45 && age <= 60) {
            return '中年(45~60)'
        }
        if (age > 60) {
            return '老年(>60)'
        }
    }

    const ChinaPeriod = ['2020/1/23', '2020/2/6', '2020/2/20']
        .map(d => new Date(d).getTime())

    const getPeriod = date => {
        const newDate = new Date(date).getTime()
        if (newDate <= ChinaPeriod[0]) {
            return '疫情初期(~1/23)'
        }
        if (newDate > ChinaPeriod[0] && newDate < ChinaPeriod[1]) {
            return '发展期(1/23~2/6)'
        }
        if (newDate > ChinaPeriod[1] && newDate < ChinaPeriod[2]) {
            return '国内二次传播期(2/6~2/20)'
        }
        if (newDate >= ChinaPeriod[2]) {
            return '国外输入期(2/20~)'
        }
        
    }

    // const scale = scaleLinear()
    //     .domain([1, 200])
    //     .range(['#87cc7c', '#966d4b','#935740', '#69277e', '#9d4da7'])

    export default {
        name: 'SanKey',
        methods: {
            getNodes(data) {
                return DIM.reduce((arr, key) => {
                    const styles = ITEM_STYLE[key] && ITEM_STYLE[key]() || {}
                    let tempArr =  _.chain(data)
                        .map(d => {
                            return {
                                name: d[key],
                                itemStyle: styles[d[key]],
                            }
                        })
                        .uniqBy('name')
                        .value()
                        tempArr = SORT_FUN[key] ? SORT_FUN[key](tempArr) : tempArr
                    return arr.concat(tempArr)
                }, [])
            },
            getLinks(data) {
                const links = [];
                DIM.forEach((d, i, arr) => {
                    if (i === arr.length - 1) return
                    data.forEach(d1 => {
                        const source = d1[d]
                        const target = d1[arr[i + 1]]
                        const value = data.filter(d2 => d2[d] === source
                            && d2[arr[i + 1]] === target
                            ).length
                        links.push({
                            source,
                            target,
                            value,
                            lineStyle: {
                                // color: scale(value),
                            },
                        })
                    })
                })

                return _.uniqWith(links, _.isEqual)
            },
            initData() {
                const data = _.chain(TrackJSON)
                    // .slice(0, 400)
                    .filter(d => d.track.length)
                    .map(d => {
                        const {track, nl} = d
                        let tran = track.length ? track[track.length - 1].tran : ''
                        tran = tran.indexOf('航班') !== -1 ? '航空' : tran
                        tran = /(私家)|(自驾)|(专车)|(商务车)/.test(tran) ? '私家/专车' : tran
                        tran = /(的士)|(出租车)/.test(tran) ? '出租车' : tran
                        const age_range = getAgeCategory(+nl)
                        return _.pick({
                            ...d,
                            tran: tran || '不明',
                            age_range,
                            period: getPeriod(d.track[d.track.length - 1].time)
                        },
                        DIM
                        )
                    })
                    .value()
                //console.log('data'+data[0])
                const nodes = this.getNodes(data)
                const links = this.getLinks(data)
                console.log('nodes'+nodes[0])
                console.log('data'+data[0])
                return {nodes, links}
            },
            initChart() {
                //const { nodes, links } = this.initData()
                
               /* const option = {
                    color: ['#87cc7c', '#966d4b', '#935740', '#69277e', '#9d4da7'],
                    tooltip: {
                        trigger: "item",
                        triggerOn: "mousemove"
                    },
                    series: {
                        type: "sankey",
                        left: 10,
                        right: 50,
                        nodeGap: 1,
                        layoutIterations: 0,
                        data: nodes, // 节点
                        links: links, // 节点之间的连线
                        draggable: false,
                        focusNodeAdjacency: "allEdges", // 鼠标划上时高亮的节点和连线，allEdges表示鼠标划到节点上点亮节点上的连线及连线对应的节点
                        label: {
                            fontSize: 10,
                            color: "rgba(255,255,255,.8)"
                        },
                        lineStyle: {
                            color: 'source',
                            curveness: 0.5
                        },
                    }
                };*/
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
                            

                    series: [
                        {
                            type: 'themeRiver',
                            emphasis: {
                                itemStyle: {
                                    shadowBlur: 20,
                                    shadowColor: 'rgba(0, 0, 0, 0.8)'
                                }
                            },
                            color:['#ff0000','#dec674','#6495ED','#8A2BE2'],
                            data: dataList
                                }
                            ]
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