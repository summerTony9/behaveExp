import{_ as l,G as d,o as n,c as a,b as c,d as t,F as u,r as m,N as p}from"./index.ebdbe3a6.js";import"./index.7e2f11a3.js";const b={methods:{click_yes(){this.$router.push("about")},click_no(){this.$router.push("question2")}},components:{Game_time:d}},h={class:"card shadow p-2 mb-2 bg-body rounded"},k={class:"card-body"},f=t("p",{class:"card-text"},"\u662F\u5426\u67E5\u770B\u672C\u8F6E\u5E02\u573A\u4EF7\u683C\u8D70\u52BF",-1);function v(_,s,r,w,B,o){const i=m("Game_time");return n(),a(u,null,[c(i),t("div",h,[t("div",k,[f,t("button",{type:"button",class:"btn btn-primary float-start",onClick:s[0]||(s[0]=(...e)=>o.click_yes&&o.click_yes(...e))},"\u662F"),t("button",{type:"button",class:"btn btn-danger float-end",onClick:s[1]||(s[1]=(...e)=>o.click_no&&o.click_no(...e))},"\u5426")])])],64)}const y=l(b,[["render",v]]),$={class:"container"},x={class:"row"},G=t("div",{class:"col"},null,-1),N={class:"col-8"},g=t("div",{class:"col"},null,-1),F={__name:"QuestionView",setup(_){return(s,r)=>(n(),a("div",$,[c(p),t("div",x,[G,t("div",N,[c(y)]),g])]))}};export{F as default};