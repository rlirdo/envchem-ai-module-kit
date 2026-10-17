
document.querySelectorAll('.copy').forEach(b=>b.onclick=()=>{const t=b.parentElement.querySelector('.pt').innerText;navigator.clipboard.writeText(t).then(()=>{b.textContent='已複製 ✓';setTimeout(()=>b.textContent='複製',1500)})});
const lb=document.getElementById('lb');document.querySelectorAll('figure img').forEach(i=>i.onclick=()=>{lb.querySelector('img').src=i.src;lb.style.display='flex'});if(lb)lb.onclick=()=>lb.style.display='none';
const secs=[...document.querySelectorAll('section[data-stage]')],pills=[...document.querySelectorAll('.flowbar a[data-s]')];
if(secs.length){const io=new IntersectionObserver(es=>{es.forEach(x=>{if(x.isIntersecting){const s=x.target.dataset.stage;pills.forEach(p=>p.classList.toggle('on',p.dataset.s===s))}})},{rootMargin:'-45% 0px -50% 0px'});secs.forEach(s=>io.observe(s))}
