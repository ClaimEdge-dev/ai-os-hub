const next10=[
  'Lock reference board categories','Produce four brand boards','Render four singlet families front/back',
  'Render 8-step Achievement Apparel Ladder','Build vendor sample/QC pack','Build facility teaser/first-look templates',
  'Build social template matrix','Build website hero + navigation','Load results register skeleton','Assemble owner review board'
];
export default function Page(){
  return <main style={{padding:24,fontFamily:'system-ui',background:'#0b0d0c',color:'#f5f0df',minHeight:'100vh'}}>
    <p style={{color:'#c9a44c',fontWeight:800}}>DEBO • CWA 14</p>
    <h1>CWA Dominant Board</h1>
    <p>Private Chief-of-Staff command center for brand, apparel, facility, website, results, vendor/store and approvals.</p>
    <section style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(260px,1fr))',gap:16,marginTop:24}}>
      <article style={{border:'1px solid #29322d',borderRadius:16,padding:18}}><b>Active Objective</b><h2>Achievement Apparel Ladder</h2></article>
      <article style={{border:'1px solid #29322d',borderRadius:16,padding:18}}><b>Release Gate</b><h2>Approval Required</h2></article>
      <article style={{border:'1px solid #29322d',borderRadius:16,padding:18}}><b>Design Direction</b><h2>Heritage × Blackout</h2></article>
    </section>
    <h2 style={{marginTop:28}}>Next 10</h2>
    <ol>{next10.map(x=><li key={x} style={{padding:5}}>{x}</li>)}</ol>
  </main>
}
