let discordURL = document.getElementById('discordurl');
let memeURL = document.getElementById('urlselect');
let output = document.getElementById('linkout');
let enableAlts = document.getElementById('alts');
let memeAlts = document.getElementById('memeselect');
let CDN_REGEX = /^(https:\/\/cdn.discordapp.com\/attachments\/)([^{}|\\^\[\]`<>#;\/?:@&=+$,]{1,50}\/)([^{}|\\^\[\]`<>#;\/?:@&=+$,]{1,50}\/)([^{}|\\^\[\]`<>#;\/?:@&=+$,]{1,50})$/;

discordURL.addEventListener('input', updateURL);
memeURL.addEventListener('change', updateURL);
memeAlts.addEventListener('change', updateURL);
enableAlts.addEventListener('click', updateURL);
enableAlts.addEventListener('click', controlAlts);

function updateURL() {
    let content = discordURL.value;
    let target = memeURL.value;

    let match = CDN_REGEX.exec(content);

    if (match != null) {
        let uuid1 = match[2];
        let uuid2 = match[3];
        let file = match[4];

        if (enableAlts.checked) {
          var memeshard = `shard${memeAlts.value}/`;
        }
        else {
          var memeshard = "";
        }

        console.log(memeshard);

        console.log("Alts: " + enableAlts.checked);

        console.log("Dis: " + memeAlts.disabled);

        output.innerText = `https://${target}/attachments/${memeshard}${uuid1}${uuid2}${file}`;
    }
}

function controlAlts() {
    memeAlts.disabled = ! enableAlts.checked;
    updateURL();
}
