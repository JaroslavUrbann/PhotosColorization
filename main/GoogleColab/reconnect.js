function getDialog() {
    var doc = document.getElementsByTagName("BODY")[0];
    for (var i = 0; i < doc.childNodes.length; i++) {
        if (doc.childNodes[i].className == "yes-no-dialog") {
            return doc.childNodes[i];
        }
    }
    return null;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function main() {
    while(true){
        var dialog = getDialog();
        console.log(dialog);
        if(dialog instanceof Element || dialog instanceof HTMLDocument){
            // dialog.childNodes[0].childNodes[2].childNodes[0].click(); for gpu close to memory limit
            dialog.childNodes[0].childNodes[2].childNodes[1].click();
        }
        await sleep(300000);
    }
}

main();
