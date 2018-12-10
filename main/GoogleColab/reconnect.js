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
            if(dialog.childNodes[0].childNodes[1].childNodes[0].textContent == "GPU memory usage is close to the limit"){
                dialog.childNodes[0].childNodes[2].childNodes[0].click();
            }
            else{
                dialog.childNodes[0].childNodes[2].childNodes[1].click();
            }
        }
        await sleep(300000);
    }
}

main();
/*
<colab-dialog class="yes-no-dialog"><colab-dialog-impl role="dialog" tabindex="-1" class="x-scope colab-dialog-impl-0" style="outline: none; position: fixed; top: 308.886px; left: 0.227295px; box-sizing: border-box; max-height: 805.009px; max-width: 1125px;">

    <div class="content-area"><h2>GPU memory usage is close to the limit</h2><div class="flex">Your GPU is close to its memory limit. You will not be able to use any additional memory in this session. Currently, 9.18 GB / 11.17 GB is being used. Would you like to terminate some sessions in order to free up GPU memory (state will be lost for those sessions)?</div></div><div class="buttons"><paper-button id="cancel" dialog-dismiss="" role="button" tabindex="0" animated="" aria-disabled="false" elevation="0" class="x-scope paper-button-0">Ignore</paper-button><paper-button id="ok" autofocus="" dialog-confirm="" role="button" tabindex="0" animated="" aria-disabled="false" elevation="0" class="x-scope paper-button-0">Manage sessions<paper-ripple class="style-scope paper-button">


    <div id="background" class="style-scope paper-ripple"></div>
    <div id="waves" class="style-scope paper-ripple"></div>
  </paper-ripple></paper-button></div>
  </colab-dialog-impl></colab-dialog>
*/