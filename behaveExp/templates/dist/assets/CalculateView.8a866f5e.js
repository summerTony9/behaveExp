import{_ as m,a as d,o as _,c as u,t as a,b as c,d as s,w as p,v as f,F as v,r as b,N as q}from"./index.6bc05358.js";const N={props:["userName","nround","qn"],data(){return{start_min:0,start_sec:0,timer0:0}},mounted(){d.get("http://127.0.0.1:8000/get_time",{params:{userName:this.userName}}).then(t=>{this.start_min=t.data.mint,this.start_sec=t.data.sec}),this.timer0=setInterval(()=>{this.start_sec===60?(this.start_sec=0,this.start_min=this.start_min+1):this.start_sec=this.start_sec+1},1e3)},watch:{start_min(t,e){t==12&&this.$router.push("about")}},beforeDestroy(){clearInterval(this.timer0)}},M={class:"shadow p-2 mb-2 bg-body rounded"};function y(t,e,r,l,n,o){return _(),u("div",M," \u7528\u6237"+a(r.userName)+", \u5DF2\u8BA1\u7B97"+a(r.qn)+"\u9898,\u5B9E\u9A8C\u5DF2\u8FDB\u884C"+a(n.start_min)+"\u5206"+a(n.start_sec)+"\u79D2 ",1)}const $=m(N,[["render",y]]),g={data(){return{qn:0,num_1:Math.floor(Math.random()*100),num_2:Math.floor(Math.random()*100),correct_n:0}},methods:{cal(){this.ans===this.num_1+this.num_2&&(this.correct_n=this.correct_n+1),this.num_1=Math.floor(Math.random()*100),this.num_2=Math.floor(Math.random()*100),this.qn=this.qn+1,this.ans=""}},components:{Game_time_cal:$}},x={class:"input-group mb-3"},w={class:"input-group-text"};function C(t,e,r,l,n,o){const h=b("Game_time_cal");return _(),u(v,null,[c(h,{userName:this.$route.query.id,nround:this.$route.query.nround,qn:n.qn},null,8,["userName","nround","qn"]),s("div",x,[s("span",w,a(n.num_1)+"+"+a(n.num_2)+"=",1),p(s("input",{type:"text",class:"form-control","onUpdate:modelValue":e[0]||(e[0]=i=>t.ans=i)},null,512),[[f,t.ans,void 0,{number:!0}]]),s("button",{class:"btn btn-outline-primary",type:"button",onClick:e[1]||(e[1]=(...i)=>o.cal&&o.cal(...i))},"\u63D0\u4EA4")])],64)}const V=m(g,[["render",C]]),k={class:"container"},B={class:"row"},D=s("div",{class:"col"},null,-1),G={class:"col-8"},F=s("div",{class:"col"},null,-1),E={__name:"CalculateView",setup(t){return(e,r)=>(_(),u("div",k,[c(q),s("div",B,[D,s("div",G,[c(V)]),F])]))}};export{E as default};
