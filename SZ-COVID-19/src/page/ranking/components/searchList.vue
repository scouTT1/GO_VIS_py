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
                    :class="{smart_index :active==index}"
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
import PlayerData from '@/data/player_all_list.json'

export default {

    name: 'search-list',
    components: {
    },
    data() {
        return {
            tableData:[],
            active: -1,
            checkboxGroup: ['男','女'],
            sex_male: ['男'],
            sex_female: ['女'],
            male: true,
            female: true,
            listArr: [],
            
        }
    },
    methods: {
        initData() {
            this.playerData=PlayerData
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
        handleChangeMale() {
            this.male=!this.male;
            this.initData();
        },
        handleChangeFemale() {
            this.female=!this.female;
            this.initData();
        },
        mouseOver(item,index){
            //this.active[index]='background-color: #ffffff';
            this.active=index;
            eventBus.$emit('selectPlayerInfo',{
                playerInfo: item
            });
        },
        mouseLeave(item,index){
            //this.active[index]='background-color: #09141D';
            this.active=-1;
            console.log(item,index);
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
</style>