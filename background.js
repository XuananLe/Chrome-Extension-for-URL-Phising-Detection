function setupContextMenu() {
  chrome.contextMenus.update(
    "Url-Net",
    { title: "Url Net", contexts: ["link"] },
    function () {
      if (chrome.runtime.lastError) {
        chrome.contextMenus.create({
          title: "Url Net",
          contexts: ["link"],
          id: "Url-Net",
          visible: true,
        });
      }
    }
  );
}

function create_contribution_menu() {
  chrome.contextMenus.update(
    "contribute-links",
    { title: "Contribute Links To Us", contexts: ["all"] },
    function () {
      if (chrome.runtime.lastError) {
        chrome.contextMenus.create({
          title: "Contribute Links To Us",
          contexts: ["link"],
          parentId: "Url-Net",
          id: "contribute-links",
          visible: true,
        });
      }
    }
  );
}
function create_inspect_this_link() {
  chrome.contextMenus.update(
    "inspect-link",
    { title: "Inspect This Link", contexts: ["link"] },
    function () {
      if (chrome.runtime.lastError) {
        chrome.contextMenus.create({
          title: "Inspect This Link",
          contexts: ["link"],
          parentId: "Url-Net",
          id: "inspect-link",
          visible: true,
        });
      }
    }
  );
}

setupContextMenu();
create_contribution_menu();
create_inspect_this_link();
chrome.contextMenus.onClicked.addListener(function (info, tab) {
  if (info.menuItemId === "inspect-link") {
    console.log(info.linkUrl);
    fetch(info.linkUrl).then((response) => {
      if (response.ok) {
        const link = response.url;
        console.log("Link stored:", link);
        chrome.storage.sync.set({Link: link }, () => {
          console.log("Link stored in local storage");
          chrome.runtime.sendMessage({Link: link}); 
        });
      }
    });
    chrome.windows.create({
      url: "popup/popup.html",
      type: "popup",
      width: 300,
      height: 480,
      left: 400,
      top: 400
    });
  } else 
  if (info.menuItemId === "contribute-links") {
    chrome.tabs.create({ url: "Contribute_Links/Contribute.html" });
  }
});
