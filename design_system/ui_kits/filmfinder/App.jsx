// Components for the FilmFinder UI kit.

const { useState, useEffect } = React;

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "accent": "#D8352A",
  "paper": "#FBF8F3",
  "radius": 8,
  "density": "regular",
  "headingStyle": "serif",
  "heroLayout": "editorial",
  "showLiveBar": true,
  "showDescriptions": true,
  "headline": "Wann läuft Ihr Film im Fernsehen?",
  "subhead": "Durchsuchen Sie das Programm von über 30 deutschen Sendern — und lassen Sie sich benachrichtigen, sobald Ihre Sendung wieder erscheint.",
  "accentLive": true
}/*EDITMODE-END*/;

function TopNav() {
  return (
    <header className="nav">
      <div className="nav-inner">
        <a href="#" className="nav-logo"><img src="../../assets/logo.svg" alt="FilmFinder"/></a>
        <nav className="nav-tabs">
          <button className="nav-tab active"><Icons.Search size={16}/>Suche</button>
        </nav>
      </div>
    </header>
  );
}

function SearchHero({ query, setQuery, onSubmit, t }) {
  // split headline: if it contains "Ihr Film", accent that word
  const hl = t.headline;
  const accentWord = /Ihr Film|Tatort|James Bond|Ihre Serie/i;
  const m = hl.match(accentWord);
  const before = m ? hl.slice(0, m.index) : hl;
  const accent = m ? m[0] : '';
  const after = m ? hl.slice(m.index + m[0].length) : '';

  return (
    <section className={"hero hero-" + t.heroLayout}>
      <div className="hero-eyebrow"><span className="dot"/>Freies Fernsehen &middot; durchsuchbar</div>
      <h1>{before}{accent && <span className="accent">{accent}</span>}{after}</h1>
      {t.subhead && <p className="hero-sub">{t.subhead}</p>}
      <form className="search-bar" onSubmit={(e) => { e.preventDefault(); onSubmit(); }}>
        <span className="icon"><Icons.Search size={20}/></span>
        <input value={query} onChange={e => setQuery(e.target.value)} placeholder="z.B. Tatort, James Bond, Krimi…" />
        <button type="submit" className="btn btn-primary btn-lg">Suchen</button>
      </form>
      <div className="suggestion-list">
        <span className="label">Beliebt:</span>
        {SUGGESTIONS.map(s => (
          <button key={s} className="sugg-pill" onClick={() => { setQuery(s); onSubmit(s); }}>{s}</button>
        ))}
      </div>
    </section>
  );
}

function ChannelFilter({ selected, onToggle }) {
  return (
    <div className="chip-rail">
      <button className={"chip chip-all" + (!selected ? ' active' : '')} onClick={() => onToggle(null)}>Alle Sender</button>
      {CHANNELS.map(c => (
        <button key={c.id} className={"chip" + (selected === c.id ? ' active' : '')} onClick={() => onToggle(c.id)}>
          <img className="chip-logo" src={LOGO(c.id)} alt=""/>{c.name}
        </button>
      ))}
    </div>
  );
}

function ProgramRow({ p, onToggleFav, fav, t }) {
  const showLive = p.live && t.accentLive;
  return (
    <article className={"program" + (showLive && t.showLiveBar ? ' live' : '')}>
      <img className="program-logo" src={LOGO(p.channel)} alt=""/>
      <div className="program-time">
        <span className="time">{p.time}</span>
        <span className="date">{p.date}</span>
      </div>
      <div className="program-body">
        <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:4,flexWrap:'wrap'}}>
          {showLive && <span className="badge badge-live"><span className="dot"/>Jetzt live</span>}
        </div>
        <div className="title">{p.title}</div>
        {t.showDescriptions && <div className="desc">{p.desc}</div>}
        <div className="meta-row">
          <span>{p.channelName}</span><span className="sep"/>
          <span>{p.genre}</span><span className="sep"/>
          <span>{p.duration}</span>
        </div>
      </div>
      <div className="program-actions">
        <button className={"icon-btn" + (fav ? ' active' : '')} onClick={() => onToggleFav(p.id)} title="Favorit">
          {fav ? <Icons.HeartFill size={18}/> : <Icons.Heart size={18}/>}
        </button>
      </div>
    </article>
  );
}

