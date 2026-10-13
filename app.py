"""Hello World Motion Lab. Run with: streamlit run app.py"""
import html
import json

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hello World Motion Lab", page_icon="👋", layout="wide")
st.title("👋 Hello World Motion Lab")
st.write("Type your name, change its style, and bring it to life!")

with st.sidebar:
    st.header("Controls")
    name = st.text_input("Enter your name", "Hello World", max_chars=100)
    font = st.selectbox("Font type", ["Arial", "Courier New", "Georgia", "Times New Roman", "Verdana", "Trebuchet MS"])
    size = st.slider("Font size (px)", 20, 120, 48)
    background = st.selectbox("Background", ["Light", "Dark", "Lavender", "Ocean", "Sunset"])
    mode = st.selectbox("Name display mode", ["Centered", "Ticker Tape", "Repeated"])
    effect = st.selectbox("Dynamic action", ["None", "Rain", "Snow", "Hail", "Wind", "Confetti", "Tornado"])
    speed = st.slider("Animation speed", 0.25, 3.0, 1.0, 0.25)
    paused = st.checkbox("Pause animation")

# Escape user input before putting it into HTML. No external assets are needed.
safe_name = html.escape(name.strip() or "Hello World")
themes = {
    "Light": ("#f6f8fc", "#172033"),
    "Dark": ("#101827", "#ffffff"),
    "Lavender": ("linear-gradient(135deg,#ede2ff,#c8b6ee)", "#34204f"),
    "Ocean": ("linear-gradient(135deg,#073b66,#007d92)", "#ffffff"),
    "Sunset": ("linear-gradient(135deg,#ffcf9b,#f49aaa,#a399df)", "#302039"),
}
bg, fg = themes[background]
names = "".join(f"<div>{safe_name}</div>" for _ in range(5)) if mode == "Repeated" else safe_name
config = json.dumps({"effect": effect, "speed": speed, "paused": paused, "dark": background in ["Dark", "Ocean"]})

