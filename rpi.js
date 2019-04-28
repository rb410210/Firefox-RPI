browser.contextMenus.create({
  id: "pushToRpiLink",
  title: "Download to Raspberry Pi",
  contexts: ["link"]
});


function onResponse(response) {
  console.log("Received " + response);
  browser.tabs.executeScript({
    file: "passive.js"
  });

}

function onError(error) {
  console.log(`Error: `, error);
  browser.tabs.executeScript({
    file: "passive.js"
  });
}

browser.contextMenus.onClicked.addListener(function(info, tab) {
  if (info && info.menuItemId === 'pushToRpiLink') {
    console.log("Downloading to Raspberry Pi", info.linkUrl);

    browser.tabs.executeScript({
      file: "active.js"
    });

    var sending = browser.runtime.sendNativeMessage("firefox_rpi_native",
      info.linkUrl);
    sending.then(onResponse, onError);
  }
});
