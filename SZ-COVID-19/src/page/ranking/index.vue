<template>
    <div class="analysis">
        <div class="up-container">
            <Section
                title="围棋棋手排名"
                class="map-left"
                height="100%"
            >
                <div class="map-container">
                    <search-list />
                </div>
            </Section>
            <Section
                title="个人等级分曲线"
                class="map-right"
                height="100%"
            >
                <div class="map-container">
                    <lineChart />
                </div>
            </Section>
        </div>
        <div class="down-container">
            <Section
                title="百强棋手数量"
                height="100%"
                class="down-map"
            >
                <SanKey />
            </Section>
        </div>
    </div>
</template>

<script>
    import Section from '@/components/section'
    import SanKey from './components/sankey'
    import LineChart from './components/lineChart'
    import SearchList from './components/searchList'

    export default {
        name: 'Ranking',
        components:  {
            Section,
            SanKey,
            LineChart,
            'search-list': SearchList
        }
    }
</script>

<style lang="less" scoped>
    .analysis {
        display: flex;
        flex-direction: column;
        height: 100%;
        .up-container{
            flex-direction: row;
            display: flex;
            width: 100%;
            .map-left {
                height: 500px;
                flex-direction: row;
                margin: 0 10px 0 0;
                .map-container {
                    height: 100%;
                    width: 100%;
                    display: flex;
                }
            }
            .map-right {
                height: 500px;
                flex-direction: row;
                margin: 0 0 0 10px;
                .map-container {
                    height: 100%;
                    width: 100%;
                    display: flex;
                }
            }
        }
        .down-container{
            flex-direction: row;
            display: flex;
            width: 100%;
            .down-map{
                margin-top: 20px;
            }
        }
    }
</style>