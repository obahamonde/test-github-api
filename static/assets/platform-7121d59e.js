import{d as y,Q as m,m as w,b as C,k as h,r as S,o as l,c as i,f as e,u as t,a as p,A as g,F as f,e as T,h as $,w as I,s as G,z as B,H as D,D as N,R,t as V,p as F,l as z,_ as v}from"./index-addff8a8.js";const M=r=>(F("data-v-de5042fc"),r=r(),z(),r),O={key:0,class:"text-center text-2xl font-bold col center gap-4 bg-light px-16 py-8 rounded-lg sh"},P=M(()=>e("h1",{class:"text-lg text-accent font-sans drop-shadow-color-success drop-shadow-sm"}," Your Development Stack is Ready! ",-1)),j={class:"text-center text-2xl font-bold row center gap-4"},A=["href"],E={class:"col center p-4"},H=["href"],J=["href"],L={class:"grid3"},Q={class:"col center gap-8"},U={class:"template-name"},Y={class:"flex flex-col gap-4 action-button"},q=["disabled"],K=y({__name:"GithubTemplates",setup(r){const s=m({about:"Pick your template",templates:["logos:react","logos:vue","logos:ruby","logos:express","simple-icons:fastapi","logos:php","logos:python"],response:null}),{state:n}=w(),c=C(""),d=m({login:n.user.name,repo:"",token:n.githubToken,email:n.user.email,image:h(()=>c.value?c.value.split(":").pop():null)}),x=async u=>{const{data:o}=await D("/api/github/workspace",{method:"POST",body:JSON.stringify(u)}).json();s.response=t(o),n.notifications.push({message:"Template created",status:"success"})},b=h(()=>!!c.value);return(u,o)=>{const _=S("Icon"),k=N;return l(),i(f,null,[e("div",null,[t(s).response?(l(),i("div",O,[P,e("div",j,[e("a",{href:t(s).response.workspace.url,target:"_blank",class:"text-teal-700"},[p(_,{icon:"logos:visual-studio-code",class:"x4 scale"})],8,A),e("div",E,[e("a",{href:t(s).response.preview.url,target:"_blank",class:"text-teal-700"},[p(_,{icon:"logos:chrome",class:"x4 scale"})],8,H)]),e("a",{href:t(s).response.preview.repo,target:"_blank",class:"text-teal-700"},[p(_,{icon:"logos:github-icon",class:"x4 scale"})],8,J)])])):g("",!0)]),e("section",L,[(l(!0),i(f,null,T(t(s).templates,a=>(l(),i("div",Q,[p(_,{icon:a,class:R(["template-icon",t(c)===a?"animate-bounce":""]),onClick:se=>c.value=a},null,8,["icon","onClick","class"]),e("h1",U,V(a.split(":").pop()),1)]))),256))]),t(b)?(l(),$(k,{key:0,title:t(s).about,onClose:o[2]||(o[2]=a=>c.value="")},{body:I(()=>[e("div",Y,[e("span",null,[G(e("input",{class:"input","onUpdate:modelValue":o[0]||(o[0]=a=>t(d).repo=a),placeholder:"Repository name"},null,512),[[B,t(d).repo]])]),e("button",{class:"btn-get",onClick:o[1]||(o[1]=a=>x(t(d))),disabled:!t(d).repo}," Get started ",8,q)])]),_:1},8,["title"])):g("",!0)],64)}}});const W=v(K,[["__scopeId","data-v-de5042fc"]]),X={},Z={class:"container"},ee=e("h1",{class:"text-title my-8"},"Get started with a predefined template:",-1);function te(r,s){const n=W;return l(),i("main",Z,[ee,p(n)])}const ae=v(X,[["render",te]]);export{ae as default};