function CoverageTable() {
  return (
    <div className="card-surface coverage">
      <h3>Abdeckung pro Sender</h3>
      {COVERAGE.map(c => (
        <div key={c.channel} className="coverage-row">
          <img src={LOGO(c.channel)} style={{width:28,height:28,borderRadius:4}} alt=""/>
          <span className="name">{c.name}</span>
          <span className="until">bis {c.until}</span>
          <span className="bar"><span style={{width:c.pct+'%'}}/></span>
        </div>
      ))}
    </div>
  );
}

function Toast({ msg, onDone }) {
  useEffect(() => {
    if (!msg) return;
    const id = setTimeout(onDone, 3200);
    return () => clearTimeout(id);
  }, [msg]);
  if (!msg) return null;
  return <div className="toast-wrap"><div className="toast"><span className="dot"/>{msg}</div></div>;
}

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const [query, setQuery] = useState('');
  const [searched, setSearched] = useState(false);
  const [lastQ, setLastQ] = useState('');
  const [channel, setChannel] = useState(null);
  const [showPast, setShowPast] = useState(false);
  const [favs, setFavs] = useState(new Set([3]));
  const [toast, setToast] = useState('');

  // apply tweaks to CSS vars
  useEffect(() => {
    const r = document.documentElement;
    r.style.setProperty('--accent', t.accent);
    // derive hover as darker
    r.style.setProperty('--accent-hover', shade(t.accent, -12));
    r.style.setProperty('--accent-tint', shade(t.accent, 82, true));
    r.style.setProperty('--paper-50', t.paper);
    r.style.setProperty('--paper-100', shade(t.paper, -3));
    r.style.setProperty('--paper-200', shade(t.paper, -8));
    r.style.setProperty('--radius-md', t.radius + 'px');
    const sp = { compact: { pad: '10px 14px', gap: '6px' }, regular: { pad: '14px 18px', gap: '10px' }, comfy: { pad: '18px 22px', gap: '14px' }}[t.density];
    r.style.setProperty('--prog-pad', sp.pad);
    r.style.setProperty('--prog-gap', sp.gap);
    r.style.setProperty('--heading-font', t.headingStyle === 'serif' ? 'var(--font-serif)' : 'var(--font-sans)');
  }, [t.accent, t.paper, t.radius, t.density, t.headingStyle]);

  const onSearch = (q) => {
    const qq = q || query;
    if (!qq) return;
    setQuery(qq);
    setLastQ(qq);
    setSearched(true);
  };

  const filtered = React.useMemo(() => {
    let list = PROGRAMS;
    if (channel) list = list.filter(p => p.channel === channel);
    return list;
  }, [channel]);

  const toggleFav = (id) => {
    const n = new Set(favs);
    if (n.has(id)) { n.delete(id); setToast('Favorit entfernt.'); }
    else { n.add(id); setToast(`„${PROGRAMS.find(p => p.id === id).title}" zu Favoriten hinzugefügt.`); }
    setFavs(n);
  };

  return (
    <>
      <TopNav/>
      <main className="page">
        <SearchHero query={query} setQuery={setQuery} onSubmit={onSearch} t={t}/>

        {searched && (
          <section>
            <div className="section-head">
              <h2>Ergebnisse für „{lastQ}"</h2>
              <span className="count">{filtered.length} Treffer</span>
            </div>

            <div style={{display:'flex',gap:12,alignItems:'center',marginBottom:24,flexWrap:'wrap'}}>
              <ChannelFilter selected={channel} onToggle={setChannel}/>
            </div>

            <div style={{display:'flex',gap:10,alignItems:'center',marginBottom:20}}>
              <label style={{display:'inline-flex',gap:8,alignItems:'center',fontSize:14,color:'var(--fg-muted)',cursor:'pointer'}}>
                <input type="checkbox" checked={showPast} onChange={e => setShowPast(e.target.checked)}/>
                Vergangene Sendungen anzeigen
              </label>
            </div>

            <div className="program-list" style={{marginBottom:'var(--space-10)'}}>
              {filtered.map(p => (
                <ProgramRow key={p.id} p={p} onToggleFav={toggleFav} fav={favs.has(p.id)} t={t}/>
              ))}
            </div>

            <CoverageTable/>
          </section>
        )}
      </main>

      <Toast msg={toast} onDone={() => setToast('')}/>

      <TweaksPanel>
        <TweakSection label="Brand"/>
        <TweakColor label="Akzentfarbe" value={t.accent} onChange={(v) => setTweak('accent', v)}/>
        <TweakColor label="Papierton" value={t.paper} onChange={(v) => setTweak('paper', v)}/>

        <TweakSection label="Typografie"/>
        <TweakRadio label="Überschriften" value={t.headingStyle}
                    options={[{value:'serif',label:'Serif'},{value:'sans',label:'Sans'}]}
                    onChange={(v) => setTweak('headingStyle', v)}/>

        <TweakSection label="Layout"/>
        <TweakRadio label="Hero" value={t.heroLayout}
                    options={[{value:'editorial',label:'Editorial'},{value:'compact',label:'Kompakt'}]}
                    onChange={(v) => setTweak('heroLayout', v)}/>
        <TweakRadio label="Dichte" value={t.density}
                    options={['compact','regular','comfy']}
                    onChange={(v) => setTweak('density', v)}/>
        <TweakSlider label="Eckradius" value={t.radius} min={0} max={16} step={1} unit="px"
                     onChange={(v) => setTweak('radius', v)}/>

        <TweakSection label="Rows"/>
        <TweakToggle label="Beschreibungen zeigen" value={t.showDescriptions} onChange={(v) => setTweak('showDescriptions', v)}/>
        <TweakToggle label="Jetzt-live Akzent" value={t.accentLive} onChange={(v) => setTweak('accentLive', v)}/>
        <TweakToggle label="Live-Leiste" value={t.showLiveBar} onChange={(v) => setTweak('showLiveBar', v)}/>

        <TweakSection label="Kopie"/>
        <TweakText label="Headline" value={t.headline} onChange={(v) => setTweak('headline', v)}/>
        <TweakText label="Unterzeile" value={t.subhead} onChange={(v) => setTweak('subhead', v)} multiline/>
      </TweaksPanel>
    </>
  );
}

// simple hex shader: percent in -100..100; if tint=true, lighten toward white
function shade(hex, percent, tint) {
  const h = hex.replace('#','');
  const full = h.length === 3 ? h.split('').map(c => c+c).join('') : h;
  let r = parseInt(full.slice(0,2),16), g = parseInt(full.slice(2,4),16), b = parseInt(full.slice(4,6),16);
  if (tint) {
    // percent here is "how far toward white" 0..100
    const p = Math.max(0, Math.min(100, percent)) / 100;
    r = Math.round(r + (255 - r) * p);
    g = Math.round(g + (255 - g) * p);
    b = Math.round(b + (255 - b) * p);
  } else {
    const p = percent / 100;
    r = Math.max(0, Math.min(255, Math.round(r + 255 * p)));
    g = Math.max(0, Math.min(255, Math.round(g + 255 * p)));
    b = Math.max(0, Math.min(255, Math.round(b + 255 * p)));
  }
  return '#' + [r,g,b].map(x => x.toString(16).padStart(2,'0')).join('');
}

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
