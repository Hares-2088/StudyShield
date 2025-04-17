let isFocusSessionActive = false;
let blockedSites = [];

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'startFocus') {
    blockedSites = message.blockedSites;
    isFocusSessionActive = true;
    console.log('Focus session started. Blocking:', blockedSites);
  }
});

// Block websites during focus session
chrome.webRequest.onBeforeRequest.addListener(
  function (details) {
    if (isFocusSessionActive && blockedSites.some(site => details.url.includes(site))) {
      return { cancel: true }; // Block the request
    }
  },
  { urls: ['<all_urls>'] }, // Monitor all URLs
  ['blocking']
);