import{d as p,m,C as f,b as g,o as r,c as h,f as s,u as e,t as c,h as b,w as l,a as k,A as C,F as v,D as w}from"./index-addff8a8.js";import{_ as x}from"./SingleUpload.vue_vue_type_script_setup_true_lang-b6d94e27.js";import{b as i}from"./route-block-83d24a4e.js";const y={class:"col center p-12 gap-4"},B=["src"],$={class:"font-sans"},F={class:"font-sans"},N=s("p",{class:"drop-shadow drop-shadow-color-blueGray font-sans text-center"}," Upload a File ",-1),S=["src"],V=p({__name:"monitoring",setup(D){const{state:a}=m(),{logout:_}=f(),t=g(!1);return(M,o)=>{const d=x,u=w;return r(),h(v,null,[s("div",y,[s("img",{src:e(a).user.picture,class:"rf sh cp scale",onClick:o[0]||(o[0]=n=>t.value=!e(t))},null,8,B),s("h1",$,c(e(a).user.name),1),s("h2",F,c(e(a).user.email),1),s("button",{class:"btn-del",onClick:o[1]||(o[1]=n=>e(_)())},"Logout")]),e(t)?(r(),b(u,{key:0,onClose:o[2]||(o[2]=n=>t.value=!1)},{header:l(()=>[N]),body:l(()=>[k(d,{accepts:"image/*"},{default:l(({data:n})=>[s("img",{src:n.url,class:"rf sh x6"},null,8,S)]),_:1})]),_:1})):C("",!0)],64)}}});typeof i=="function"&&i(V);export{V as default};