let discordURL = document.getElementById('discordurl');

let memeURL = document.getElementById('urlselect');

let output = document.getElementById('linkout');


discordURL.addEventListener('input', updateURL);

memeURL.addEventListener('change', updateURL);


let CDN_REGEX = /^(https:\/\/cdn.discordapp.com\/attachments\/)([^{}|\\^\[\]`<>#;\/?:@&=+$,]{1,50}\/)([^{}|\\^\[\]`<>#;\/?:@&=+$,]{1,50}\/)([^{}|\\^\[\]`<>#;\/?:@&=+$,]{1,50})$/g;

function updateURL() {
    let content = discordURL.value;
    let target = memeURL.value;

    console.log(content);
    console.log(target);

    // let match = content.exec(CDN_REGEX);

    let match = CDN_REGEX.exec(content);

    console.log(match);

    if (match != null) {
        let uuid1 = match[2];
        let uuid2 = match[3];
        let file = match[4];

        output.innerText = `https://${target}/attachments/${uuid1}${uuid2}${file}`;
    }
}