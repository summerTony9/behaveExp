import{_ as d,G as l,o as n,c as a,b as c,d as s,F as u,r as m,N as p}from"./index.ebdbe3a6.js";import"./index.7e2f11a3.js";const b={methods:{click_yes(){this.$router.push("reward")},click_no(){this.$router.push("/")}},components:{Game_time:l}},h={class:"card shadow p-2 mb-2 bg-body rounded"},k={class:"card-body"},f=s("p",{class:"card-text"},"\u662F\u5426\u67E5\u770B\u672C\u8F6E\u60A8\u7684\u4E2A\u4EBA\u8D44\u4EA7\u7EC4\u5408\u6536\u76CA?",-1);function v(r,t,_,g,B,e){const i=m("Game_time");return n(),a(u,null,[c(i),s("div",h,[s("div",k,[f,s("button",{type:"button",class:"btn btn-primary float-start",onClick:t[0]||(t[0]=(...o)=>e.click_yes&&e.click_yes(...o))},"\u662F"),s("button",{type:"button",class:"btn btn-danger float-end",onClick:t[1]||(t[1]=(...o)=>e.click_no&&e.click_no(...o))},"\u5426")])])],64)}const y=d(b,[["render",v]]),$={class:"container"},x={class:"row"},w=s("div",{class:"col"},null,-1),G={class:"col-8"},N=s("div",{class:"col"},null,-1),F={__name:"Question2View",setup(r){return(t,_)=>(n(),a("div",$,[c(p),s("div",x,[w,s("div",G,[c(y)]),N])]))}};export{F as default};