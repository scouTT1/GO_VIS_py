import _ from 'lodash'
import basicInfo from '@/data/player_basic_info.json'
import match_list from '@/data/link_table.json'
import id2zh from '@/data/id2zh.json'
// import zh2id from '@/data/zh2id.json'
// import player from '@/data/player'
// import fs from 'fs'
export function initData() {
    let percent = [];
    var upperbound = 0.0;
    for(upperbound = 0.01; upperbound<=1.0;upperbound+=0.01){
        percent.push(upperbound);
    }
    basicInfo.forEach(d=>{
        d.level = d.level===undefined? '未知' : d.level;
        d.country = d.country===undefined? '未知' : d.country;
        d.score_new = d.score_new===undefined? 0 : d.score_new;
        d.winProb = (d.num_total && d.num_wins) ? (d.num_wins*1.0/d.num_total) : 0.0;
        if(d.country === '日本'){
            d.family_name = d.name_zh.substring(0, 2);
        }
        else if(d.country === '中国' || d.country === '中国台湾' || d.country === '韩国' ){
            d.family_name = d.name_zh.substring(0, 1);
        }
        else{
            d.family_name = '其他';
        }
        for(upperbound in percent){
            if(parseFloat(upperbound)>d.winProb){
                d.winRange = parseFloat(upperbound)-0.01;
                break;
            }
        }
        
    })
    return basicInfo.filter(d => d.num_total>150);
}

export function aggre(sortkey) {
    const total = basicInfo.length;
    return _.chain(basicInfo)
        .reduce((obj, d) => {
            const key = d[sortkey] === '' ? '未知' : d[sortkey];
            const value = obj[key] ? obj[key].value + 1 : 1;
            obj[key] = {
                name: key,
                value,
                percent: `${(value * 100 / total).toFixed(2)}%`
            }
            return obj;
        }, {})
        .values()
        .orderBy('value', 'desc')
        .value()
}

export function calculateNodeAndLink(data) {
    const links = [];
    const nodes = data;
    const nodeIds = data.map(d => d.player_id);
    _.forIn(nodes, d => {
        // const relation = match_list[d.player_id]
        // const targetid = d.player_id;
        // if (relation.length) {
        //     const relationArr = relation.map(d => zh2id[d.opponent_name]);
        //     d.match_opponents = relationArr 
        //     relationArr.forEach(sourceid => {
        //         if(nodeIds.includes(sourceid) && nodeIds.includes(targetid)) {
        //             links.push({
        //                 source: sourceid,
        //                 target: targetid,
        //             })
        //         }
        //     })
        // }
        const targetid = d.player_id;
        const relation = match_list[targetid]
        if (Object.keys(relation).length) {
            Object.keys(relation).forEach(sourceid => {
                if(nodeIds.includes(parseInt(sourceid)) && nodeIds.includes(targetid)) {
                    const sid = parseInt(sourceid);
                    links.push({
                        source: {player_id: sid, name_zh: id2zh[sid]},
                        target: {player_id: targetid, name_zh: id2zh[targetid]},
                    })
                }
            })
        }
    })
    // calculate node radius
    nodes.forEach(d => { 
        // const winProb = d.num_total ? d.num_wins*1.0/d.num_total : 0;
        const r = 5;
        // d.winProb = winProb;
        d.r = r + (d.score_new-1500) * 0.001;
    })

    return [nodes, links];
} 