# Animation runs in the browser, so Python only reruns when a control changes.
page = r'''<!doctype html>
<html><head><meta charset="utf-8"><style>
* {box-sizing:border-box} body {margin:0}
#stage {position:relative;height:580px;overflow:hidden;border-radius:20px;
background:BACKGROUND;color:FOREGROUND;font-family:FONT,sans-serif;}
canvas {position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
#names {position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
font-size:SIZEpx;font-weight:bold;text-align:center;padding:24px;z-index:2;
text-shadow:0 2px 14px rgba(128,128,128,.3);overflow-wrap:anywhere;}
#names.repeated {flex-direction:column;justify-content:space-evenly;font-size:min(SIZEpx,8vw)}
#names.ticker {padding:0;display:block;overflow:hidden}
.ticker .label {position:absolute;top:50%;width:max-content;white-space:nowrap;
animation:marquee DURATIONs linear infinite;transform:translateY(-50%)}
@keyframes marquee {from {left:100%;transform:translate(0,-50%)}
to {left:0;transform:translate(-100%,-50%)}}
.paused .label {animation-play-state:paused}
@media (prefers-reduced-motion:reduce) {.ticker .label {animation:none;left:50%;transform:translate(-50%,-50%)}}
</style></head><body>
<div id="stage"><canvas id="weather" aria-hidden="true"></canvas>
<div id="names" class="MODE"><div class="label">NAMES</div></div></div>
<script>
const cfg=CONFIG;
const canvas=document.getElementById('weather'), ctx=canvas.getContext('2d');
const stage=document.getElementById('stage');
let w=0,h=580,last=0,elapsed=0;
const rand=(a,b)=>a+Math.random()*(b-a);
const colors=['#ff4f81','#ffcf40','#38cbbb','#7795ff','#ce6cff'];
const particles=Array.from({length:120},()=>({x:Math.random(),y:Math.random(),
size:rand(2,6),v:rand(.6,1.5),angle:rand(0,Math.PI*2),color:colors[Math.floor(rand(0,5))]}));
function resize(){w=stage.clientWidth;h=stage.clientHeight;const dpr=Math.min(devicePixelRatio||1,2);
canvas.width=w*dpr;canvas.height=h*dpr;ctx.setTransform(dpr,0,0,dpr,0,0);}
new ResizeObserver(resize).observe(stage);resize();
function draw(dt){
 ctx.clearRect(0,0,w,h);
 if(cfg.effect==='None')return;
 for(let i=0;i<particles.length;i++){
  const p=particles[i];let x,y;
  if(cfg.effect==='Tornado'){
   const level=i/particles.length;
   const radius=20+level*Math.min(w*.32,180);
   const angle=p.angle+elapsed*(2.5+p.v);
   x=w*.5+Math.cos(angle)*radius+Math.sin(elapsed)*30;
   y=h*.88-level*h*.76+Math.sin(angle)*12;
   ctx.fillStyle=cfg.dark?'rgba(220,231,246,.65)':'rgba(72,83,105,.55)';
   ctx.beginPath();ctx.ellipse(x,y,p.size*2,p.size,angle,0,Math.PI*2);ctx.fill();continue;
  }
  const falling=cfg.effect!=='Wind';
  if(falling){p.y+=dt*p.v*(cfg.effect==='Rain'?.65:cfg.effect==='Hail'?.5:.15);
   p.x+=dt*(cfg.effect==='Rain'?-.08:Math.sin(elapsed+p.angle)*.025);}
  else{p.x+=dt*p.v*.45;p.y+=Math.sin(elapsed*2+p.angle)*dt*.03;}
  p.x=(p.x+1)%1;p.y=(p.y+1)%1;x=p.x*w;y=p.y*h;
  ctx.save();ctx.translate(x,y);
  if(cfg.effect==='Rain'){ctx.strokeStyle=cfg.dark?'#8dccff':'#337bb5';ctx.lineWidth=1.8;
   ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(-4,18);ctx.stroke();}
  else if(cfg.effect==='Wind'){ctx.strokeStyle=cfg.dark?'#c3e4ee':'#527a92';ctx.lineWidth=2;
   ctx.beginPath();ctx.moveTo(-35,0);ctx.quadraticCurveTo(10,-12,35,0);ctx.stroke();}
  else if(cfg.effect==='Confetti'){ctx.rotate(p.angle+elapsed*p.v*3);ctx.fillStyle=p.color;ctx.fillRect(-3,-5,6,10);}
  else {ctx.fillStyle=cfg.effect==='Snow'?(cfg.dark?'#ffffff':'#7295b8'):'#a5d9ee';
   ctx.beginPath();ctx.arc(0,0,p.size*(cfg.effect==='Snow'?.65:1),0,Math.PI*2);ctx.fill();
   if(cfg.effect==='Hail'){ctx.strokeStyle='#6597b1';ctx.stroke();}}
  ctx.restore();
 }
}
const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
function frame(now){const dt=last?Math.min((now-last)/1000,.05)*cfg.speed:0;last=now;
 if(!cfg.paused&&!reduced){elapsed+=dt;draw(dt);}
 requestAnimationFrame(frame);}
draw(0);requestAnimationFrame(frame);
</script></body></html>'''

replacements = {
    "BACKGROUND": bg, "FOREGROUND": fg, "FONT": font, "SIZE": str(size),
    "DURATION": str(14 / speed),
    "MODE": ("ticker" if mode == "Ticker Tape" else "repeated" if mode == "Repeated" else "centered") + (" paused" if paused else ""),
    "NAMES": names, "CONFIG": config,
}
# Replace template tokens in one pass, so user text never becomes a token.
import re
page = re.sub(r"BACKGROUND|FOREGROUND|FONT|SIZE|DURATION|MODE|NAMES|CONFIG", lambda m: replacements[m.group()], page)
components.html(page, height=590, scrolling=False)
st.caption("Input → Python controls → browser display. Change a control to see the app respond.")
