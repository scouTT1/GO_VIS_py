<template>
    <div class="search-list">
        <div class="search-lists">
            <header class="lists-header">
                <span>个人等级分排名</span>
                <el-checkbox-group v-model="checkboxGroup" size="mini">
                    <el-checkbox-button
                        v-model="male"
                        v-for="sex in sex_male"
                        :label="sex"
                        :key="sex"
                        @change="handleChangeMale">
                            {{sex}}
                    </el-checkbox-button>
                    <el-checkbox-button
                        v-model="female"
                        v-for="sex in sex_female"
                        :label="sex"
                        :key="sex"
                        @change="handleChangeFemale">
                            {{sex}}
                    </el-checkbox-button>
                </el-checkbox-group>
            </header>
            <ul >
                <li
                    v-for="(item,index) in listArr"
                    :key="item.name"
                    :class="index===active? smart_index : normal_index"
                    @mouseover="mouseOver(item,index)"
                    @mouseleave="mouseLeave(item,index)"
                >
                    <div>{{item.name}}</div>
                    <div>{{item.country}}</div>
                    <div>{{item.count}}</div>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import eventBus from '../eventBus'
import _ from 'lodash'
import picture from '@/assets/border.png'
import TrackJSON from '@/data/track'
import PlayerData from '@/data/player'
//import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
//import 'swiper/css/swiper.css'

export default {

    name: 'search-list',
    components: {
    },
    data() {
        return {
            tableData:[],
            active: 0,
            checkboxGroup: ['男','女'],
            sex_male: ['男'],
            sex_female: ['女'],
            male: true,
            female: true,
            swiperOption: {
                direction : 'vertical',
                autoplay: {
                    delay: 1000,
                    disableOnInteraction: false,
                },
                loop: true,
                slidesPerView: 3,
                mousewheel: true,
                height: 400,
            },
            styles: {
                backgroundImage: `url(${picture})`,
                backgroundRepeat: 'no-repeat',
            },
            listArr: [],
            currentDate: '',
            transArr: [],
            transObj: {},
            idAdd: false,
        }
    },
    methods: {
        initData() {
            this.playerData=PlayerData
            this.initTrackData = TrackJSON
                .filter(d => d.track.length)
                .map(d => ({
                    ...d,
                    place: _.chain(d.track)
                        .slice(0, 1)
                        .reduce((arr, d1) => {
                            arr.push({
                                name: d1.from,
                                date: d.track[d.track.length - 1].time,
                                time: new Date(d.track[d.track.length - 1].time).getTime(),
                            })
                            return arr
                        }, [])
                        .uniqBy('name')
                        .value()
            }))

            this.originListArr = _.chain(this.initTrackData)
                .map(d => d.track.map(d1 => [d1.from, d1.to]))
                .flattenDeep()
                .uniq()
                .compact()
                .map(d => ({
                    name: d,
                    count: 0,
                }))
                .filter(d => d.name !== '深圳')
                .value()

            this.allCountObj = _.chain(this.initTrackData)
                .map('place')
                .flatten()
                .map('name')
                .countBy()
                .value()

            this.placeArr = _.chain(this.initTrackData)
                .map('place')
                .flatten()
                .value()

            this.startSearch()
        },
        startSearch(date = '') {
            this.listArr = _.chain(this.originListArr)
                .map(d => ({
                    ...d,
                    count: this.getCount(d.name, date)
                }))
                .filter(d => d.count)
                .orderBy('count', 'desc')
                .value()

            var temp_list;
            if(this.male && !this.female){
                temp_list=['♂'];
            }else if(!this.male && this.female){
                temp_list=['♀'];
            }else{
                temp_list=['♂','♀'];
            }
            this.listArr=_.chain(this.playerData).map(d => ({
                ...d,
                name: d.name_zh,
                country: d.country,
                count: d.score_new
            })).filter(d => d.count).filter(d => temp_list.indexOf(d.sex)!=-1)
            .orderBy('count','desc')
            .value();
            
        },
        getCount(name, date) {
            if (!date) return this.allCountObj[name] || 0
            const timeStamp = new Date(date).getTime()
            return this.placeArr
                .filter(d => {
                    let tempFlag = false
                    if (this.isAdd) {
                        tempFlag = d.time <= timeStamp
                    } else {
                        tempFlag = d.date === date
                    }
                    return tempFlag && d.name === name}
                )
                .length
        },
        watchTime() {
            eventBus.$on('trackMapTime', ({date, isAdd}) => {
                this.isAdd = isAdd
                this.currentDate = date
                this.startSearch(date)
            })
        },
        handleChangeMale() {
            this.male=!this.male;
            this.initData();
        },
        handleChangeFemale() {
            this.female=!this.female;
            this.initData();
        },
        mouseOver(item,index){
            this.active=index;
            eventBus.$emit('selectPlayerInfo',{
                playerInfo: item
            });
        },
        mouseLeave(item,index){
            this.active=index;
        }
    },
    mounted() {
        this.initData()
    },
}
</script>

<style lang="less">
    .search-list {
        margin-left: 20px;
        width: calc(100% - 20px);
        display: flex;
        flex-direction: column;
        .search-lists {
            margin-top: 20px;
            margin-bottom: 20px;
            height: calc(100% - 20px);
            overflow: auto;
            .lists-header {
                display: flex;
                justify-content: space-between;
                font-size: 14px;
            }
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
    .smart_index{
        background-color: #fff;
    }
    .normal_index{
        background-color: yellow;
    }
</style>