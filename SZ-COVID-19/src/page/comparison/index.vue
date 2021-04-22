<template>
   <div id="comparison">
       <div class="comparison-left">
            <Section
                class="left-map"
                title="棋手对比热力图"
                height="100%"
            >
                <div class="part-sz">
                    <!--<heatmap />-->
                    <SzStatic />
                    <SzMap />
                </div>
            </Section>
       </div>
        <div class="comparison-right">
             <Section
                class="right-list"
                title="棋手A"
                height="100%"
            >
                <div class="part-list">
                    <List />
                </div>
            </Section>
            <Section
                title="棋手B"
                class="right-map"
                height="100%"
            >
                <div class="part-world">
                    <LineChart />
                </div>
            </Section>
       </div>
   </div>
</template>

<script>


import Section from '@/components/section'
import SzMap from './components/szMap2'
import SzStatic from './components/szStatic'
//import heatmap from './components/heatmap'
import List from './components/list'
import LineChart from './components/lineChart'

export default {
    name: 'Comparison',
    components: {
        Section,
        List,
        //heatmap,
        SzMap,
        SzStatic,
        LineChart,
    },
};
</script>

<style lang="less" scoped>
    #comparison{
        display: flex;
        height: 100%;
        .comparison-left {
            width: 66%;
            overflow: hidden;
            .left-map {
                height: 100%;
            }
            .part-sz{
                display: flex;
                flex-direction: column;
                height: 100%;
                .map{
                    flex: 1;
                    width: 100%;
                }
            }
        }
        .comparison-right {
            margin-left: 20px;
            display: flex;
            flex-direction: column;
            flex: 1;
            .part-list{
                height: 100%;
            }
            .right-list{
                height: calc(50% - 10px);
            }
            .right-map{
                height: calc(50% - 10px);
            }
            .part-world {
                height: 100%;
                display: flex;
                flex-direction: column;
                .world-map {
                    height: 50%;
                }
                .world-bar {
                    flex: 1;
                }
            }
        }
    }
</style>
