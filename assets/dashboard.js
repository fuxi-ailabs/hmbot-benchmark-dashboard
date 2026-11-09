(() => {
  const section = document.querySelector('#migration-results');
  if (!section) return;
  const body = section.querySelector('tbody');
  const rows = [...body.rows];
  const controls = Object.fromEntries(['model','harness','batch','search','sort','direction'].map(id => [id, section.querySelector('#'+id)]));
  const params = new URLSearchParams(location.search);
  for (const [id, control] of Object.entries(controls)) {
    const value = params.get(id);
    if (value !== null && (control.tagName === 'INPUT' || [...control.options].some(o => o.value === value))) control.value = value;
  }
  function update() {
    const {model,harness,batch,search,sort,direction} = controls;
    const query = search.value.trim().toLowerCase();
    let visible = 0;
    const metric = sort.value;
    const ascending = direction.value === 'asc';
    rows.sort((a,b) => {
      const av = a.dataset[metric], bv = b.dataset[metric];
      // Unknown values always follow known values, in either direction. Zero is known.
      if (av === '' && bv !== '') return 1;
      if (bv === '' && av !== '') return -1;
      const delta = av === '' ? 0 : Number(av) - Number(bv);
      return (ascending ? delta : -delta) || a.dataset.run.localeCompare(b.dataset.run);
    });
    const metricNames = {functional:'功能完备度',ui:'UI 分',tokens:'Token 数',duration:'迁移耗时'};
    for (const row of rows) {
      row.hidden = !((model.value === 'all' || row.dataset.model === model.value) &&
        (harness.value === 'all' || row.dataset.harness === harness.value) &&
        (batch.value === 'all' || row.dataset.batch === batch.value) &&
        row.textContent.toLowerCase().includes(query));
      if (!row.hidden) visible++;
      body.append(row);
    }
    section.querySelector('#result-count').textContent = `${visible} / ${rows.length} 次运行 · ${metricNames[metric]}${ascending?'升序':'降序'}`;
    section.querySelector('#empty-results').hidden = visible !== 0;
    section.querySelector('.table-wrap').hidden = visible === 0;
    for (const button of section.querySelectorAll('[data-sort]')) {
      const active = button.dataset.sort === metric;
      button.classList.toggle('active', active);
      button.textContent = button.dataset.label + (active ? (ascending?' ↑':' ↓') : ' ↕');
      button.closest('th').setAttribute('aria-sort',active ? (ascending?'ascending':'descending') : 'none');
    }
    const url = new URL(location.href);
    for (const [id,control] of Object.entries(controls)) {
      const defaults = {model:'all',harness:'all',batch:'all',search:'',sort:'functional',direction:'desc'};
      if (control.value === defaults[id]) url.searchParams.delete(id);
      else url.searchParams.set(id, control.value);
    }
    if (location.protocol !== 'file:') history.replaceState(null,'',url);
  }
  for (const control of Object.values(controls)) control.addEventListener('input',update);
  section.querySelector('#reset').addEventListener('click',() => {
    Object.assign(controls.model,{value:'all'}); controls.harness.value='all'; controls.batch.value='all';
    controls.search.value=''; controls.sort.value='functional'; controls.direction.value='desc'; update();
  });
  for (const button of section.querySelectorAll('[data-sort]')) button.addEventListener('click',() => {
    if (controls.sort.value === button.dataset.sort) controls.direction.value=controls.direction.value === 'asc'?'desc':'asc';
    else {controls.sort.value=button.dataset.sort;controls.direction.value=['tokens','duration'].includes(button.dataset.sort)?'asc':'desc';}
    update();
  });
  update();
})();
