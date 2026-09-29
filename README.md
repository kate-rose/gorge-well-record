# The Gorge Well Record

An Open Gorge community records project. Neighbors using public records to find the old oil and
gas test wells in the six Columbia River Gorge counties (Clark, Skamania and Klickitat in Washington;
Multnomah, Hood River and Wasco in Oregon), so they can be sealed for good.

One self-contained page (`index.html`), served by GitHub Pages.

## Building

Edit `page.html`, then run `python3 build.py`. It inlines the map (`assets/_map.svg`) and writes
`index.html`. `tools_map.py` rebuilds the map from `assets/_counties.geojson`, `assets/_nsa.geojson`
and the well list inside the script.

## Embedding

`?theme=light` or `?theme=dark` pins the colors. With no parameter, the page follows the reader's
system setting. When framed, the page posts its height to the parent as
`{type: 'gorge-well-record:height', height}` so the iframe can grow to fit:

```html
<iframe id="gorge-well-record" src="https://kate-rose.github.io/gorge-well-record/?theme=light"
  title="The Gorge Well Record" style="width:100%;border:0;min-height:1200px;display:block" loading="lazy"></iframe>
<script>
window.addEventListener('message', function (e) {
  if (e.origin !== 'https://kate-rose.github.io') return;
  if (e.data && e.data.type === 'gorge-well-record:height') {
    document.getElementById('gorge-well-record').style.height = e.data.height + 'px';
  }
});
</script>
```

## Sources

Washington DNR / Washington Geological Survey oil and gas wells; Oregon DOGAMI permit records and
Miscellaneous Paper 6 (1954, rev. 1965); USGS aerial single frames (1952, 1953, 1955) via
EarthExplorer; USDA NAIP imagery via USGS; USGS orphan well dataset (2022); USGS PAD-US 4.1;
BLM PLSS; WSDOT mileposts; Census TIGERweb; U.S. Forest Service Scenic Area boundary.
Photo alignment by Open Gorge, accurate to about 20 to 50 m.

Independent analysis by Kate Bertash for the Skamania Dispatch and Open Gorge. Anyone can use it.
