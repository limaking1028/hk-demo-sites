import sys, urllib.parse, json, html
from PIL import Image, ImageDraw, ImageFont
BASE = (sys.argv[1] if len(sys.argv)>1 else "https://YOUR-USERNAME.github.io/hk-demo").rstrip("/")
PHONE="85212345678"
FONT="/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
def wa(msg): return f"https://wa.me/{PHONE}?text="+urllib.parse.quote(msg, safe="")
def money(items): return "".join(f"<li><span>{n}</span><b>HK${p}</b></li>" for n,p in items)
SITES = {
"cha-chaan-teng": dict(
 name="港味茶餐廳", c1="#b03a2e", c2="#e67e22", type="Restaurant", price="HK$14-HK$68",
 desc="地道港式早餐、下午茶及招牌餐，旺角茶餐廳",
 tag="地道港式 · 熱辣出爐", wamsg="你好，我想訂位（人數：＿＿，時間：＿＿）",
 cta="WhatsApp 訂位", nav=[("menu","餐單"),("about","關於我們"),("reviews","食客評價"),("faq","常見問題"),("visit","地址／訂位")],
 logo='<svg viewBox="0 0 64 64" width="72" height="72" role="img" aria-label="港味茶餐廳標誌：茶杯"><circle cx="32" cy="32" r="30" fill="#fff"/><path d="M16 26h28v8a14 14 0 0 1-28 0z" fill="#b03a2e"/><path d="M44 28h4a5 5 0 0 1 0 10h-5" fill="none" stroke="#b03a2e" stroke-width="3"/><path d="M24 20c0-4 4-4 4-8M33 20c0-4 4-4 4-8" stroke="#e67e22" stroke-width="3" fill="none" stroke-linecap="round"/></svg>',
 sections=[
 ("signature","招牌推介","<ul class='cards'><li><h3>絲襪奶茶</h3><p>茶底濃滑，每日新鮮泡製。<br><b>HK$16</b></p></li><li><h3>菠蘿油</h3><p>熱辣出爐，牛油冰凍對比。<br><b>HK$14</b></p></li><li><h3>焗豬扒飯</h3><p>厚切豬扒配蕃茄汁。<br><b>HK$58</b></p></li></ul>"),
 ("menu","分時段餐單","<h3>早餐 07:00–11:30</h3><ul class='price'>"+money([("餐蛋治套餐（連飲品）",38),("火腿通粉（連飲品）",36),("多士配奶茶",28)])+"</ul><h3>午市套餐 11:30–15:00</h3><ul class='price'>"+money([("沙嗲牛肉麵（連飲品）",48),("招牌焗豬扒飯（連飲品）",58),("星洲炒米（連飲品）",54)])+"</ul><h3>下午茶 15:00–18:00</h3><ul class='price'>"+money([("港式奶茶",16),("菠蘿油",14),("西多士",32),("下午茶套餐",42)])+"</ul><h3>晚市 18:00–21:00</h3><ul class='price'>"+money([("惠靈頓牛柳飯",68),("乾炒牛河",62)])+"</ul>"),
 ("about","關於我們","<p>港味茶餐廳（虛構）以街坊價錢提供地道港式味道，用料新鮮、落單快、坐得舒服，歡迎一家大細或朋友小聚。</p>"),
 ("reviews","食客評價（示範）","<p class='note'>以下評價為虛構示範內容。</p><blockquote>「奶茶夠滑，菠蘿油一流！」— 陳小姐（示範）</blockquote><blockquote>「午市出餐快，啱上班族。」— 李先生（示範）</blockquote><blockquote>「豬扒飯份量足，價錢合理。」— 黃太（示範）</blockquote>"),
 ("faq","常見問題","<details><summary>可以訂位嗎？</summary><p>可以，經 WhatsApp 提供人數及時間即可。</p></details><details><summary>有無外賣自取？</summary><p>設外賣自取，請先 WhatsApp 落單。</p></details><details><summary>可唔可以收信用卡？</summary><p>示範網站，實際付款方式以真實店舖為準。</p></details>"),
 ("notice","訂位須知","<ul class='plain'><li>訂位會保留 15 分鐘，逾時恕不另行通知。</li><li>6 人或以上請提早一日預約。</li><li>繁忙時段（12:00–14:00）可能需限時用餐。</li></ul>"),
 ],
 hours="每日 07:00–21:00", ),
"beauty-salon": dict(
 name="美麗軒美容院", c1="#7d3c98", c2="#d81b7a", type="BeautySalon", price="HK$88-HK$680",
 desc="面部護理、美甲及身體按摩，旺角美容院",
 tag="放鬆身心 · 專業護理", wamsg="你好，我想預約療程（療程：＿＿，日期時間：＿＿）",
 cta="WhatsApp 預約療程", nav=[("treatments","療程"),("about","關於我們"),("reviews","客人評價"),("faq","常見問題"),("visit","地址／預約")],
 logo='<svg viewBox="0 0 64 64" width="72" height="72" role="img" aria-label="美麗軒美容院標誌：蓮花"><circle cx="32" cy="32" r="30" fill="#fff"/><path d="M32 12c8 8 8 24 0 36-8-12-8-28 0-36z" fill="#d81b7a"/><path d="M14 24c12 0 20 10 18 24-12-2-20-12-18-24zM50 24c-12 0-20 10-18 24 12-2 20-12 18-24z" fill="#7d3c98"/></svg>',
 sections=[
 ("signature","招牌療程","<ul class='cards'><li><h3>深層清潔面部護理</h3><p>60 分鐘 · 淨化毛孔<br><b>HK$388</b></p></li><li><h3>全身香薰按摩</h3><p>90 分鐘 · 舒緩疲勞<br><b>HK$480</b></p></li><li><h3>新客體驗優惠</h3><p>45 分鐘 · 首次限定<br><b>HK$168</b></p></li></ul>"),
 ("treatments","療程分類及時長","<h3>面部護理</h3><ul class='price'>"+money([("深層清潔面部護理（60 分鐘）",388),("補濕亮肌護理（75 分鐘）",458)])+"</ul><h3>美甲</h3><ul class='price'>"+money([("基本修甲連甲油（45 分鐘）",198),("凝膠甲（75 分鐘）",298)])+"</ul><h3>身體按摩</h3><ul class='price'>"+money([("全身香薰按摩（90 分鐘）",480),("肩頸舒緩按摩（30 分鐘）",220)])+"</ul><h3>眉毛及其他</h3><ul class='price'>"+money([("眉毛修飾（20 分鐘）",88),("新客體驗（45 分鐘）",168)])+"</ul>"),
 ("about","關於我們","<p>美麗軒（虛構）專注舒適私隱的護理環境，由資深美容師一對一服務，按你的膚質及需要建議合適療程。</p>"),
 ("reviews","客人評價（示範）","<p class='note'>以下評價為虛構示範內容。</p><blockquote>「面部護理好舒服，皮膚明顯透亮。」— Amy（示範）</blockquote><blockquote>「環境乾淨，美容師好細心。」— Karen（示範）</blockquote><blockquote>「按摩手勢好，做完好輕鬆。」— Joey（示範）</blockquote>"),
 ("faq","常見問題","<details><summary>第一次要點準備？</summary><p>建議卸妝後到店，並預早 10 分鐘抵達。</p></details><details><summary>可唔可以改期？</summary><p>請提早 24 小時 WhatsApp 通知。</p></details><details><summary>敏感肌可以做嗎？</summary><p>預約時告知，美容師會建議合適療程。</p></details>"),
 ("notice","預約須知","<ul class='plain'><li>請提早 10 分鐘到達，遲到會縮短療程時間。</li><li>改期或取消請提早 24 小時通知。</li><li>孕婦或有皮膚疾患請預約時說明。</li></ul>"),
 ],
 hours="星期一至六 10:00–21:00；日及公眾假期 11:00–19:00"),
}
MAP_Q=urllib.parse.quote("旺角")
for d,s in SITES.items():
    url=f"{BASE}/{d}/"; img=f"{url}og-image.png"; w=wa(s["wamsg"])
    # og image
    im=Image.new("RGB",(1200,630),s["c1"]); dr=ImageDraw.Draw(im)
    c1=tuple(int(s["c1"][i:i+2],16) for i in (1,3,5)); c2=tuple(int(s["c2"][i:i+2],16) for i in (1,3,5))
    for x in range(1200):
        t=x/1199; dr.line([(x,0),(x,630)],fill=tuple(int(c1[k]+(c2[k]-c1[k])*t) for k in range(3)))
    dr.text((600,260),s["name"],font=ImageFont.truetype(FONT,110,index=2),fill="white",anchor="mm")
    dr.text((600,400),s["tag"],font=ImageFont.truetype(FONT,48,index=2),fill="white",anchor="mm")
    dr.text((600,570),"示範網站 Demo",font=ImageFont.truetype(FONT,30,index=2),fill="white",anchor="mm")
    im.save(f"{d}/og-image.png")
    ld={"@context":"https://schema.org","@type":s["type"],"name":s["name"],"description":s["desc"],"url":url,"image":img,"telephone":"+"+PHONE,"priceRange":s["price"],"address":{"@type":"PostalAddress","streetAddress":"示範街 1 號","addressLocality":"旺角","addressRegion":"九龍","addressCountry":"HK"},"openingHours":"Mo-Su 07:00-21:00" if d=="cha-chaan-teng" else ["Mo-Sa 10:00-21:00","Su 11:00-19:00"]}
    nav="".join(f'<a href="#{i}">{t}</a>' for i,t in s["nav"])
    secs="".join(f'<section id="{i}"><h2>{t}</h2>{b}</section>' for i,t,b in s["sections"])
    title=f'{s["name"]}｜{s["desc"]}'
    page=f'''<!DOCTYPE html>
<html lang="zh-HK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{s["name"]}（示範網站）：{s["desc"]}。一鍵 WhatsApp 預約。">
<meta name="theme-color" content="{s["c1"]}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{s["name"]}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{s["desc"]}。示範網站，一鍵 WhatsApp 預約。">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{s["name"]}宣傳圖">
<meta property="og:locale" content="zh_HK">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:image" content="{img}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Ccircle cx='16' cy='16' r='16' fill='{urllib.parse.quote(s["c1"])}'/%3E%3C/svg%3E">
<script type="application/ld+json">{json.dumps(ld,ensure_ascii=False)}</script>
<style>
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;font-family:system-ui,"PingFang HK","Noto Sans TC",sans-serif;color:#222;line-height:1.7;padding-bottom:84px}}
header.hero{{background:linear-gradient(135deg,{s["c1"]},{s["c2"]});color:#fff;text-align:center;padding:40px 20px}}
header.hero h1{{margin:.3em 0 0}}header.hero p{{margin:.3em 0 0}}
nav{{position:sticky;top:0;background:#fff;box-shadow:0 1px 6px #0002;display:flex;overflow-x:auto;white-space:nowrap;z-index:5}}
nav a{{padding:12px 14px;color:{s["c1"]};text-decoration:none;font-weight:600}}
main{{max-width:760px;margin:auto;padding:0 20px}}section{{padding:20px 0;scroll-margin-top:50px}}
h2{{border-left:5px solid {s["c1"]};padding-left:10px}}h3{{color:{s["c1"]};margin:1em 0 .2em}}
ul.price{{list-style:none;padding:0;margin:0}}ul.price li{{display:flex;justify-content:space-between;gap:12px;padding:8px 0;border-bottom:1px dashed #ccc}}
ul.cards{{list-style:none;padding:0;display:grid;gap:12px}}ul.cards li{{background:#faf5f7;border-radius:12px;padding:6px 16px}}
blockquote{{margin:10px 0;padding:10px 16px;background:#f5f5f5;border-left:4px solid {s["c2"]}}}.note{{color:#666;font-size:.9em}}
details{{border-bottom:1px solid #ddd;padding:8px 0}}summary{{cursor:pointer;font-weight:600}}
iframe{{width:100%;height:280px;border:0;border-radius:12px}}
.wa{{display:block;background:#128c7e;color:#fff;text-align:center;padding:16px;border-radius:12px;font-size:1.1em;text-decoration:none;font-weight:bold}}
.fix{{position:fixed;bottom:12px;left:12px;right:12px;max-width:760px;margin:auto;box-shadow:0 4px 12px #0005;z-index:9}}
footer{{text-align:center;font-size:.85em;color:#555;padding:20px}}
@media(min-width:700px){{ul.cards{{grid-template-columns:repeat(3,1fr)}}header.hero{{padding:70px}}nav{{justify-content:center}}}}
</style>
</head>
<body>
<header class="hero">{s["logo"]}<h1>{s["name"]}</h1><p>{s["desc"]}</p></header>
<nav aria-label="頁內導覽">{nav}</nav>
<main>
{secs}
<section id="visit"><h2>地址、營業時間及預約</h2>
<p>地址：九龍旺角示範街 1 號（虛構地址）<br>營業時間：{s["hours"]}<br>電話／WhatsApp：+{PHONE}（示範號碼）</p>
<iframe title="{s["name"]}位置地圖（旺角）" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=114.1650%2C22.3150%2C114.1750%2C22.3225&amp;layer=mapnik"></iframe>
<p><a href="https://www.openstreetmap.org/search?query={MAP_Q}" rel="noopener">在 OpenStreetMap 查看旺角地圖</a>（地圖位置僅供示範）</p>
<p class="note">※ 本網站為示範作品：店名、地址、電話、評價均為虛構。</p></section>
</main>
<a class="wa fix" href="{w}" rel="noopener">{s["cta"]}（示範）</a>
<footer>© 2026 {s["name"]}（示範） · 網站設計：網站製作</footer>
</body></html>'''
    open(f"{d}/index.html","w").write(page)
open("robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+f"<url><loc>{BASE}/</loc></url>\n"+"".join(f"<url><loc>{BASE}/{d}/</loc></url>\n" for d in SITES)+"</urlset>\n")
open("index.html","w").write('<!DOCTYPE html><html lang="zh-HK"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>香港小商家單頁網站示範</title><meta name="description" content="香港小商家單頁網站示範作品集：茶餐廳及美容院。"></head><body><h1>示範作品集</h1><ul><li><a href="cha-chaan-teng/">港味茶餐廳</a></li><li><a href="beauty-salon/">美麗軒美容院</a></li></ul></body></html>')
